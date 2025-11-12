/**
 * Notification Center Component
 * Centro de notificações em tempo real com polling
 */

class NotificationCenter {
    constructor() {
        this.btn = document.getElementById('notification-btn');
        this.panel = document.getElementById('notification-panel');
        this.list = document.getElementById('notification-list');
        this.badge = document.getElementById('notif-count');
        this.markAllBtn = document.getElementById('mark-all-read-btn');
        
        if (!this.btn || !this.panel || !this.list) {
            console.warn('Notification center elements not found');
            return;
        }
        
        this.isOpen = false;
        this.notifications = [];
        this.unreadCount = 0;
        this.pollingInterval = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.startPolling();
        this.loadNotifications();
    }
    
    setupEventListeners() {
        // Toggle painel
        this.btn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });
        
        // Fechar ao clicar fora
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.panel.contains(e.target) && e.target !== this.btn) {
                this.close();
            }
        });
        
        // Marcar todas como lidas
        if (this.markAllBtn) {
            this.markAllBtn.addEventListener('click', () => {
                this.markAllAsRead();
            });
        }
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.panel.classList.remove('hidden');
        this.panel.classList.add('active');
        this.btn.setAttribute('aria-expanded', 'true');
        this.isOpen = true;
        this.loadNotifications(); // Atualizar ao abrir
    }
    
    close() {
        this.panel.classList.add('hidden');
        this.panel.classList.remove('active');
        this.btn.setAttribute('aria-expanded', 'false');
        this.isOpen = false;
    }
    
    async loadNotifications() {
        try {
            const response = await fetch('/api/notifications/unread/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Erro ao carregar notificações');
            }
            
            const data = await response.json();
            this.notifications = data.results || data;
            this.updateUI();
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }
    
    updateUI() {
        // Atualizar badge
        this.unreadCount = this.notifications.length;
        this.updateBadge();
        
        // Atualizar lista
        if (this.notifications.length === 0) {
            this.showEmptyState();
        } else {
            this.renderNotifications();
        }
        
        // Mostrar/esconder botão "marcar todas"
        if (this.markAllBtn) {
            if (this.unreadCount > 0) {
                this.markAllBtn.classList.remove('hidden');
            } else {
                this.markAllBtn.classList.add('hidden');
            }
        }
    }
    
    updateBadge() {
        if (this.unreadCount > 0) {
            this.badge.textContent = this.unreadCount > 9 ? '9+' : this.unreadCount;
            this.badge.classList.remove('hidden');
        } else {
            this.badge.classList.add('hidden');
        }
    }
    
    showEmptyState() {
        this.list.innerHTML = `
            <div class="notification-empty">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
                <p>Nenhuma notificação</p>
            </div>
        `;
    }
    
    renderNotifications() {
        this.list.innerHTML = '';
        
        this.notifications.forEach((notification) => {
            const item = this.createNotificationItem(notification);
            this.list.appendChild(item);
        });
    }
    
    createNotificationItem(notification) {
        const template = document.getElementById('notification-item-template');
        const clone = template.content.cloneNode(true);
        
        const item = clone.querySelector('.notification-item');
        
        // Se não lida, adicionar classe
        if (notification.status === 'pending') {
            item.classList.add('unread');
        }
        
        // Mensagem
        clone.querySelector('.notification-message').textContent = notification.message;
        
        // Tempo relativo
        const timeEl = clone.querySelector('.notification-time');
        timeEl.textContent = this.formatTime(notification.created_at);
        
        // Botão marcar como lida
        const markReadBtn = clone.querySelector('.mark-read-btn');
        if (notification.status === 'pending') {
            markReadBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.markAsRead(notification.id);
            });
        } else {
            markReadBtn.remove();
        }
        
        // Botão deletar
        const deleteBtn = clone.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.deleteNotification(notification.id);
        });
        
        return clone;
    }
    
    async markAsRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/mark-read/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCsrfToken()
                },
                credentials: 'include'
            });
            
            if (response.ok) {
                this.loadNotifications(); // Recarregar lista
            }
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    }
    
    async markAllAsRead() {
        try {
            const response = await fetch('/api/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCsrfToken()
                },
                credentials: 'include'
            });
            
            if (response.ok) {
                this.loadNotifications(); // Recarregar lista
                if (window.toast) {
                    window.toast.show('Todas notificações marcadas como lidas', 'success');
                }
            }
        } catch (error) {
            console.error('Error marking all as read:', error);
        }
    }
    
    async deleteNotification(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCsrfToken()
                },
                credentials: 'include'
            });
            
            if (response.ok) {
                this.loadNotifications(); // Recarregar lista
            }
        } catch (error) {
            console.error('Error deleting notification:', error);
        }
    }
    
    formatTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Agora';
        if (diffMins < 60) return `${diffMins}m atrás`;
        if (diffHours < 24) return `${diffHours}h atrás`;
        if (diffDays < 7) return `${diffDays}d atrás`;
        
        return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
    }
    
    startPolling() {
        // Polling a cada 30 segundos
        this.pollingInterval = setInterval(() => {
            this.loadNotifications();
        }, 30000);
    }
    
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }
    }
    
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    destroy() {
        this.stopPolling();
    }
}

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.notificationCenter = new NotificationCenter();
    });
} else {
    window.notificationCenter = new NotificationCenter();
}

// Cleanup ao descarregar página
window.addEventListener('beforeunload', () => {
    if (window.notificationCenter) {
        window.notificationCenter.destroy();
    }
});

