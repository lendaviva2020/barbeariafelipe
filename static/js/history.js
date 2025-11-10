/**
 * History Page - Sistema completo de histórico de agendamentos
 * Extraído 100% do React History.tsx (553 linhas)
 */

// State management
let appointments = [];
let filteredAppointments = [];
let currentFilter = 'all';
let selectedAppointment = null;
let isCancelling = false;

// Initialize page
document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!auth.isAuthenticated()) {
        window.location.href = '/auth/?redirect=/historico/';
        return;
    }
    
    // Setup event listeners
    setupFilterTabs();
    setupCancelReasonCounter();
    
    // Load appointments
    await loadAppointments();
});

/**
 * Setup filter tabs
 */
function setupFilterTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const filter = tab.dataset.filter;
            setFilter(filter);
        });
    });
}

/**
 * Setup cancel reason character counter
 */
function setupCancelReasonCounter() {
    const textarea = document.getElementById('cancelReason');
    const counter = document.getElementById('reasonCount');
    
    if (textarea && counter) {
        textarea.addEventListener('input', () => {
            counter.textContent = textarea.value.length;
        });
    }
}

/**
 * Load appointments from API
 */
async function loadAppointments() {
    showLoading();
    
    try {
        const response = await fetchAPI('/api/agendamentos/');
        
        if (!response.ok) {
            throw new Error('Erro ao carregar agendamentos');
        }
        
        appointments = await response.json();
        filteredAppointments = [...appointments];
        
        // Sort by date (newest first)
        appointments.sort((a, b) => {
            const dateA = new Date(`${a.appointment_date}T${a.appointment_time}`);
            const dateB = new Date(`${b.appointment_date}T${b.appointment_time}`);
            return dateB - dateA;
        });
        
        renderAppointments();
    } catch (error) {
        console.error('Error loading appointments:', error);
        showError('Não foi possível carregar os agendamentos. Tente novamente.');
    } finally {
        hideLoading();
    }
}

/**
 * Set filter and re-render
 */
