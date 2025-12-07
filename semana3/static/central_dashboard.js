// Configuración global
const API_BASE_URL = 'http://localhost:8000';
const AUTH_API_URL = 'http://localhost:8002';
const BRANCH_API_URL = 'http://localhost:8001'; // Sucursal API en puerto 8001
const ITEMS_PER_PAGE = 5;

// Variables globales
let allProducts = [];
let allBranchProducts = [];
let currentPage = 1;
let branchCurrentPage = 1;
let editingProductId = null;
let selectedBranch = BRANCH_API_URL;
let authToken = localStorage.getItem('authToken');
let userRole = localStorage.getItem('userRole');

// Funciones de Autenticación
function updateAuthUI() {
    const btnLogin = document.getElementById('btnLogin');
    const userSection = document.getElementById('userSection');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const btnAddProduct = document.getElementById('btnAddProduct');

    if (authToken) {
        btnLogin.style.display = 'none';
        userSection.style.display = 'flex';
        usernameDisplay.textContent = `Rol: ${userRole || 'Usuario'}`;
        btnAddProduct.style.display = 'block';
    } else {
        btnLogin.style.display = 'block';
        userSection.style.display = 'none';
        btnAddProduct.style.display = 'none';
    }
}

async function login(username, password) {
    try {
        const payload = {
            email: username,
            password: password
        };

        const response = await fetch(`${AUTH_API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            // Decodificar token para obtener rol (simplificado)
            const payload = JSON.parse(atob(authToken.split('.')[1]));
            userRole = payload.role;
            
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('userRole', userRole);
            
            updateAuthUI();
            bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
            loadProducts(); // Recargar para habilitar botones si es admin
        } else {
            const error = await response.json();
            document.getElementById('loginMessage').textContent = error.detail || 'Error de autenticación';
        }
    } catch (error) {
        document.getElementById('loginMessage').textContent = 'Error de conexión';
        console.error(error);
    }
}

function logout() {
    authToken = null;
    userRole = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    updateAuthUI();
    loadProducts(); // Recargar para deshabilitar botones
}

function getHeaders() {
    const headers = {
        'Content-Type': 'application/json'
    };
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    return headers;
}

// Funciones para actualizar las estadísticas
function updateStatistics() {
    const totalProducts = allProducts.length;
    const totalStock = allProducts.reduce((sum, product) => sum + product.stock, 0);
    const totalValue = allProducts.reduce((sum, product) => sum + (product.precio * product.stock), 0).toFixed(2);
    
    document.getElementById('totalProducts').textContent = totalProducts;
    document.getElementById('totalStock').textContent = totalStock;
    document.getElementById('totalValue').textContent = `$${totalValue}`;
}

// Mostrar productos en tabla con paginación
function displayProductsInTable(products, page = 1) {
    const tableBody = document.getElementById('inventoryTableBody');
    const paginationInfo = document.getElementById('inventoryPaginationInfo');
    const pagination = document.getElementById('inventoryPagination');
    
    // Calcular paginación
    const totalProducts = products.length;
    const totalPages = Math.ceil(totalProducts / ITEMS_PER_PAGE);
    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, totalProducts);
    const currentProducts = products.slice(startIndex, endIndex);
    
    // Actualizar información de paginación
    paginationInfo.textContent = `Mostrando ${startIndex + 1}-${endIndex} de ${totalProducts} productos`;
    
    if (currentProducts.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    <i class="bi bi-inbox"></i>
                    <div class="text-muted">No hay productos disponibles</div>
                </td>
            </tr>
        `;
    } else {
        const isAdmin = userRole === 'admin';
        tableBody.innerHTML = currentProducts.map(product => `
            <tr>
                <td><strong>${product.id}</strong></td>
                <td>${product.nombre}</td>
                <td><span class="text-success fw-bold">$${product.precio.toFixed(2)}</span></td>
                <td>
                    <span class="badge ${product.stock > 10 ? 'bg-success' : product.stock > 0 ? 'bg-warning' : 'bg-danger'}">
                        ${product.stock}
                    </span>
                </td>
                <td class="text-end">
                    ${isAdmin ? `
                    <button class="btn btn-outline-primary btn-sm me-1" onclick="editProduct(${product.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-danger btn-sm" onclick="confirmDeleteProduct(${product.id}, '${product.nombre}')">
                        <i class="bi bi-trash"></i>
                    </button>
                    ` : '<small class="text-muted">Solo lectura</small>'}
                </td>
            </tr>
        `).join('');
    }
    
    // Crear paginación
    createPagination(pagination, page, totalPages, 'loadProductPage');
}

// Mostrar productos de sucursal en tabla con paginación
function displayBranchProductsInTable(products, page = 1) {
    const tableBody = document.getElementById('branchInventoryTableBody');
    const paginationInfo = document.getElementById('branchPaginationInfo');
    const pagination = document.getElementById('branchPagination');
    
    // Calcular paginación
    const totalProducts = products.length;
    const totalPages = Math.ceil(totalProducts / ITEMS_PER_PAGE);
    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, totalProducts);
    const currentProducts = products.slice(startIndex, endIndex);
    
    // Actualizar información de paginación
    paginationInfo.textContent = `Mostrando ${startIndex + 1}-${endIndex} de ${totalProducts} productos`;
    
    if (currentProducts.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4">
                    <i class="bi bi-inbox"></i>
                    <div class="text-muted">No hay productos disponibles</div>
                </td>
            </tr>
        `;
    } else {
        tableBody.innerHTML = currentProducts.map(product => `
            <tr>
                <td><strong>${product.id}</strong></td>
                <td>${product.nombre}</td>
                <td>
                    <span class="badge ${product.stock > 10 ? 'bg-success' : product.stock > 0 ? 'bg-warning' : 'bg-danger'}">
                        ${product.stock}
                    </span>
                </td>
                <td class="text-end">
                    <button class="btn btn-outline-primary btn-sm" onclick="editBranchStock(${product.id}, '${product.nombre}', ${product.stock})">
                        <i class="bi bi-pencil"></i> Stock
                    </button>
                </td>
            </tr>
        `).join('');
    }
    
    // Crear paginación
    createPagination(pagination, page, totalPages, 'loadBranchPage');
}

// Crear controles de paginación
function createPagination(container, currentPage, totalPages, functionName) {
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let paginationHTML = '';
    
    // Botón anterior
    paginationHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <button class="page-link" onclick="${functionName}(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
                <i class="bi bi-chevron-left"></i>
            </button>
        </li>
    `;
    
    // Números de página
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            paginationHTML += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            paginationHTML += `<li class="page-item"><button class="page-link" onclick="${functionName}(${i})">${i}</button></li>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            paginationHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
    }
    
    // Botón siguiente
    paginationHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <button class="page-link" onclick="${functionName}(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
                <i class="bi bi-chevron-right"></i>
            </button>
        </li>
    `;
    
    container.innerHTML = paginationHTML;
}

// Funciones de paginación
function loadProductPage(page) {
    currentPage = page;
    displayProductsInTable(allProducts, currentPage);
}

function loadBranchPage(page) {
    branchCurrentPage = page;
    displayBranchProductsInTable(allBranchProducts, branchCurrentPage);
}

// Cargar notificaciones recientes
async function loadNotifications() {
    try {
        console.log('Cargando notificaciones...');
        const response = await fetch(`${API_BASE_URL}/sales/recent`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const notifications = await response.json();
        console.log('Notificaciones cargadas:', notifications);
        displayNotifications(notifications);
        
    } catch (error) {
        console.error('Error cargando notificaciones:', error);
        // Mostrar mensaje de error en notificaciones
        document.querySelector('.notifications-body').innerHTML = `
            <div class="no-notifications-icon">
                <i class="bi bi-exclamation-triangle text-warning"></i>
            </div>
            <div class="no-notifications">Error cargando notificaciones</div>
        `;
    }
}

// Mostrar notificaciones en el panel
function displayNotifications(notifications) {
    const notificationsBody = document.querySelector('.notifications-body');
    
    // Actualizar contador en el header
    document.getElementById('totalNotifications').textContent = notifications.length;
    
    if (!notifications || notifications.length === 0) {
        notificationsBody.innerHTML = `
            <div class="no-notifications-icon">
                <i class="bi bi-inbox"></i>
            </div>
            <div class="no-notifications">No hay notificaciones</div>
        `;
        return;
    }
    
    // Mostrar las notificaciones más recientes primero
    const sortedNotifications = notifications
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        .slice(0, 5); // Mostrar solo las últimas 5
    
    notificationsBody.innerHTML = sortedNotifications.map(notification => {
        const timestamp = new Date(notification.timestamp).toLocaleString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <div class="notification-item">
                <div class="notification-icon">
                    <i class="bi bi-cart-check text-success"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">Venta realizada</div>
                    <div class="notification-details">
                        <span class="branch-name">${notification.branch_id}</span> vendió 
                        <span class="quantity">${notification.quantity_sold}</span> unidades
                        del producto ID ${notification.product_id}
                    </div>
                    <div class="notification-time">${timestamp}</div>
                </div>
                <div class="notification-amount">
                    $${(notification.sale_price).toFixed(2)}
                </div>
            </div>
        `;
    }).join('');
}

// Cargar productos desde la API central
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventario`);
        if (response.ok) {
            allProducts = await response.json();
            displayProductsInTable(allProducts, currentPage);
            updateStatistics();
        } else {
            console.error('Error al cargar productos:', response.status);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        // Usar datos de ejemplo si no hay conexión
        allProducts = [
            { id: 1, nombre: "Manzanas Orgánicas", precio: 2.50, stock: 100 },
            { id: 2, nombre: "Pan Integral", precio: 1.80, stock: 50 },
            { id: 3, nombre: "Leche Deslactosada", precio: 3.20, stock: 30 },
            { id: 4, nombre: "Café Premium", precio: 8.90, stock: 25 },
            { id: 5, nombre: "Quinoa", precio: 12.50, stock: 15 }
        ];
        displayProductsInTable(allProducts, currentPage);
        updateStatistics();
    }
}

// Cargar productos de sucursal
async function loadBranchProducts() {
    try {
        const response = await fetch(`${selectedBranch}/inventario`);
        if (response.ok) {
            allBranchProducts = await response.json();
            displayBranchProductsInTable(allBranchProducts, branchCurrentPage);
        } else {
            console.error('Error al cargar productos de sucursal:', response.status);
        }
    } catch (error) {
        console.error('Error de conexión con sucursal:', error);
        // Datos de ejemplo para sucursal
        allBranchProducts = [
            { id: 1, nombre: "Manzanas Orgánicas", stock: 20 },
            { id: 2, nombre: "Pan Integral", stock: 15 },
            { id: 3, nombre: "Leche Deslactosada", stock: 8 }
        ];
        displayBranchProductsInTable(allBranchProducts, branchCurrentPage);
    }
}

// Funciones CRUD para productos

// Abrir modal para agregar producto
function addProduct() {
    if (!authToken) {
        alert('Debe iniciar sesión para realizar esta acción');
        return;
    }
    editingProductId = null;
    document.getElementById('productModalLabel').innerHTML = '<i class="bi bi-plus-circle me-2"></i>Agregar Producto';
    document.getElementById('productForm').reset();
    document.getElementById('productId').disabled = false;
    document.getElementById('productFormMessage').innerHTML = '';
    new bootstrap.Modal(document.getElementById('productModal')).show();
}

// Abrir modal para editar producto
function editProduct(productId) {
    if (!authToken) {
        alert('Debe iniciar sesión para realizar esta acción');
        return;
    }
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    editingProductId = productId;
    document.getElementById('productModalLabel').innerHTML = '<i class="bi bi-pencil me-2"></i>Editar Producto';
    document.getElementById('productId').value = product.id;
    document.getElementById('productId').disabled = true;
    document.getElementById('productName').value = product.nombre;
    document.getElementById('productPrice').value = product.precio;
    document.getElementById('productStock').value = product.stock;
    document.getElementById('productFormMessage').innerHTML = '';
    new bootstrap.Modal(document.getElementById('productModal')).show();
}

// Guardar producto (crear o editar)
async function saveProduct() {
    if (!authToken) {
        showMessage('productFormMessage', 'Sesión expirada. Inicie sesión nuevamente.', 'danger');
        return;
    }

    const id = parseInt(document.getElementById('productId').value);
    const name = document.getElementById('productName').value.trim();
    const price = parseFloat(document.getElementById('productPrice').value);
    const stock = parseInt(document.getElementById('productStock').value);
    
    if (!name || price <= 0 || stock < 0) {
        showMessage('productFormMessage', 'Por favor, complete todos los campos correctamente.', 'danger');
        return;
    }
    
    const productData = { id, name, price, stock };
    
    console.log('Enviando datos del producto:', productData);
    
    try {
        let response;
        const headers = getHeaders();
        
        if (editingProductId) {
            // Editar producto existente
            response = await fetch(`${API_BASE_URL}/products/${id}`, {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify(productData)
            });
        } else {
            // Crear nuevo producto
            response = await fetch(`${API_BASE_URL}/products`, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(productData)
            });
        }
        
        if (response.ok) {
            const result = await response.json();
            console.log('Producto guardado exitosamente:', result);
            showMessage('productFormMessage', `Producto ${editingProductId ? 'actualizado' : 'creado'} exitosamente.`, 'success');
            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
                loadProducts();
            }, 1000);
        } else {
            const errorData = await response.text(); // Cambiar a text() para ver el error completo
            console.error('Error del servidor (status:', response.status, '):', errorData);
            try {
                const errorJson = JSON.parse(errorData);
                showMessage('productFormMessage', errorJson.detail || 'Error al guardar el producto.', 'danger');
            } catch (e) {
                showMessage('productFormMessage', `Error del servidor: ${response.status}`, 'danger');
            }
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        showMessage('productFormMessage', 'Error de conexión. Inténtelo de nuevo.', 'danger');
    }
}

// Confirmar eliminación de producto
function confirmDeleteProduct(productId, productName) {
    if (!authToken) {
        alert('Debe iniciar sesión para realizar esta acción');
        return;
    }
    document.getElementById('deleteProductName').textContent = productName;
    document.getElementById('btnConfirmDelete').onclick = () => deleteProduct(productId);
    new bootstrap.Modal(document.getElementById('confirmDeleteModal')).show();
}

// Eliminar producto
async function deleteProduct(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
            loadProducts();
        } else {
            const error = await response.json();
            alert('Error al eliminar el producto: ' + (error.detail || 'Error desconocido'));
        }
    } catch (error) {
        alert('Error de conexión. Inténtelo de nuevo.');
    }
}

