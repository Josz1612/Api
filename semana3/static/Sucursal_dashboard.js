// Configuración
const API_BASE_URL = 'http://localhost:8001';

// Estado local
let currentInventory = [];

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    loadInventory();
    loadSalesHistory();
    startClock();

    // Event Listeners
    document.getElementById('productSelect').addEventListener('change', updateSaleTotal);
    document.getElementById('quantityInput').addEventListener('input', updateSaleTotal);
    document.getElementById('saleForm').addEventListener('submit', processSale);
});

// Reloj
function startClock() {
    setInterval(() => {
        const now = new Date();
        document.getElementById('clock').textContent = now.toLocaleTimeString();
    }, 1000);
}

// Cargar Inventario
async function loadInventory() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory`);
        if (response.ok) {
            currentInventory = await response.json();
            renderInventoryTable(currentInventory);
            updateProductSelect(currentInventory);
            updateStats(currentInventory);
        }
    } catch (error) {
        console.error('Error cargando inventario:', error);
    }
}

// Renderizar Tabla de Inventario
function renderInventoryTable(products) {
    const tbody = document.getElementById('inventoryTableBody');
    tbody.innerHTML = products.map(p => `
        <tr>
            <td><strong>${p.id}</strong></td>
            <td>${p.name}</td>
            <td>$${p.price.toFixed(2)}</td>
            <td>
                <span class="badge ${p.stock > 5 ? 'bg-success' : p.stock > 0 ? 'bg-warning' : 'bg-danger'}">
                    ${p.stock}
                </span>
            </td>
            <td>
                ${p.stock > 0 ? '<span class="text-success"><i class="bi bi-check-circle"></i> Disponible</span>' : '<span class="text-danger"><i class="bi bi-x-circle"></i> Agotado</span>'}
            </td>
        </tr>
    `).join('');
}

// Actualizar Select de Productos
function updateProductSelect(products) {
    const select = document.getElementById('productSelect');
    const currentVal = select.value;
    
    // Guardar selección actual si existe
    select.innerHTML = '<option value="" selected disabled>Elija un producto...</option>' + 
        products.map(p => `
            <option value="${p.id}" data-price="${p.price}" data-stock="${p.stock}" ${p.stock === 0 ? 'disabled' : ''}>
                ${p.name} - $${p.price.toFixed(2)} (Stock: ${p.stock})
            </option>
        `).join('');
    
    if (currentVal) select.value = currentVal;
}

// Actualizar Total de Venta
function updateSaleTotal() {
    const select = document.getElementById('productSelect');
    const quantityInput = document.getElementById('quantityInput');
    const totalDisplay = document.getElementById('saleTotal');
    
    const option = select.options[select.selectedIndex];
    if (!option || !option.value) {
        totalDisplay.textContent = '$0.00';
        return;
    }

    const price = parseFloat(option.dataset.price);
    const stock = parseInt(option.dataset.stock);
    let quantity = parseInt(quantityInput.value);

    // Validar stock
    if (quantity > stock) {
        quantityInput.value = stock;
        quantity = stock;
    }
    if (quantity < 1) {
        quantityInput.value = 1;
        quantity = 1;
    }

    const total = price * quantity;
    totalDisplay.textContent = `$${total.toFixed(2)}`;
}

// Procesar Venta
async function processSale(e) {
    e.preventDefault();
    
    const productId = parseInt(document.getElementById('productSelect').value);
    const quantity = parseInt(document.getElementById('quantityInput').value);
    const messageDiv = document.getElementById('saleMessage');

    if (!productId || quantity < 1) return;

    try {
        const response = await fetch(`${API_BASE_URL}/sales`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        if (response.ok) {
            const sale = await response.json();
            
            // Éxito
            messageDiv.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show">
                    <i class="bi bi-check-circle-fill me-2"></i>
                    Venta procesada: <strong>$${sale.total_amount.toFixed(2)}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Resetear formulario
            document.getElementById('saleForm').reset();
            document.getElementById('saleTotal').textContent = '$0.00';
            
            // Recargar datos
            loadInventory();
            loadSalesHistory();
            
        } else {
            const error = await response.json();
            messageDiv.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Error: ${error.detail}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error procesando venta:', error);
        messageDiv.innerHTML = `
            <div class="alert alert-danger">Error de conexión</div>
        `;
    }
}

// Cargar Historial de Ventas
async function loadSalesHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/sales`);
        if (response.ok) {
            const sales = await response.json();
            renderSalesTable(sales.reverse().slice(0, 10)); // Últimas 10
            
            // Actualizar stats globales
            document.getElementById('totalSales').textContent = sales.length;
            const totalRevenue = sales.reduce((sum, s) => sum + s.total_amount, 0);
            document.getElementById('totalRevenue').textContent = `$${totalRevenue.toFixed(2)}`;
        }
    } catch (error) {
        console.error('Error cargando ventas:', error);
    }
}

function renderSalesTable(sales) {
    const tbody = document.getElementById('salesTableBody');
    if (sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No hay ventas registradas</td></tr>';
        return;
    }
    
    tbody.innerHTML = sales.map(s => `
        <tr>
            <td><small class="text-muted">${s.sale_id.split('_')[1].substring(0,8)}...</small></td>
            <td>${s.product_name}</td>
            <td>${s.quantity_sold}</td>
            <td class="fw-bold text-primary">$${s.total_amount.toFixed(2)}</td>
            <td>${new Date(s.timestamp).toLocaleTimeString()}</td>
            <td><span class="badge bg-success">Completado</span></td>
        </tr>
    `).join('');
}

function updateStats(products) {
    document.getElementById('localProducts').textContent = products.length;
}