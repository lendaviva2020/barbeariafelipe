// Admin Dashboard JavaScript
let currentTab = 'dashboard';
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    // Verificar se é admin
    const user = auth.getUser();
    if (!user || user.role !== 'admin') {
        alert('Acesso negado. Você não tem permissão para acessar esta área.');
        window.location.href = '/';
        return;
    }
    
    setupAdminTabs();
    loadDashboardStats();
    setupRefreshButton();
});

// Setup das tabs
function setupAdminTabs() {
    const tabs = document.querySelectorAll('.admin-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    currentTab = tabName;
    
    // Atualizar tabs
    document.querySelectorAll('.admin-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
    });
    
    // Atualizar conteúdo
    document.querySelectorAll('.admin-tab-content').forEach(content => {
        content.classList.toggle('active', content.dataset.content === tabName);
    });
    
    // Carregar dados específicos da tab
    switch(tabName) {
        case 'dashboard':
            loadDashboardStats();
            break;
        case 'agendamentos':
            loadAppointments();
            setupFilters();
            break;
        case 'servicos':
            loadServices();
            break;
        case 'barbeiros':
            loadBarbers();
            break;
        case 'cupons':
            loadCoupons();
            setupCouponFilters();
            break;
    }
}

// Carregar estatísticas do dashboard
async function loadDashboardStats() {
    const timeRange = document.getElementById('timeRange')?.value || '30days';
    
    // Calcular datas
    const end = new Date();
    let start = new Date();
    
    switch(timeRange) {
        case '7days':
            start.setDate(end.getDate() - 7);
            break;
        case '30days':
            start.setDate(end.getDate() - 30);
            break;
        case '90days':
            start.setDate(end.getDate() - 90);
            break;
    }
    
    try {
        const response = await fetchAPI(
            `/admin/dashboard/stats/?start_date=${start.toISOString().split('T')[0]}&end_date=${end.toISOString().split('T')[0]}`
        );
        
        const stats = await response.json();
        
        // Atualizar métricas
        document.getElementById('stat_revenue').textContent = formatCurrency(stats.total_revenue);
        document.getElementById('stat_appointments').textContent = stats.total_appointments;
        document.getElementById('stat_completed').textContent = stats.completed_appointments;
        document.getElementById('stat_pending').textContent = stats.pending_appointments;
        document.getElementById('stat_barbers').textContent = stats.active_barbers;
        document.getElementById('stat_avg_ticket').textContent = formatCurrency(stats.average_ticket);
        
        // Atualizar hoje
        if (stats.today) {
            document.getElementById('today_completed').textContent = stats.today.completed;
            document.getElementById('today_pending').textContent = stats.today.pending;
            document.getElementById('today_cancelled').textContent = stats.today.cancelled;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Carregar agendamentos
async function loadAppointments(status = 'all') {
    const appointmentsList = document.getElementById('appointmentsList');
    appointmentsList.innerHTML = '<div class="loader-container"><div class="loader"></div><p>Carregando...</p></div>';
    
    try {
        const url = status === 'all' ? '/admin/agendamentos/' : `/admin/agendamentos/?status=${status}`;
        const response = await fetchAPI(url);
        const appointments = await response.json();
        
        appointmentsList.innerHTML = '';
        
        if (appointments.length === 0) {
            appointmentsList.innerHTML = '<div class="empty-state"><p>Nenhum agendamento encontrado</p></div>';
            return;
        }
        
        appointments.forEach(appointment => {
            const item = document.createElement('div');
            item.className = 'appointment-item';
            item.innerHTML = `
                <div class="appointment-info">
                    <div class="appointment-info-label">Cliente</div>
                    <div class="appointment-info-value">${appointment.customer_name}</div>
                </div>
                <div class="appointment-info">
                    <div class="appointment-info-label">Serviço</div>
                    <div class="appointment-info-value">${appointment.service}</div>
                </div>
                <div class="appointment-info">
                    <div class="appointment-info-label">Barbeiro</div>
                    <div class="appointment-info-value">${appointment.barber}</div>
                </div>
                <div class="appointment-info">
                    <div class="appointment-info-label">Data/Hora</div>
                    <div class="appointment-info-value">${formatDate(appointment.date)} ${appointment.time}</div>
                </div>
                <div class="appointment-info">
                    <div class="appointment-info-label">Status</div>
                    <span class="appointment-status ${appointment.status}">${getStatusLabel(appointment.status)}</span>
                </div>
                <div class="appointment-info">
                    <div class="appointment-info-label">Valor</div>
                    <div class="appointment-info-value">${formatCurrency(appointment.price)}</div>
                </div>
                <div class="appointment-actions">
                    ${appointment.status === 'pending' ? `
                        <button class="btn btn-sm btn-primary" onclick="updateStatus(${appointment.id}, 'confirmed')">Confirmar</button>
                        <button class="btn btn-sm btn-outline" onclick="updateStatus(${appointment.id}, 'cancelled')">Cancelar</button>
                    ` : ''}
                    ${appointment.status === 'confirmed' ? `
                        <button class="btn btn-sm btn-primary" onclick="updateStatus(${appointment.id}, 'completed')">Concluir</button>
                    ` : ''}
                </div>
            `;
            appointmentsList.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading appointments:', error);
        appointmentsList.innerHTML = '<div class="error-state"><p>Erro ao carregar agendamentos</p></div>';
    }
}

function getStatusLabel(status) {
    const labels = {
        'pending': 'Pendente',
        'confirmed': 'Confirmado',
        'completed': 'Concluído',
        'cancelled': 'Cancelado'
    };
    return labels[status] || status;
}

// Atualizar status
async function updateStatus(appointmentId, newStatus) {
    try {
        const response = await fetchAPI(`/admin/agendamentos/${appointmentId}/status/`, {
            method: 'PATCH',
            body: JSON.stringify({ status: newStatus }),
        });
        
        if (response.ok) {
            alert('Status atualizado com sucesso!');
            loadAppointments(currentFilter);
        } else {
            alert('Erro ao atualizar status');
        }
    } catch (error) {
        console.error('Error updating status:', error);
        alert('Erro ao atualizar status');
    }
}

// Setup dos filtros
function setupFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const status = btn.dataset.status;
            currentFilter = status;
            
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            loadAppointments(status);
        });
    });
}

