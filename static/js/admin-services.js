/**
 * Admin Services - CRUD completo
 */

let services = [];
let editingService = null;

document.addEventListener('DOMContentLoaded', loadServices);

async function loadServices() {
    try {
        const response = await fetchAPI('/api/servicos/');
        services = await response.json();
        renderServices();
    } catch (error) {
        console.error(error);
    }
}

function renderServices() {
    const grid = document.getElementById('servicesGrid');
    grid.innerHTML = services.map(service => `
        <div class="service-card ${!service.active ? 'inactive' : ''}">
            <div class="service-header">
                <h3>${service.name}</h3>
                <span class="badge ${service.active ? 'badge-success' : 'badge-muted'}">
                    ${service.active ? 'Ativo' : 'Inativo'}
                </span>
            </div>
            <p class="service-description">${service.description || ''}</p>
            <div class="service-details">
                <span>💰 R$ ${service.price.toFixed(2)}</span>
                <span>⏱️ ${service.duration} min</span>
            </div>
            <div class="service-actions">
                <button class="btn-sm btn-outline" onclick="editService(${service.id})">✏️</button>
                <button class="btn-sm btn-danger" onclick="deleteService(${service.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function openServiceDialog() {
    editingService = null;
    document.getElementById('serviceModalTitle').textContent = 'Novo Serviço';
    document.querySelector('#serviceDialog form').reset();
    document.getElementById('serviceDialog').style.display = 'flex';
}

function closeServiceDialog() {
    document.getElementById('serviceDialog').style.display = 'none';
}

function editService(id) {
    const service = services.find(s => s.id === id);
    editingService = service;
    document.getElementById('serviceId').value = service.id;
    document.getElementById('serviceName').value = service.name;
    document.getElementById('serviceDescription').value = service.description || '';
    document.getElementById('servicePrice').value = service.price;
    document.getElementById('serviceDuration').value = service.duration;
    document.getElementById('serviceCategory').value = service.category || 'haircut';
    document.getElementById('serviceActive').checked = service.active;
    document.getElementById('serviceModalTitle').textContent = 'Editar Serviço';
    document.getElementById('serviceDialog').style.display = 'flex';
}

async function submitService() {
    const data = {
        name: document.getElementById('serviceName').value,
        description: document.getElementById('serviceDescription').value,
        price: parseFloat(document.getElementById('servicePrice').value),
        duration: parseInt(document.getElementById('serviceDuration').value),
        category: document.getElementById('serviceCategory').value,
        active: document.getElementById('serviceActive').checked
    };
    
    try {
        const url = editingService 
            ? `/api/servicos/admin/${editingService.id}/`
            : '/api/servicos/admin/create/';
        const method = editingService ? 'PUT' : 'POST';
        
        await fetchAPI(url, { method, body: JSON.stringify(data) });
        showToast('Sucesso', 'Serviço salvo', 'success');
        closeServiceDialog();
        loadServices();
    } catch (error) {
        showToast('Erro', 'Não foi possível salvar', 'error');
    }
}

async function deleteService(id) {
    if (!confirm('Excluir serviço?')) return;
    
    try {
        await fetchAPI(`/api/servicos/admin/${id}/delete/`, { method: 'DELETE' });
        showToast('Sucesso', 'Serviço excluído', 'success');
        loadServices();
    } catch (error) {
        showToast('Erro', 'Não foi possível excluir', 'error');
    }
}

function filterServices() {
    renderServices(); // Simplificado - filtro seria aplicado aqui
}

window.openServiceDialog = openServiceDialog;
window.closeServiceDialog = closeServiceDialog;
window.submitService = submitService;
window.editService = editService;
window.deleteService = deleteService;
window.filterServices = filterServices;

