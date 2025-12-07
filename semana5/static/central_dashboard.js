/* 
===============================================
EcoMarket Central Dashboard - Master JS
Integrates Week 3 UI/UX with Week 8 Auth & Microservices
===============================================
*/

// Configuración global
const CONFIG = {
    centralAPI: window.location.origin,
    authAPI: window.location.origin + '/api/auth',
    defaultBranch: window.location.origin + '/api/sucursal',
    updateInterval: 30000, // 30 segundos
    animationDelay: 300
};

// Variables globales
let selectedBranch = CONFIG.defaultBranch;
let inventoryData = [];
let branchInventoryData = [];
let salesData = [];
let filteredSalesData = [];
let currentEditingId = null;

// Variables de paginación
const ITEMS_PER_PAGE = 5;
const SALES_PER_PAGE = 10;
let centralCurrentPage = 1;
let branchCurrentPage = 1;
let salesCurrentPage = 1;
let filteredCentralData = [];
let filteredBranchData = [];
let isCentralFiltered = false;
let isBranchFiltered = false;
let isSalesFiltered = false;

// Utilidades generales
const Utils = {
    formatPrice: (price) => `$${parseFloat(price).toFixed(2)}`,
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    },
    showAlert: (containerId, message, type = 'success') => {
        const container = document.getElementById(containerId);
        if (!container) return;
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        container.innerHTML = `<div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        setTimeout(() => {
            const alert = container.querySelector('.alert');
            if (alert) alert.remove();
        }, 5000);
    },
    showLoading: (containerId, message = 'Cargando...') => {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                        ${message}
                    </td>
                </tr>`;
        }
    }
};

