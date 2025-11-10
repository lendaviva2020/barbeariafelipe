/**
 * Admin Barbers Management - Extraído de admin/Barbers.tsx
 */

let barbers = [];
let currentTab = 'all';

document.addEventListener('DOMContentLoaded', async () => {
    await loadBarbers();
});

async function loadBarbers() {
    try {
        const response = await fetchAPI('/api/barbeiros/');
        barbers = await response.json();
        updateStats();
        renderBarbers();
    } catch (error) {
        console.error('Erro ao carregar barbeiros:', error);
    }
}

function updateStats() {
    const total = barbers.length;
    const active = barbers.filter(b => b.active).length;
    const avgRating = 4.8; // Mock - seria calculado de reviews
    
    document.getElementById('totalBarbers').textContent = total;
    document.getElementById('activeBarbers').textContent = active;
    document.getElementById('avgRating').textContent = avgRating.toFixed(1);
}

function setTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    renderBarbers();
}

function renderBarbers() {
    const filtered = currentTab === 'all' ? barbers :
                    currentTab === 'active' ? barbers.filter(b => b.active) :
                    barbers.filter(b => !b.active);
    
    const grid = document.getElementById('barbersGrid');
    grid.innerHTML = filtered.map(barber => `
        <div class="barber-card ${!barber.active ? 'inactive' : ''}">
            <div class="barber-avatar">${barber.name.split(' ').map(n => n[0]).join('').slice(0,2)}</div>
            <h3>${barber.name}</h3>
            <p class="barber-specialty">${barber.specialty || 'Barbeiro'}</p>
            <div class="barber-actions">
                <button class="btn-sm btn-outline" onclick="editBarber(${barber.id})">✏️ Editar</button>
                <button class="btn-sm btn-danger" onclick="deleteBarber(${barber.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function openBarberDialog() {
    document.getElementById('barberModalTitle').textContent = 'Novo Barbeiro';
    document.getElementById('barberDialog').style.display = 'flex';
}

function closeBarberDialog() {
    document.getElementById('barberDialog').style.display = 'none';
}

async function submitBarber() {
    const data = {
        name: document.getElementById('barberName').value,
        email: document.getElementById('barberEmail').value,
        phone: document.getElementById('barberPhone').value,
        specialty: document.getElementById('barberSpecialty').value,
        bio: document.getElementById('barberBio').value,
        active: document.getElementById('barberActive').checked
    };
    
    try {
        await fetchAPI('/api/barbeiros/admin/create/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showToast('Sucesso', 'Barbeiro criado', 'success');
        closeBarberDialog();
        loadBarbers();
    } catch (error) {
        showToast('Erro', 'Não foi possível criar o barbeiro', 'error');
    }
}

function editBarber(id) {
    const barber = barbers.find(b => b.id === id);
    document.getElementById('barberId').value = barber.id;
    document.getElementById('barberName').value = barber.name;
    document.getElementById('barberEmail').value = barber.email || '';
    document.getElementById('barberPhone').value = barber.phone || '';
    document.getElementById('barberSpecialty').value = barber.specialty || '';
    document.getElementById('barberBio').value = barber.bio || '';
    document.getElementById('barberActive').checked = barber.active;
    document.getElementById('barberModalTitle').textContent = 'Editar Barbeiro';
    document.getElementById('barberDialog').style.display = 'flex';
}

async function deleteBarber(id) {
    if (!confirm('Excluir este barbeiro?')) return;
    
    try {
        await fetchAPI(`/api/barbeiros/admin/${id}/delete/`, { method: 'DELETE' });
        showToast('Sucesso', 'Barbeiro excluído', 'success');
        loadBarbers();
    } catch (error) {
        showToast('Erro', 'Não foi possível excluir', 'error');
    }
}

window.openBarberDialog = openBarberDialog;
window.closeBarberDialog = closeBarberDialog;
window.submitBarber = submitBarber;
window.editBarber = editBarber;
window.deleteBarber = deleteBarber;
window.setTab = setTab;

