/**
 * Suppliers Management
 */

let suppliers = [];

document.addEventListener('DOMContentLoaded', loadSuppliers);

async function loadSuppliers() {
    try {
        const response = await fetchAPI('/api/suppliers/');
        suppliers = await response.json();
        renderSuppliers();
    } catch (error) {
        console.error(error);
    }
}

function renderSuppliers() {
    const grid = document.getElementById('suppliersGrid');
    grid.innerHTML = suppliers.map(supplier => `
        <div class="supplier-card">
            <div class="supplier-icon">🏢</div>
            <h3>${supplier.name}</h3>
            <p class="supplier-company">${supplier.company_name || ''}</p>
            <div class="supplier-contacts">
                <p>📞 ${supplier.phone}</p>
                <p>📧 ${supplier.email}</p>
            </div>
            <div class="supplier-actions">
                <button class="btn-sm btn-outline" onclick="editSupplier(${supplier.id})">✏️</button>
                <button class="btn-sm btn-danger" onclick="deleteSupplier(${supplier.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function openSupplierDialog() {
    document.getElementById('supplierDialog').style.display = 'flex';
}

function closeSupplierDialog() {
    document.getElementById('supplierDialog').style.display = 'none';
}

function editSupplier(id) {
    openSupplierDialog();
}

async function submitSupplier() {
    const data = {
        name: document.getElementById('supplierName').value,
        company_name: document.getElementById('supplierCompany').value,
        cnpj: document.getElementById('supplierCnpj').value,
        phone: document.getElementById('supplierPhone').value,
        email: document.getElementById('supplierEmail').value,
        address: document.getElementById('supplierAddress').value,
        payment_terms: document.getElementById('supplierPaymentTerms').value
    };
    
    try {
        await fetchAPI('/api/suppliers/create/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showToast('Sucesso', 'Fornecedor criado', 'success');
        closeSupplierDialog();
        loadSuppliers();
    } catch (error) {
        showToast('Erro', 'Não foi possível criar', 'error');
    }
}

async function deleteSupplier(id) {
    if (!confirm('Excluir fornecedor?')) return;
    
    try {
        await fetchAPI(`/api/suppliers/${id}/delete/`, { method: 'DELETE' });
        showToast('Sucesso', 'Fornecedor excluído', 'success');
        loadSuppliers();
    } catch (error) {
        showToast('Erro', 'Não foi possível excluir', 'error');
    }
}

window.openSupplierDialog = openSupplierDialog;
window.closeSupplierDialog = closeSupplierDialog;
window.editSupplier = editSupplier;
window.submitSupplier = submitSupplier;
window.deleteSupplier = deleteSupplier;