// Gestor de Autenticación (Week 8 Integration)
const AuthManager = {
    token: localStorage.getItem('authToken'),
    role: localStorage.getItem('userRole'),

    isAuthenticated: () => {
        return !!AuthManager.token && AuthManager.token !== 'null' && AuthManager.token !== 'undefined';
    },

    getHeaders: () => {
        const headers = { 'Content-Type': 'application/json' };
        if (AuthManager.isAuthenticated()) {
            headers['Authorization'] = `Bearer ${AuthManager.token}`;
        }
        return headers;
    },

    login: async (username, password) => {
        try {
            const response = await fetch(`${CONFIG.authAPI}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: username, password: password })
            });
            
            if (response.ok) {
                const data = await response.json();
                AuthManager.token = data.access_token;
                // Decode token to get role (simple base64 decode for payload)
                try {
                    const payload = JSON.parse(atob(data.access_token.split('.')[1]));
                    AuthManager.role = payload.role;
                } catch(e) { AuthManager.role = 'user'; }
                
                localStorage.setItem('authToken', AuthManager.token);
                localStorage.setItem('userRole', AuthManager.role);
                
                AuthManager.updateUI();
                bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
                Utils.showAlert('formMsg', 'Sesión iniciada correctamente');
            } else {
                const err = await response.json();
                alert(err.detail || 'Error de autenticación');
            }
        } catch (e) {
            console.error(e);
            alert('Error de conexión con el servicio de autenticación');
        }
    },

    logout: () => {
        AuthManager.token = null;
        AuthManager.role = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('userRole');
        AuthManager.updateUI();
        window.location.reload();
    },

    updateUI: () => {
        const btnLogin = document.getElementById('btnLogin');
        const userSection = document.getElementById('userSection');
        const usernameDisplay = document.getElementById('usernameDisplay');
        const btnAddProduct = document.getElementById('btnAddProduct');
        const btnAddBranchProduct = document.getElementById('btnAddBranchProduct');

        if (AuthManager.isAuthenticated()) {
            if (btnLogin) btnLogin.style.display = 'none';
            if (userSection) userSection.style.display = 'flex';
            if (usernameDisplay) usernameDisplay.textContent = `Rol: ${AuthManager.role || 'Usuario'}`;
            if (btnAddProduct) btnAddProduct.style.display = 'block';
            if (btnAddBranchProduct) btnAddBranchProduct.style.display = 'block';
        } else {
            if (btnLogin) btnLogin.style.display = 'block';
            if (userSection) userSection.style.display = 'none';
            if (btnAddProduct) btnAddProduct.style.display = 'none';
            if (btnAddBranchProduct) btnAddBranchProduct.style.display = 'none';
        }
        
        // Re-render tables to update button visibility
        InventoryManager.renderInventory();
        BranchManager.renderBranchInventory();
    },

    checkAuth: () => {
        if (!AuthManager.isAuthenticated()) {
            Utils.showAlert('formMsg', 'Debe iniciar sesión para realizar esta acción', 'warning');
            return false;
        }
        return true;
    }
};

// Gestor de Inventario Central
const InventoryManager = {
    fetchInventory: async () => {
        try {
            const response = await fetch(`${CONFIG.centralAPI}/inventario`);
            if (response.ok) {
                inventoryData = await response.json();
                InventoryManager.renderInventory();
                StatsManager.updateStats();
            }
        } catch (e) {
            console.error('Error fetching inventory', e);
            Utils.showAlert('formMsg', 'Error de conexión con el servidor central', 'danger');
        }
    },

    renderInventory: () => {
        const tbody = document.getElementById('inventoryBody');
        if (!tbody) return;

        const dataToShow = isCentralFiltered ? filteredCentralData : inventoryData;
        
        // Toggle header visibility based on auth
        const actionsHeader = document.querySelector('#inventoryBody').closest('table').querySelector('thead tr th:last-child');
        if (actionsHeader) {
            actionsHeader.style.display = AuthManager.isAuthenticated() ? '' : 'none';
        }

        if (dataToShow.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No hay productos</td></tr>`;
            return;
        }

        const startIndex = (centralCurrentPage - 1) * ITEMS_PER_PAGE;
        const paginatedData = dataToShow.slice(startIndex, startIndex + ITEMS_PER_PAGE);

        tbody.innerHTML = paginatedData.map(product => {
            const actionsCell = AuthManager.isAuthenticated() ? `
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="InventoryManager.editProduct(${product.id})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="InventoryManager.deleteProduct(${product.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>` : '';
            
            return `
            <tr data-id="${product.id}">
                <td><strong>${product.id}</strong></td>
                <td>${product.nombre || product.name}</td>
                <td>${Utils.formatPrice(product.precio || product.price)}</td>
                <td>
                    <span class="badge ${product.stock < 10 ? 'bg-warning' : 'bg-success'}">
                        ${product.stock}
                    </span>
                </td>
                ${actionsCell}
            </tr>
        `}).join('');

        CentralPagination.updatePaginationInfo(dataToShow.length);
    },

    addProduct: async (productData) => {
        if (!AuthManager.checkAuth()) return;
        try {
            const response = await fetch(`${CONFIG.centralAPI}/products`, {
                method: 'POST',
                headers: AuthManager.getHeaders(),
                body: JSON.stringify(productData)
            });
            if (response.ok) {
                Utils.showAlert('formMsg', 'Producto agregado correctamente');
                FormManager.resetForm();
                bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
                InventoryManager.fetchInventory();
            } else {
                const err = await response.json();
                throw new Error(err.detail || 'Error al agregar producto');
            }
        } catch (e) {
            Utils.showAlert('formMsg', e.message, 'danger');
        }
    },

    editProduct: (id) => {
        if (!AuthManager.checkAuth()) return;
        const product = inventoryData.find(p => p.id === id);
        if (product) {
            document.getElementById('centralProductId').value = product.id;
            document.getElementById('centralProductName').value = product.nombre || product.name;
            document.getElementById('centralProductPrice').value = product.precio || product.price;
            document.getElementById('centralProductStock').value = product.stock;
            new bootstrap.Modal(document.getElementById('editCentralModal')).show();
        }
    },

    updateProduct: async (id, productData) => {
        if (!AuthManager.checkAuth()) return;
        try {
            const response = await fetch(`${CONFIG.centralAPI}/products/${id}`, {
                method: 'PUT',
                headers: AuthManager.getHeaders(),
                body: JSON.stringify(productData)
            });
            if (response.ok) {
                Utils.showAlert('centralFormMsg', 'Producto actualizado correctamente');
                bootstrap.Modal.getInstance(document.getElementById('editCentralModal')).hide();
                InventoryManager.fetchInventory();
            } else {
                throw new Error('Error al actualizar producto');
            }
        } catch (e) {
            Utils.showAlert('centralFormMsg', e.message, 'danger');
        }
    },

    deleteProduct: async (id) => {
        if (!AuthManager.checkAuth()) return;
        if (!confirm('¿Está seguro de eliminar este producto?')) return;
        
        try {
            const response = await fetch(`${CONFIG.centralAPI}/products/${id}`, {
                method: 'DELETE',
                headers: AuthManager.getHeaders()
            });
            if (response.ok) {
                Utils.showAlert('formMsg', 'Producto eliminado');
                InventoryManager.fetchInventory();
            } else {
                throw new Error('Error al eliminar producto');
            }
        } catch (e) {
            Utils.showAlert('formMsg', e.message, 'danger');
        }
    }
};

// Gestor de Sucursales
const BranchManager = {
    fetchBranchInventory: async () => {
        try {
            Utils.showLoading('branchInventoryBody');
            console.log(`Fetching branch inventory from: ${selectedBranch}/inventory`);
            const response = await fetch(`${selectedBranch}/inventory`);
            if (response.ok) {
                branchInventoryData = await response.json();
                BranchManager.renderBranchInventory();
            } else {
                console.error('Branch API Error:', response.status, response.statusText);
                document.getElementById('branchInventoryBody').innerHTML = 
                    `<tr><td colspan="5" class="text-center text-danger">Error del servidor: ${response.status}</td></tr>`;
            }
        } catch (e) {
            console.error('Error fetching branch inventory', e);
            document.getElementById('branchInventoryBody').innerHTML = 
                `<tr><td colspan="5" class="text-center text-danger">Error de conexión: ${e.message}</td></tr>`;
        }
    },

    renderBranchInventory: () => {
        const tbody = document.getElementById('branchInventoryBody');
        if (!tbody) return;

        const dataToShow = isBranchFiltered ? filteredBranchData : branchInventoryData;
        
        // Toggle header visibility based on auth
        const actionsHeader = document.querySelector('#branchInventoryBody').closest('table').querySelector('thead tr th:last-child');
        if (actionsHeader) {
            actionsHeader.style.display = AuthManager.isAuthenticated() ? '' : 'none';
        }

        if (dataToShow.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="text-center">No hay productos</td></tr>`;
            return;
        }

        const startIndex = (branchCurrentPage - 1) * ITEMS_PER_PAGE;
        const paginatedData = dataToShow.slice(startIndex, startIndex + ITEMS_PER_PAGE);

        tbody.innerHTML = paginatedData.map(product => {
            const actionsCell = AuthManager.isAuthenticated() ? `
                <td class="text-end pe-4">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary rounded-start-pill" onclick="BranchManager.editBranchProduct(${product.id})" title="Editar Stock">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger rounded-end-pill" onclick="BranchManager.deleteBranchProduct(${product.id})" title="Eliminar de Sucursal">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>` : '';

            return `
            <tr data-id="${product.id}">
                <td><strong>${product.id}</strong></td>
                <td>${product.nombre || product.name}</td>
                <td>${Utils.formatPrice(product.precio || product.price || 0)}</td>
                <td>
                    <span class="badge ${product.stock < 10 ? 'bg-warning' : 'bg-success'}">
                        ${product.stock}
                    </span>
                </td>
                ${actionsCell}
            </tr>
        `}).join('');

        BranchPagination.updatePaginationInfo(dataToShow.length);
    },

    editBranchProduct: (id) => {
        const product = branchInventoryData.find(p => p.id === id);
        if (product) {
            document.getElementById('branchProductId').value = product.id;
            document.getElementById('branchProductName').value = product.nombre || product.name;
            document.getElementById('branchProductPrice').value = product.precio || product.price || 0;
            document.getElementById('branchProductStock').value = product.stock;
            new bootstrap.Modal(document.getElementById('editBranchModal')).show();
        }
    },

    updateBranchProduct: async (id, formData) => {
        if (!AuthManager.checkAuth()) return;
        // Nota: Las sucursales pueden requerir auth o no, dependiendo de la implementación
        try {
            const response = await fetch(`${selectedBranch}/products/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    stock: formData.stock,
                    price: formData.price
                })
            });
            if (response.ok) {
                Utils.showAlert('branchFormMsg', 'Producto actualizado', 'success');
                BranchManager.fetchBranchInventory();
                bootstrap.Modal.getInstance(document.getElementById('editBranchModal')).hide();
            } else {
                throw new Error('Error al actualizar sucursal');
            }
        } catch (e) {
            Utils.showAlert('branchFormMsg', e.message, 'danger');
        }
    },

    addBranchProduct: async (productData) => {
        if (!AuthManager.checkAuth()) return;
        try {
            const response = await fetch(`${selectedBranch}/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
            if (response.ok) {
                Utils.showAlert('branchFormMsg', 'Producto agregado a sucursal', 'success');
                BranchManager.fetchBranchInventory();
                bootstrap.Modal.getInstance(document.getElementById('addBranchProductModal')).hide();
                document.getElementById('addBranchProductForm').reset();
            } else {
                const err = await response.json();
                throw new Error(err.detail || 'Error al agregar producto a sucursal');
            }
        } catch (e) {
            Utils.showAlert('branchFormMsg', e.message, 'danger');
        }
    },

    deleteBranchProduct: async (id) => {
        if (!AuthManager.checkAuth()) return;
        if (!confirm('¿Está seguro de eliminar este producto de la sucursal?')) return;
        try {
            const response = await fetch(`${selectedBranch}/products/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                Utils.showAlert('branchFormMsg', 'Producto eliminado de sucursal', 'success');
                BranchManager.fetchBranchInventory();
            } else {
                throw new Error('Error al eliminar producto de sucursal');
            }
        } catch (e) {
            Utils.showAlert('branchFormMsg', e.message, 'danger');
        }
    }
};