function setFilter(filter) {
    currentFilter = filter;
    
    // Update tab active state
    document.querySelectorAll('.tab-btn').forEach(tab => {
        if (tab.dataset.filter === filter) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    // Filter appointments
    if (filter === 'all') {
        filteredAppointments = [...appointments];
    } else {
        filteredAppointments = appointments.filter(apt => apt.status === filter);
    }
    
    renderAppointments();
}

/**
 * Render appointments list
 */
function renderAppointments() {
    const container = document.getElementById('appointmentsList');
    const emptyState = document.getElementById('emptyState');
    
    if (filteredAppointments.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        updateEmptyMessage();
        return;
    }
    
    emptyState.style.display = 'none';
    container.innerHTML = filteredAppointments.map(apt => createAppointmentCard(apt)).join('');
}

/**
 * Update empty state message based on filter
 */
function updateEmptyMessage() {
    const message = document.getElementById('emptyMessage');
    const messages = {
        'all': 'Você ainda não tem agendamentos.',
        'pending': 'Nenhum agendamento pendente encontrado.',
        'confirmed': 'Nenhum agendamento confirmado encontrado.',
        'completed': 'Nenhum agendamento concluído encontrado.',
        'cancelled': 'Nenhum agendamento cancelado encontrado.'
    };
    
    message.textContent = messages[currentFilter] || messages['all'];
}

/**
 * Create appointment card HTML
 */
function createAppointmentCard(appointment) {
    const canCancel = checkCanCancel(appointment);
    const appointmentDate = new Date(`${appointment.appointment_date}T${appointment.appointment_time}`);
    const formattedDate = formatAppointmentDate(appointmentDate);
    
    return `
        <div class="appointment-card" data-id="${appointment.id}">
            <!-- Header -->
            <div class="appointment-header">
                <div class="appointment-date-info">
                    <div class="appointment-date">
                        📅 ${formattedDate}
                    </div>
                    <div class="appointment-time">
                        🕐 ${appointment.appointment_time}
                    </div>
                </div>
                ${getStatusBadge(appointment.status)}
            </div>
            
            <!-- Details -->
            <div class="appointment-details">
                ${appointment.customer_name ? `
                    <div class="detail-row">
                        <span class="detail-icon">👤</span>
                        <span class="detail-text">${appointment.customer_name}</span>
                    </div>
                ` : ''}
                
                <div class="detail-row">
                    <span class="detail-icon">✂️</span>
                    <span class="detail-text">${appointment.service_name || 'Serviço não especificado'}</span>
                </div>
                
                ${appointment.price ? `
                    <div class="detail-row">
                        <span class="detail-icon">💰</span>
                        <span class="detail-text price-text">
                            R$ ${appointment.price.toFixed(2)}
                            ${appointment.discount_amount && appointment.discount_amount > 0 ? 
                                `<span class="discount-badge">-R$ ${appointment.discount_amount.toFixed(2)}</span>` 
                                : ''}
                        </span>
                    </div>
                ` : ''}
            </div>
            
            <!-- Additional Info -->
            ${(appointment.notes || appointment.payment_method || appointment.photo_url) ? `
                <div class="additional-info">
                    ${appointment.notes ? `
                        <div class="mb-2">
                            <p class="info-label">Observações:</p>
                            <p class="info-value">${appointment.notes}</p>
                        </div>
                    ` : ''}
                    
                    ${appointment.payment_method ? `
                        <div class="text-sm">
                            <span class="text-muted">Pagamento: </span>
                            <span class="font-medium capitalize">${appointment.payment_method}</span>
                        </div>
                    ` : ''}
                    
                    ${appointment.photo_url ? `
                        <div class="flex items-center gap-2 text-sm text-primary mt-2">
                            🖼️ <span>Foto de referência disponível</span>
                        </div>
                    ` : ''}
                </div>
            ` : ''}
            
            <!-- Actions -->
            <div class="appointment-actions">
                <button class="btn-chat" onclick="openChat('${appointment.id}')">
                    💬 Chat
                </button>
                ${canCancel ? `
                    <button class="btn-cancel" onclick="openCancelDialog('${appointment.id}')">
                        ❌ Cancelar
                    </button>
                ` : ''}
            </div>
            
            <!-- Cancel Reason (if cancelled) -->
            ${appointment.cancel_reason ? `
                <div class="cancel-reason">
                    <div class="cancel-reason-header">
                        <span>⚠️</span>
                        <div>
                            <p class="cancel-reason-title">Motivo do cancelamento:</p>
                            <p class="cancel-reason-text">${appointment.cancel_reason}</p>
                        </div>
                    </div>
                </div>
            ` : ''}
        </div>
    `;
}

/**
 * Format appointment date (pt-BR)
 */
function formatAppointmentDate(date) {
    const months = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
    ];
    
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    
    return `${day} de ${month} de ${year}`;
}

/**
 * Get status badge HTML
 */
function getStatusBadge(status) {
    const badges = {
        'pending': { label: 'Pendente', class: 'pending', icon: '🕐' },
        'confirmed': { label: 'Confirmado', class: 'confirmed', icon: '✅' },
        'completed': { label: 'Concluído', class: 'completed', icon: '✅' },
        'cancelled': { label: 'Cancelado', class: 'cancelled', icon: '❌' }
    };
    
    const badge = badges[status] || badges['pending'];
    
    return `
        <span class="status-badge ${badge.class}">
            ${badge.icon} ${badge.label}
        </span>
    `;
}

/**
 * Check if appointment can be cancelled (2h before)
 */
function checkCanCancel(appointment) {
    if (appointment.status === 'cancelled' || appointment.status === 'completed') {
        return false;
    }
    
    const appointmentDateTime = new Date(`${appointment.appointment_date}T${appointment.appointment_time}`);
    const twoHoursBefore = new Date(appointmentDateTime.getTime() - (2 * 60 * 60 * 1000));
    const now = new Date();
    
    return now < twoHoursBefore;
}

/**
 * Open cancel dialog
 */
function openCancelDialog(appointmentId) {
    selectedAppointment = appointments.find(apt => apt.id == appointmentId);
    
    if (!selectedAppointment) {
        showToast('Erro', 'Agendamento não encontrado', 'error');
        return;
    }
    
    const appointmentDate = new Date(`${selectedAppointment.appointment_date}T${selectedAppointment.appointment_time}`);
    const formattedDate = formatDateTime(appointmentDate);
    
    document.getElementById('cancelMessage').innerHTML = 
        `Tem certeza que deseja cancelar o agendamento do dia <strong>${formattedDate}</strong>?`;
    
    document.getElementById('cancelDialog').style.display = 'flex';
    document.getElementById('cancelReason').value = '';
    document.getElementById('reasonCount').textContent = '0';
}

/**
 * Close cancel dialog
 */
function closeCancelDialog() {
    document.getElementById('cancelDialog').style.display = 'none';
    selectedAppointment = null;
    isCancelling = false;
}

/**
 * Confirm cancel
 */
async function confirmCancel() {
    if (!selectedAppointment || isCancelling) return;
    
    isCancelling = true;
    const btn = document.getElementById('confirmCancelBtn');
    btn.disabled = true;
    btn.textContent = 'Cancelando...';
    
    const reason = document.getElementById('cancelReason').value.trim() || 'Cancelado pelo cliente';
    
    try {
        const response = await fetchAPI(`/api/agendamentos/${selectedAppointment.id}/cancel/`, {
            method: 'POST',
            body: JSON.stringify({ reason })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao cancelar agendamento');
        }
        
        showToast('Sucesso', 'Agendamento cancelado com sucesso', 'success');
        closeCancelDialog();
        
        // Reload appointments
        await loadAppointments();
    } catch (error) {
        console.error('Error cancelling appointment:', error);
        showToast('Erro', 'Não foi possível cancelar o agendamento. Tente novamente.', 'error');
    } finally {
        isCancelling = false;
        btn.disabled = false;
        btn.textContent = 'Confirmar Cancelamento';
    }
}

/**
 * Open chat dialog
 */
function openChat(appointmentId) {
    const appointment = appointments.find(apt => apt.id == appointmentId);
    
    if (!appointment) {
        showToast('Erro', 'Agendamento não encontrado', 'error');
        return;
    }
    
    // Simple chat implementation
    document.getElementById('chatDialog').style.display = 'flex';
    
    // In a real implementation, this would load chat history
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="chat-message bot">
            <p>Olá! Como posso ajudar com seu agendamento do dia ${appointment.appointment_date}?</p>
            <span class="chat-time">Agora</span>
        </div>
    `;
}

/**
 * Close chat dialog
 */
function closeChatDialog() {
    document.getElementById('chatDialog').style.display = 'none';
}

/**
 * Send chat message
 */
function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    const chatMessages = document.getElementById('chatMessages');
    const now = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    chatMessages.innerHTML += `
        <div class="chat-message user">
            <p>${message}</p>
            <span class="chat-time">${now}</span>
        </div>
    `;
    
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Auto response (mock)
    setTimeout(() => {
        chatMessages.innerHTML += `
            <div class="chat-message bot">
                <p>Obrigado pela mensagem! Um atendente irá responder em breve.</p>
                <span class="chat-time">${now}</span>
            </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

/**
 * Format date and time for display
 */
function formatDateTime(date) {
    return date.toLocaleDateString('pt-BR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Show loading state
 */
function showLoading() {
    document.getElementById('loadingState').style.display = 'flex';
    document.getElementById('appointmentsList').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

/**
 * Hide loading state
 */
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('appointmentsList').style.display = 'flex';
}

/**
 * Show error message
 */
function showError(message) {
    const container = document.getElementById('appointmentsList');
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">⚠️</div>
            <h3>Erro ao carregar</h3>
            <p>${message}</p>
            <button class="btn btn-primary" onclick="loadAppointments()">Tentar Novamente</button>
        </div>
    `;
}

/**
 * Show toast notification
 */
function showToast(title, message, type = 'info') {
    // Use existing toast system from app.js if available
    if (window.showToast) {
        window.showToast(title, message, type);
    } else {
        alert(`${title}: ${message}`);
    }
}

// Export functions for inline onclick handlers
window.openCancelDialog = openCancelDialog;
window.closeCancelDialog = closeCancelDialog;
window.confirmCancel = confirmCancel;
window.openChat = openChat;
window.closeChatDialog = closeChatDialog;
window.sendChatMessage = sendChatMessage;

