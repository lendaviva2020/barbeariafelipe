/**
 * Inventory System - CRUD Produtos
 */

let products = [];
let currentCategory = 'all';

document.addEventListener('DOMContentLoaded', loadProducts);

async function loadProducts() {
    try {
        const response = await fetchAPI('/api/products/');
        products = await response.json();
        checkLowStock();
        renderProducts();
    } catch (error) {
        console.error(error);
    }
}

function checkLowStock() {
    const lowStock = products.filter(p => p.stock_quantity <= p.min_stock_level);
    const alert = document.getElementById('lowStockAlert');
    
    if (lowStock.length > 0) {
        alert.style.display = 'flex';
        document.getElementById('lowStockCount').textContent = lowStock.length;
    } else {
        alert.style.display = 'none';
    }
}

function setCategory(category) {
    currentCategory = category;
    document.querySelectorAll('[data-category]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === category);
    });
    renderProducts();
}

function renderProducts() {
    const filtered = currentCategory === 'all' ? products : products.filter(p => p.category === currentCategory);
    const grid = document.getElementById('productsGrid');
    
    grid.innerHTML = filtered.map(product => `
        <div class="product-card ${product.stock_quantity <= product.min_stock_level ? 'low-stock' : ''}">
            <div class="product-header">
                <h3>${product.name}</h3>
                ${product.stock_quantity <= product.min_stock_level ? '<span class="badge badge-danger">⚠️ Estoque Baixo</span>' : ''}
            </div>
            <p class="product-brand">${product.brand || ''}</p>
            <p class="product-sku">SKU: ${product.sku}</p>
            <div class="product-prices">
                <div>
                    <span class="label">Custo:</span>
                    <span class="value">R$ ${product.cost_price.toFixed(2)}</span>
                </div>
                <div>
                    <span class="label">Venda:</span>
                    <span class="value price">R$ ${product.selling_price.toFixed(2)}</span>
                </div>
            </div>
            <div class="product-stock">
                <span>Estoque: <strong>${product.stock_quantity}</strong> unidades</span>
                <span class="stock-min">(mín: ${product.min_stock_level})</span>
            </div>
            <div class="product-actions">
                <button class="btn-sm btn-outline" onclick="editProduct(${product.id})">✏️</button>
                <button class="btn-sm btn-danger" onclick="deleteProduct(${product.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function openProductDialog() {
    document.getElementById('productDialog').style.display = 'flex';
}

function closeProductDialog() {
    document.getElementById('productDialog').style.display = 'none';
}

function editProduct(id) {
    const product = products.find(p => p.id === id);
    // Populate form...
    openProductDialog();
}

async function submitProduct() {
    const data = {
        name: document.getElementById('productName').value,
        sku: document.getElementById('productSku').value,
        category: document.getElementById('productCategory').value,
        description: document.getElementById('productDescription').value,
        brand: document.getElementById('productBrand').value,
        cost_price: document.getElementById('productCost').value,
        selling_price: document.getElementById('productPrice').value,
        stock_quantity: document.getElementById('productStock').value,
        min_stock_level: document.getElementById('productMinStock').value,
        active: document.getElementById('productActive').checked
    };
    
    try {
        await fetchAPI('/api/products/create/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showToast('Sucesso', 'Produto criado', 'success');
        closeProductDialog();
        loadProducts();
    } catch (error) {
        showToast('Erro', 'Não foi possível criar o produto', 'error');
    }
}

async function deleteProduct(id) {
    if (!confirm('Excluir produto?')) return;
    
    try {
        await fetchAPI(`/api/products/${id}/delete/`, { method: 'DELETE' });
        showToast('Sucesso', 'Produto excluído', 'success');
        loadProducts();
    } catch (error) {
        showToast('Erro', 'Não foi possível excluir', 'error');
    }
}

window.setCategory = setCategory;
window.openProductDialog = openProductDialog;
window.closeProductDialog = closeProductDialog;
window.editProduct = editProduct;
window.submitProduct = submitProduct;
window.deleteProduct = deleteProduct;