// Gestor de Ventas y Notificaciones
const SalesManager = {
    fetchSales: async () => {
        try {
            // Ahora obtenemos TODAS las ventas para el historial
            const response = await fetch(`${CONFIG.centralAPI}/sales`);
            if (response.ok) {
                salesData = await response.json();
                // Si no hay filtros activos, los datos filtrados son iguales a los originales
                if (!isSalesFiltered) {
                    filteredSalesData = [...salesData];
                } else {
                    SalesManager.applyFilters();
                }
                SalesManager.renderSales();
                SalesManager.renderNotifications(salesData); // Las notificaciones siempre muestran lo más reciente
                SalesManager.updateBranchFilterOptions();
            }
        } catch (e) {
            console.error('Error fetching sales', e);
        }
    },

    updateBranchFilterOptions: () => {
        const select = document.getElementById('salesBranchFilter');
        if (!select) return;
        
        const branches = [...new Set(salesData.map(s => s.branch_id))];
        const currentValue = select.value;
        
        // Mantener la opción "Todas"
        let options = '<option value="">Todas las Sucursales</option>';
        branches.forEach(branch => {
            options += `<option value="${branch}" ${branch === currentValue ? 'selected' : ''}>${branch}</option>`;
        });
        select.innerHTML = options;
    },

    applyFilters: () => {
        const searchId = document.getElementById('salesSearch').value.toLowerCase();
        const branch = document.getElementById('salesBranchFilter').value;
        const date = document.getElementById('salesDateFilter').value;

        filteredSalesData = salesData.filter(sale => {
            const matchId = !searchId || sale.product_id.toString().includes(searchId);
            const matchBranch = !branch || sale.branch_id === branch;
            const matchDate = !date || sale.timestamp.startsWith(date);
            return matchId && matchBranch && matchDate;
        });

        isSalesFiltered = true;
        salesCurrentPage = 1; // Resetear a primera página al filtrar
        SalesManager.renderSales();
    },

    clearFilters: () => {
        document.getElementById('salesSearch').value = '';
        document.getElementById('salesBranchFilter').value = '';
        document.getElementById('salesDateFilter').value = '';
        isSalesFiltered = false;
        filteredSalesData = [...salesData];
        salesCurrentPage = 1;
        SalesManager.renderSales();
    },

    renderSales: () => {
        const tbody = document.getElementById('salesBody');
        if (!tbody) return;
        
        const dataToShow = filteredSalesData;

        if (dataToShow.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No hay ventas registradas</td></tr>`;
            SalesPagination.updatePaginationInfo(0);
            return;
        }

        const startIndex = (salesCurrentPage - 1) * SALES_PER_PAGE;
        const paginatedData = dataToShow.slice(startIndex, startIndex + SALES_PER_PAGE);

        tbody.innerHTML = paginatedData.map(sale => `
            <tr>
                <td><span class="badge bg-secondary">${sale.branch_id}</span></td>
                <td><strong>${sale.product_id}</strong></td>
                <td><span class="badge bg-info text-dark">${sale.quantity_sold}</span></td>
                <td>${Utils.formatPrice(sale.sale_price)}</td>
                <td class="small">${Utils.formatDate(sale.timestamp)}</td>
            </tr>
        `).join('');

        SalesPagination.updatePaginationInfo(dataToShow.length);
    },

    renderNotifications: (sales) => {
        const container = document.querySelector('.notifications-body');
        if (!container) return;

        document.getElementById('totalNotifications').textContent = sales.length;

        if (sales.length === 0) {
            container.innerHTML = `<div class="no-notifications">No hay notificaciones</div>`;
            return;
        }

        // Mostrar solo las 3 más recientes en el feed de actividad
        container.innerHTML = sales.slice(0, 3).map(sale => `
            <div class="notification-item">
                <div class="notification-icon"><i class="bi bi-cart-check text-success"></i></div>
                <div class="notification-content">
                    <div class="notification-title">Venta en ${sale.branch_id}</div>
                    <div class="notification-details">Producto ${sale.product_id} - Cant: ${sale.quantity_sold}</div>
                    <div class="notification-time">${Utils.formatDate(sale.timestamp)}</div>
                </div>
            </div>
        `).join('');
    }
};

// Gestor de Estadísticas
const StatsManager = {
    updateStats: () => {
        const totalProducts = inventoryData.length;
        const totalStock = inventoryData.reduce((sum, p) => sum + p.stock, 0);
        const totalValue = inventoryData.reduce((sum, p) => sum + ((p.precio||p.price) * p.stock), 0);

        if(document.getElementById('totalProducts')) 
            document.getElementById('totalProducts').textContent = totalProducts;
        if(document.getElementById('totalStock')) 
            document.getElementById('totalStock').textContent = totalStock;
        if(document.getElementById('totalValue')) 
            document.getElementById('totalValue').textContent = Utils.formatPrice(totalValue);
    }
};

// Paginación
const CentralPagination = {
    updatePaginationInfo: (total) => {
        const info = document.getElementById('centralPaginationInfo');
        if(info) info.textContent = `Total: ${total} productos`;
    },
    previousPage: () => {
        if(centralCurrentPage > 1) { centralCurrentPage--; InventoryManager.renderInventory(); }
    },
    nextPage: () => {
        const total = isCentralFiltered ? filteredCentralData.length : inventoryData.length;
        if(centralCurrentPage * ITEMS_PER_PAGE < total) { centralCurrentPage++; InventoryManager.renderInventory(); }
    }
};

const BranchPagination = {
    updatePaginationInfo: (total) => {
        const info = document.getElementById('branchPaginationInfo');
        if(info) info.textContent = `Total: ${total} productos`;
    },
    previousPage: () => {
        if(branchCurrentPage > 1) { branchCurrentPage--; BranchManager.renderBranchInventory(); }
    },
    nextPage: () => {
        const total = isBranchFiltered ? filteredBranchData.length : branchInventoryData.length;
        if(branchCurrentPage * ITEMS_PER_PAGE < total) { branchCurrentPage++; BranchManager.renderBranchInventory(); }
    }
};

const SalesPagination = {
    updatePaginationInfo: (total) => {
        const info = document.getElementById('salesPaginationInfo');
        if(info) info.textContent = `Total: ${total} ventas`;
    },
    previousPage: () => {
        if(salesCurrentPage > 1) { salesCurrentPage--; SalesManager.renderSales(); }
    },
    nextPage: () => {
        const total = filteredSalesData.length;
        if(salesCurrentPage * SALES_PER_PAGE < total) { salesCurrentPage++; SalesManager.renderSales(); }
    }
};

// Gestor de Formularios
const FormManager = {
    resetForm: () => {
        document.getElementById('productForm').reset();
    },
    getFormData: () => {
        return {
            id: parseInt(document.getElementById('productId').value),
            name: document.getElementById('productName').value,
            price: parseFloat(document.getElementById('productPrice').value),
            stock: parseInt(document.getElementById('productStock').value)
        };
    },
    getCentralModalData: () => {
        return {
            id: parseInt(document.getElementById('centralProductId').value),
            name: document.getElementById('centralProductName').value,
            price: parseFloat(document.getElementById('centralProductPrice').value),
            stock: parseInt(document.getElementById('centralProductStock').value)
        };
    },
    getBranchModalData: () => {
        return {
            id: parseInt(document.getElementById('branchProductId').value),
            stock: parseInt(document.getElementById('branchNewStock') ? document.getElementById('branchNewStock').value : document.getElementById('branchProductStock').value),
            price: parseFloat(document.getElementById('branchProductPrice').value)
        };
    }
};

// Inicialización
const DashboardApp = {
    init: async () => {
        console.log('Dashboard Master JS Initialized');
        AuthManager.updateUI();
        
        // Event Listeners
        document.getElementById('loginForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            AuthManager.login(
                document.getElementById('loginUsername').value,
                document.getElementById('loginPassword').value
            );
        });

        document.getElementById('btnLogout')?.addEventListener('click', AuthManager.logout);

        document.getElementById('productForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            InventoryManager.addProduct(FormManager.getFormData());
        });

        document.getElementById('editCentralForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            InventoryManager.updateProduct(
                document.getElementById('centralProductId').value,
                FormManager.getCentralModalData()
            );
        });

        document.getElementById('editBranchForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            BranchManager.updateBranchProduct(
                document.getElementById('branchProductId').value,
                FormManager.getBranchModalData()
            );
        });

        document.getElementById('addBranchProductForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const data = {
                id: parseInt(document.getElementById('newBranchProductId').value),
                name: document.getElementById('newBranchProductName').value,
                price: parseFloat(document.getElementById('newBranchProductPrice').value),
                stock: parseInt(document.getElementById('newBranchProductStock').value),
                category: document.getElementById('newBranchProductCategory').value
            };
            BranchManager.addBranchProduct(data);
        });

        document.getElementById('branchSelect')?.addEventListener('change', (e) => {
            selectedBranch = e.target.value;
            BranchManager.fetchBranchInventory();
        });

        // Sales Filters
        document.getElementById('salesSearch')?.addEventListener('input', SalesManager.applyFilters);
        document.getElementById('salesBranchFilter')?.addEventListener('change', SalesManager.applyFilters);
        document.getElementById('salesDateFilter')?.addEventListener('change', SalesManager.applyFilters);

        // Initial Load
        DashboardApp.refresh();
        
        // Auto Update
        setInterval(DashboardApp.refresh, CONFIG.updateInterval);
    },

    refresh: () => {
        InventoryManager.fetchInventory();
        BranchManager.fetchBranchInventory();
        SalesManager.fetchSales();
    }
};

// Expose to window for HTML onclick events
window.InventoryManager = InventoryManager;
window.BranchManager = BranchManager;
window.AuthManager = AuthManager;
window.CentralPagination = CentralPagination;
window.BranchPagination = BranchPagination;
window.DashboardApp = DashboardApp;

document.addEventListener('DOMContentLoaded', DashboardApp.init);