/**
 * Admin Appointments Management
 * Extraído do React admin/Appointments.tsx
 */

let appointments = [];
let filteredAppointments = [];
let currentFilter = 'all';
let searchTerm = '';

document.addEventListener('DOMContentLoaded', async () => {
    await loadAppointments();
    setupSearch();
});

function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value.toLowerCase();
        filterAndRender();
    });
}

async function loadAppointments() {
    showLoading();
    try {
        const response = await fetchAPI('/api/admin/agendamentos/');
        if (!response.ok) throw new Error('Erro ao carregar');
        
        appointments = await response.json();
        filterAndRender();
    } catch (error) {
        console.error(error);
        showError();
    } finally {
        hideLoading();
    }
}

function setStatusFilter(status) {
    currentFilter = status;
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.classList.toggle('active', chip.dataset.status === status);
    });
    filterAndRender();
}

function filterAndRender() {
    filteredAppointments = appointments.filter(apt => {
        const matchesStatus = currentFilter === 'all' || apt.status === currentFilter;
        const matchesSearch = !searchTerm || 
            apt.customer_name?.toLowerCase().includes(searchTerm) ||
            apt.customer_phone?.includes(searchTerm);
        return matchesStatus && matchesSearch;
    });
    
    renderTable();
}

function renderTable() {
    const tbody = document.getElementById('appointmentsBody');
    const table = document.getElementById('appointmentsTable');
    const empty = document.getElementById('emptyState');
    
    if (filteredAppointments.length === 0) {
        table.style.display = 'none';
        empty.style.display = 'block';
        return;
    }
    
    table.style.display = 'block';
    empty.style.display = 'none';
    
    tbody.innerHTML = filteredAppointments.map(apt => `
        <tr>
            <td>${formatDate(apt.date)} ${apt.time}</td>
            <td>${apt.customer_name}</td>
            <td>${apt.service}</td>
            <td>${apt.barber}</td>
            <td>R$ ${apt.price.toFixed(2)}</td>
            <td><span class="status-badge ${apt.status}">${getStatusLabel(apt.status)}</span></td>
            <td>
                <button class="btn-sm btn-outline" onclick="viewDetails(${apt.id})">Ver</button>
                <button class="btn-sm btn-primary" onclick="openStatusModal(${apt.id})">Status</button>
            </td>
        </tr>
    `).join('');
}

function getStatusLabel(status) {
    const labels = { pending: 'Pendente', confirmed: 'Confirmado', completed: 'Concluído', cancelled: 'Cancelado' };
    return labels[status] || status;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

function showLoading() {
    document.getElementById('loadingState').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function showError() {
    document.getElementById('emptyState').innerHTML = '<span class="empty-icon">⚠️</span><h3>Erro ao carregar</h3>';
    document.getElementById('emptyState').style.display = 'block';
}

function viewDetails(id) {
    const apt = appointments.find(a => a.id === id);
    document.getElementById('appointmentDetails').innerHTML = `
        <div class="details-grid">
            <div><strong>Cliente:</strong> ${apt.customer_name}</div>
            <div><strong>Telefone:</strong> ${apt.customer_phone}</div>
            <div><strong>Serviço:</strong> ${apt.service}</div>
            <div><strong>Barbeiro:</strong> ${apt.barber}</div>
            <div><strong>Data:</strong> ${formatDate(apt.date)}</div>
            <div><strong>Horário:</strong> ${apt.time}</div>
            <div><strong>Valor:</strong> R$ ${apt.price.toFixed(2)}</div>
            <div><strong>Pagamento:</strong> ${apt.payment_method}</div>
        </div>
    `;
    document.getElementById('detailsModal').style.display = 'flex';
}

function closeDetailsModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

function openStatusModal(id) {
    document.getElementById('statusAppointmentId').value = id;
    const apt = appointments.find(a => a.id === id);
    document.getElementById('newStatus').value = apt.status;
    document.getElementById('statusModal').style.display = 'flex';
}

function closeStatusModal() {
    document.getElementById('statusModal').style.display = 'none';
}

async function updateStatus() {
    const id = document.getElementById('statusAppointmentId').value;
    const newStatus = document.getElementById('newStatus').value;
    const reason = document.getElementById('cancelReason').value;
    
    try {
        const response = await fetchAPI(`/api/admin/update-agendamento-status/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify({ status: newStatus, reason })
        });
        
        if (!response.ok) throw new Error('Erro ao atualizar');
        
        showToast('Sucesso', 'Status atualizado', 'success');
        closeStatusModal();
        await loadAppointments();
    } catch (error) {
        showToast('Erro', 'Não foi possível atualizar o status', 'error');
    }
}

function exportAppointments() {
    showToast('Exportando', 'Preparando relatório...', 'info');
    // TODO: Implement export
}

window.setStatusFilter = setStatusFilter;
window.viewDetails = viewDetails;
window.closeDetailsModal = closeDetailsModal;
window.openStatusModal = openStatusModal;
window.closeStatusModal = closeStatusModal;
window.updateStatus = updateStatus;
window.exportAppointments = exportAppointments;

