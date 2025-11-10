/**
 * Admin Users Management
 */

let users = [];
let currentRole = 'all';

document.addEventListener('DOMContentLoaded', loadUsers);

async function loadUsers() {
    try {
        const response = await fetchAPI('/api/admin/users/');
        users = await response.json();
        renderUsers();
    } catch (error) {
        console.error(error);
    }
}

function setRoleFilter(role) {
    currentRole = role;
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.role === role);
    });
    renderUsers();
}

function renderUsers() {
    const filtered = currentRole === 'all' ? users : users.filter(u => u.role === currentRole);
    const tbody = document.getElementById('usersBody');
    
    tbody.innerHTML = filtered.map(user => `
        <tr>
            <td>
                <div class="user-cell">
                    <div class="user-avatar">${(user.name || user.email)[0].toUpperCase()}</div>
                    <span>${user.name || 'Sem nome'}</span>
                </div>
            </td>
            <td>${user.email}</td>
            <td>${user.phone || '-'}</td>
            <td><span class="role-badge role-${user.role}">${getRoleLabel(user.role)}</span></td>
            <td><span class="status-badge ${user.is_active ? 'active' : 'inactive'}">${user.is_active ? 'Ativo' : 'Inativo'}</span></td>
            <td>${formatDate(user.created_at)}</td>
            <td>
                <button class="btn-sm btn-outline" onclick="viewUserDetails(${user.id})">Ver</button>
            </td>
        </tr>
    `).join('');
}

function getRoleLabel(role) {
    const labels = { admin: 'Admin', barber: 'Barbeiro', user: 'Cliente' };
    return labels[role] || role;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

function viewUserDetails(id) {
    const user = users.find(u => u.id === id);
    const content = document.getElementById('userDetailsContent');
    content.innerHTML = `
        <div class="details-grid">
            <div><strong>Nome:</strong> ${user.name}</div>
            <div><strong>Email:</strong> ${user.email}</div>
            <div><strong>Telefone:</strong> ${user.phone || '-'}</div>
            <div><strong>Role:</strong> ${getRoleLabel(user.role)}</div>
            <div><strong>Cadastrado:</strong> ${formatDate(user.created_at)}</div>
            <div><strong>Status:</strong> ${user.is_active ? 'Ativo' : 'Inativo'}</div>
        </div>
    `;
    document.getElementById('userDetailsModal').style.display = 'flex';
}

function closeUserDetails() {
    document.getElementById('userDetailsModal').style.display = 'none';
}

window.setRoleFilter = setRoleFilter;
window.viewUserDetails = viewUserDetails;
window.closeUserDetails = closeUserDetails;