// Setup botão de atualizar
function setupRefreshButton() {
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadDashboardStats);
    }
    
    const timeRange = document.getElementById('timeRange');
    if (timeRange) {
        timeRange.addEventListener('change', loadDashboardStats);
    }
}

// ========== SERVIÇOS ==========

async function loadServices() {
    const servicesList = document.getElementById('servicesList');
    servicesList.innerHTML = '<div class="loader-container"><div class="loader"></div><p>Carregando...</p></div>';
    
    try {
        const response = await fetchAPI('/admin/servicos/');
        const services = await response.json();
        
        servicesList.innerHTML = '';
        
        if (services.length === 0) {
            servicesList.innerHTML = '<div class="empty-state"><p>Nenhum serviço cadastrado</p></div>';
            return;
        }
        
        services.forEach(service => {
            const card = document.createElement('div');
            card.className = 'service-card';
            card.innerHTML = `
                <div class="service-card-header">
                    <h3>${service.name}</h3>
                    <span class="status-badge ${service.is_active ? 'active' : 'inactive'}">
                        ${service.is_active ? 'Ativo' : 'Inativo'}
                    </span>
                </div>
                <p class="service-description">${service.description || 'Sem descrição'}</p>
                <div class="service-info">
                    <div class="service-price">${formatCurrency(service.price)}</div>
                    <div class="service-duration">⏱️ ${service.duration} min</div>
                </div>
                <div class="service-actions">
                    <button class="btn btn-sm btn-outline" onclick='editService(${JSON.stringify(service)})'>✏️ Editar</button>
                    <button class="btn btn-sm btn-outline btn-danger" onclick="deleteService(${service.id})">🗑️ Excluir</button>
                </div>
            `;
            servicesList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading services:', error);
        servicesList.innerHTML = '<div class="error-state"><p>Erro ao carregar serviços</p></div>';
    }
}

function openServiceModal(service = null) {
    const modal = document.getElementById('serviceModal');
    const form = document.getElementById('serviceForm');
    const title = document.getElementById('serviceModalTitle');
    
    if (service) {
        title.textContent = 'Editar Serviço';
        document.getElementById('serviceId').value = service.id;
        document.getElementById('serviceName').value = service.name;
        document.getElementById('serviceDescription').value = service.description || '';
        document.getElementById('servicePrice').value = service.price;
        document.getElementById('serviceDuration').value = service.duration;
        document.getElementById('serviceActive').checked = service.is_active;
    } else {
        title.textContent = 'Novo Serviço';
        form.reset();
        document.getElementById('serviceId').value = '';
    }
    
    modal.style.display = 'flex';
}

function closeServiceModal() {
    document.getElementById('serviceModal').style.display = 'none';
    document.getElementById('serviceForm').reset();
}

function editService(service) {
    openServiceModal(service);
}

async function deleteService(serviceId) {
    if (!confirm('Tem certeza que deseja excluir este serviço?')) return;
    
    try {
        const response = await fetchAPI(`/admin/servicos/${serviceId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Serviço excluído com sucesso!');
            loadServices();
        } else {
            alert('Erro ao excluir serviço');
        }
    } catch (error) {
        console.error('Error deleting service:', error);
        alert('Erro ao excluir serviço');
    }
}

// Form submit para serviços
document.addEventListener('DOMContentLoaded', () => {
    const serviceForm = document.getElementById('serviceForm');
    if (serviceForm) {
        serviceForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const serviceId = document.getElementById('serviceId').value;
            const data = {
                name: document.getElementById('serviceName').value,
                description: document.getElementById('serviceDescription').value,
                price: parseFloat(document.getElementById('servicePrice').value),
                duration: parseInt(document.getElementById('serviceDuration').value),
                is_active: document.getElementById('serviceActive').checked
            };
            
            try {
                const url = serviceId ? `/admin/servicos/${serviceId}/` : '/admin/servicos/';
                const method = serviceId ? 'PUT' : 'POST';
                
                const response = await fetchAPI(url, {
                    method: method,
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Serviço salvo com sucesso!');
                    closeServiceModal();
                    loadServices();
                } else {
                    alert('Erro ao salvar serviço');
                }
            } catch (error) {
                console.error('Error saving service:', error);
                alert('Erro ao salvar serviço');
            }
        });
    }
});

// ========== BARBEIROS ==========

async function loadBarbers() {
    const barbersList = document.getElementById('barbersList');
    barbersList.innerHTML = '<div class="loader-container"><div class="loader"></div><p>Carregando...</p></div>';
    
    try {
        const response = await fetchAPI('/admin/barbeiros/');
        const barbers = await response.json();
        
        barbersList.innerHTML = '';
        
        if (barbers.length === 0) {
            barbersList.innerHTML = '<div class="empty-state"><p>Nenhum barbeiro cadastrado</p></div>';
            return;
        }
        
        barbers.forEach(barber => {
            const card = document.createElement('div');
            card.className = 'barber-card';
            card.innerHTML = `
                <div class="barber-card-header">
                    <div class="barber-avatar">${barber.name.charAt(0).toUpperCase()}</div>
                    <div class="barber-info-header">
                        <h3>${barber.name}</h3>
                        <span class="status-badge ${barber.is_active ? 'active' : 'inactive'}">
                            ${barber.is_active ? 'Ativo' : 'Inativo'}
                        </span>
                    </div>
                </div>
                <div class="barber-details">
                    <p>📧 ${barber.email}</p>
                    ${barber.phone ? `<p>📱 ${barber.phone}</p>` : ''}
                    ${barber.specialties ? `<p class="barber-specialties">⭐ ${barber.specialties}</p>` : ''}
                </div>
                <div class="barber-actions">
                    <button class="btn btn-sm btn-outline" onclick='editBarber(${JSON.stringify(barber)})'>✏️ Editar</button>
                    <button class="btn btn-sm btn-outline btn-danger" onclick="deleteBarber(${barber.id})">🗑️ Excluir</button>
                </div>
            `;
            barbersList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading barbers:', error);
        barbersList.innerHTML = '<div class="error-state"><p>Erro ao carregar barbeiros</p></div>';
    }
}

function openBarberModal(barber = null) {
    const modal = document.getElementById('barberModal');
    const form = document.getElementById('barberForm');
    const title = document.getElementById('barberModalTitle');
    
    if (barber) {
        title.textContent = 'Editar Barbeiro';
        document.getElementById('barberId').value = barber.id;
        document.getElementById('barberName').value = barber.name;
        document.getElementById('barberEmail').value = barber.email;
        document.getElementById('barberPhone').value = barber.phone || '';
        document.getElementById('barberSpecialties').value = barber.specialties || '';
        document.getElementById('barberActive').checked = barber.is_active;
    } else {
        title.textContent = 'Novo Barbeiro';
        form.reset();
        document.getElementById('barberId').value = '';
    }
    
    modal.style.display = 'flex';
}

function closeBarberModal() {
    document.getElementById('barberModal').style.display = 'none';
    document.getElementById('barberForm').reset();
}

function editBarber(barber) {
    openBarberModal(barber);
}

async function deleteBarber(barberId) {
    if (!confirm('Tem certeza que deseja excluir este barbeiro?')) return;
    
    try {
        const response = await fetchAPI(`/admin/barbeiros/${barberId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Barbeiro excluído com sucesso!');
            loadBarbers();
        } else {
            alert('Erro ao excluir barbeiro');
        }
    } catch (error) {
        console.error('Error deleting barber:', error);
        alert('Erro ao excluir barbeiro');
    }
}

// Form submit para barbeiros
document.addEventListener('DOMContentLoaded', () => {
    const barberForm = document.getElementById('barberForm');
    if (barberForm) {
        barberForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const barberId = document.getElementById('barberId').value;
            const data = {
                name: document.getElementById('barberName').value,
                email: document.getElementById('barberEmail').value,
                phone: document.getElementById('barberPhone').value,
                specialties: document.getElementById('barberSpecialties').value,
                is_active: document.getElementById('barberActive').checked
            };
            
            try {
                const url = barberId ? `/admin/barbeiros/${barberId}/` : '/admin/barbeiros/';
                const method = barberId ? 'PUT' : 'POST';
                
                const response = await fetchAPI(url, {
                    method: method,
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Barbeiro salvo com sucesso!');
                    closeBarberModal();
                    loadBarbers();
                } else {
                    alert('Erro ao salvar barbeiro');
                }
            } catch (error) {
                console.error('Error saving barber:', error);
                alert('Erro ao salvar barbeiro');
            }
        });
    }
});

// ========== CUPONS ==========

let currentCouponFilter = 'all';

async function loadCoupons(filter = 'all') {
    const couponsList = document.getElementById('couponsList');
    couponsList.innerHTML = '<div class="loader-container"><div class="loader"></div><p>Carregando...</p></div>';
    
    try {
        const url = filter === 'all' ? '/admin/cupons/' : `/admin/cupons/?filter=${filter}`;
        const response = await fetchAPI(url);
        const coupons = await response.json();
        
        couponsList.innerHTML = '';
        
        if (coupons.length === 0) {
            couponsList.innerHTML = '<div class="empty-state"><p>Nenhum cupom encontrado</p></div>';
            return;
        }
        
        coupons.forEach(coupon => {
            const item = document.createElement('div');
            item.className = 'coupon-item';
            
            const isExpired = coupon.expiration_date && new Date(coupon.expiration_date) < new Date();
            const status = !coupon.is_active ? 'inactive' : (isExpired ? 'expired' : 'active');
            
            item.innerHTML = `
                <div class="coupon-code-section">
                    <div class="coupon-code">${coupon.code}</div>
                    <span class="status-badge ${status}">
                        ${status === 'active' ? '✅ Ativo' : (status === 'expired' ? '⏰ Expirado' : '❌ Inativo')}
                    </span>
                </div>
                <div class="coupon-details">
                    <div class="coupon-info">
                        <span class="coupon-label">Desconto:</span>
                        <span class="coupon-value">
                            ${coupon.discount_type === 'percentage' ? `${coupon.discount_value}%` : formatCurrency(coupon.discount_value)}
                        </span>
                    </div>
                    <div class="coupon-info">
                        <span class="coupon-label">Expiração:</span>
                        <span>${coupon.expiration_date ? formatDate(coupon.expiration_date) : 'Sem expiração'}</span>
                    </div>
                    <div class="coupon-info">
                        <span class="coupon-label">Usos:</span>
                        <span>${coupon.times_used || 0}${coupon.usage_limit ? ` / ${coupon.usage_limit}` : ''}</span>
                    </div>
                </div>
                <div class="coupon-actions">
                    <button class="btn btn-sm btn-outline" onclick='editCoupon(${JSON.stringify(coupon)})'>✏️ Editar</button>
                    <button class="btn btn-sm btn-outline btn-danger" onclick="deleteCoupon(${coupon.id})">🗑️ Excluir</button>
                </div>
            `;
            couponsList.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading coupons:', error);
        couponsList.innerHTML = '<div class="error-state"><p>Erro ao carregar cupons</p></div>';
    }
}

function setupCouponFilters() {
    const filterBtns = document.querySelectorAll('.coupon-filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            currentCouponFilter = filter;
            
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            loadCoupons(filter);
        });
    });
}

function openCouponModal(coupon = null) {
    const modal = document.getElementById('couponModal');
    const form = document.getElementById('couponForm');
    const title = document.getElementById('couponModalTitle');
    
    if (coupon) {
        title.textContent = 'Editar Cupom';
        document.getElementById('couponId').value = coupon.id;
        document.getElementById('couponCode').value = coupon.code;
        document.getElementById('couponType').value = coupon.discount_type;
        document.getElementById('couponValue').value = coupon.discount_value;
        document.getElementById('couponExpiration').value = coupon.expiration_date || '';
        document.getElementById('couponLimit').value = coupon.usage_limit || '';
        document.getElementById('couponActive').checked = coupon.is_active;
    } else {
        title.textContent = 'Novo Cupom';
        form.reset();
        document.getElementById('couponId').value = '';
    }
    
    modal.style.display = 'flex';
}

function closeCouponModal() {
    document.getElementById('couponModal').style.display = 'none';
    document.getElementById('couponForm').reset();
}

function editCoupon(coupon) {
    openCouponModal(coupon);
}

async function deleteCoupon(couponId) {
    if (!confirm('Tem certeza que deseja excluir este cupom?')) return;
    
    try {
        const response = await fetchAPI(`/admin/cupons/${couponId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Cupom excluído com sucesso!');
            loadCoupons(currentCouponFilter);
        } else {
            alert('Erro ao excluir cupom');
        }
    } catch (error) {
        console.error('Error deleting coupon:', error);
        alert('Erro ao excluir cupom');
    }
}

// Form submit para cupons
document.addEventListener('DOMContentLoaded', () => {
    const couponForm = document.getElementById('couponForm');
    if (couponForm) {
        couponForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const couponId = document.getElementById('couponId').value;
            const data = {
                code: document.getElementById('couponCode').value.toUpperCase(),
                discount_type: document.getElementById('couponType').value,
                discount_value: parseFloat(document.getElementById('couponValue').value),
                expiration_date: document.getElementById('couponExpiration').value || null,
                usage_limit: document.getElementById('couponLimit').value ? parseInt(document.getElementById('couponLimit').value) : null,
                is_active: document.getElementById('couponActive').checked
            };
            
            try {
                const url = couponId ? `/admin/cupons/${couponId}/` : '/admin/cupons/';
                const method = couponId ? 'PUT' : 'POST';
                
                const response = await fetchAPI(url, {
                    method: method,
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Cupom salvo com sucesso!');
                    closeCouponModal();
                    loadCoupons(currentCouponFilter);
                } else {
                    alert('Erro ao salvar cupom');
                }
            } catch (error) {
                console.error('Error saving coupon:', error);
                alert('Erro ao salvar cupom');
            }
        });
    }
    
    // Fechar modais ao clicar fora
    window.onclick = function(event) {
        const modals = ['serviceModal', 'barberModal', 'couponModal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (modal && event.target === modal) {
                modal.style.display = 'none';
            }
        });
    };
});

