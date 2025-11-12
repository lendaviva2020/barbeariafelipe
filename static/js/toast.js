/**
 * Toast Notification System
 * Sistema de notificações toast (similar ao useToast do React)
 * Suporta múltiplos tipos: info, success, warning, error
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.toasts = [];
        this.maxToasts = 5;
        this.defaultDuration = 3000;
        
        this.init();
    }
    
    init() {
        this.createContainer();
    }
    
    createContainer() {
        // Verificar se já existe
        this.container = document.getElementById('toast-container');
        
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container';
            this.container.setAttribute('aria-live', 'polite');
            this.container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(this.container);
        }
    }
    
    /**
     * Mostra uma notificação toast
     * @param {string} message - Mensagem a exibir
     * @param {string} type - Tipo: 'info', 'success', 'warning', 'error'
     * @param {number} duration - Duração em ms (padrão 3000)
     */
    show(message, type = 'info', duration = this.defaultDuration) {
        // Limitar número de toasts
        if (this.toasts.length >= this.maxToasts) {
            this.remove(this.toasts[0]);
        }
        
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);
        this.toasts.push(toast);
        
        // Animação de entrada
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        // Auto-remover após duração
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }
        
        return toast;
    }
    
    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'status');
        
        // Ícone baseado no tipo
        const icon = this.getIcon(type);
        
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-content">
                <p class="toast-message">${this.escapeHtml(message)}</p>
            </div>
            <button type="button" class="toast-close" aria-label="Fechar notificação">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        `;
        
        // Click no botão fechar
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.remove(toast);
            });
        }
        
        return toast;
    }
    
    getIcon(type) {
        const icons = {
            info: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 16v-4m0-4h.01"/>
            </svg>`,
            
            success: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>`,
            
            warning: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>`,
            
            error: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>`
        };
        
        return icons[type] || icons.info;
    }
    
    remove(toast) {
        if (!toast || !toast.classList) return;
        
        toast.classList.remove('show');
        toast.classList.add('hide');
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.toasts = this.toasts.filter(t => t !== toast);
        }, 300);
    }
    
    /**
     * Remove todas as notificações
     */
    clear() {
        this.toasts.forEach(toast => this.remove(toast));
    }
    
    /**
     * Atalhos para tipos específicos
     */
    info(message, duration) {
        return this.show(message, 'info', duration);
    }
    
    success(message, duration) {
        return this.show(message, 'success', duration);
    }
    
    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }
    
    error(message, duration) {
        return this.show(message, 'error', duration);
    }
    
    /**
     * Escape HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// CSS inline para toasts
const toastStyles = document.createElement('style');
toastStyles.textContent = `
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    gap: 12px;
    pointer-events: none;
}

.toast {
    display: flex;
    align-items: start;
    gap: 12px;
    min-width: 300px;
    max-width: 400px;
    padding: 16px;
    background: hsl(var(--card));
    border: 1px solid hsl(var(--border));
    border-radius: 8px;
    box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.3);
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: auto;
}

.toast.show {
    opacity: 1;
    transform: translateX(0);
}

.toast.hide {
    opacity: 0;
    transform: translateX(100%);
}

.toast-icon {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.toast-info {
    border-left: 4px solid hsl(var(--primary));
}

.toast-info .toast-icon {
    color: hsl(var(--primary));
}

.toast-success {
    border-left: 4px solid #10b981;
}

.toast-success .toast-icon {
    color: #10b981;
}

.toast-warning {
    border-left: 4px solid #f59e0b;
}

.toast-warning .toast-icon {
    color: #f59e0b;
}

.toast-error {
    border-left: 4px solid hsl(var(--destructive));
}

.toast-error .toast-icon {
    color: hsl(var(--destructive));
}

.toast-content {
    flex: 1;
    min-width: 0;
}

.toast-message {
    font-size: 0.875rem;
    color: hsl(var(--foreground));
    margin: 0;
    line-height: 1.5;
}

.toast-close {
    flex-shrink: 0;
    padding: 4px;
    background: transparent;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    color: hsl(var(--muted-foreground));
    transition: all 0.2s ease;
}

.toast-close:hover {
    background: hsl(var(--muted));
    color: hsl(var(--foreground));
}

/* Responsive */
@media (max-width: 640px) {
    .toast-container {
        top: auto;
        bottom: 20px;
        left: 20px;
        right: 20px;
    }
    
    .toast {
        min-width: 100%;
        max-width: 100%;
        transform: translateY(100%);
    }
    
    .toast.show {
        transform: translateY(0);
    }
    
    .toast.hide {
        transform: translateY(100%);
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .toast {
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.6);
    }
}

/* Reduzir movimento */
@media (prefers-reduced-motion: reduce) {
    .toast {
        transition: opacity 0.2s ease;
    }
    
    .toast.show,
    .toast.hide {
        transform: none;
    }
}
`;
document.head.appendChild(toastStyles);

// Criar instância global
window.toast = new ToastManager();

// Exemplo de uso:
// window.toast.show('Mensagem genérica', 'info');
// window.toast.success('Operação concluída!');
// window.toast.error('Algo deu errado');
// window.toast.warning('Atenção!');