// Funciones para inventario de sucursal

// Abrir modal para editar stock de sucursal
function editBranchStock(productId, productName, currentStock) {
    document.getElementById('branchProductId').value = productId;
    document.getElementById('branchProductName').value = productName;
    document.getElementById('branchCurrentStock').value = currentStock;
    document.getElementById('branchNewStock').value = currentStock;
    document.getElementById('branchStockFormMessage').innerHTML = '';
    new bootstrap.Modal(document.getElementById('branchStockModal')).show();
}

// Guardar nuevo stock de sucursal
async function saveBranchStock() {
    const productId = parseInt(document.getElementById('branchProductId').value);
    const newStock = parseInt(document.getElementById('branchNewStock').value);
    
    if (newStock < 0) {
        showMessage('branchStockFormMessage', 'El stock no puede ser negativo.', 'danger');
        return;
    }
    
    try {
        const response = await fetch(`${selectedBranch}/products/${productId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stock: newStock })
        });
        
        if (response.ok) {
            showMessage('branchStockFormMessage', 'Stock actualizado exitosamente.', 'success');
            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById('branchStockModal')).hide();
                loadBranchProducts();
            }, 1000);
        } else {
            const error = await response.json();
            showMessage('branchStockFormMessage', error.detail || 'Error al actualizar el stock.', 'danger');
        }
    } catch (error) {
        showMessage('branchStockFormMessage', 'Error de conexión. Inténtelo de nuevo.', 'danger');
    }
}

// Función auxiliar para mostrar mensajes
function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar UI de autenticación
    updateAuthUI();
    
    // Cargar datos iniciales
    loadProducts();
    loadBranchProducts();
    loadNotifications(); // Cargar notificaciones al inicio
    
    // Event listeners para botones
    document.getElementById('btnAddProduct').addEventListener('click', addProduct);
    document.getElementById('btnSaveProduct').addEventListener('click', saveProduct);
    document.getElementById('btnSaveBranchStock').addEventListener('click', saveBranchStock);
    
    // Login/Logout
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        login(username, password);
    });
    
    document.getElementById('btnLogout').addEventListener('click', logout);
    
    // Event listener para cambio de sucursal
    document.getElementById('branchSelect').addEventListener('change', function(e) {
        selectedBranch = e.target.value;
        branchCurrentPage = 1;
        loadBranchProducts();
    });
    
    // Actualización automática cada 30 segundos
    setInterval(() => {
        loadProducts();
        loadBranchProducts();
        loadNotifications(); // Actualizar notificaciones también
    }, 30000);
});