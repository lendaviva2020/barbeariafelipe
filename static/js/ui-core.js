/**
 * UI Core - Sistema de Componentes Django
 * Utilitários e inicializadores para componentes UI
 */

// Namespace global
window.UI = window.UI || {};

/**
 * Utilitários de classe CSS
 */
UI.classList = {
    /**
     * Adiciona classe com suporte para múltiplas classes
     */
    add(element, ...classes) {
        if (!element) return;
        classes.forEach(cls => {
            if (cls) element.classList.add(...cls.split(' ').filter(Boolean));
        });
    },
    
    /**
     * Remove classe
     */
    remove(element, ...classes) {
        if (!element) return;
        classes.forEach(cls => {
            if (cls) element.classList.remove(...cls.split(' ').filter(Boolean));
        });
    },
    
    /**
     * Toggle classe
     */
    toggle(element, className, force) {
        if (!element) return;
        return element.classList.toggle(className, force);
    },
    
    /**
     * Verifica se tem classe
     */
    has(element, className) {
        if (!element) return false;
        return element.classList.contains(className);
    }
};

/**
 * Utilitários DOM
 */
UI.dom = {
    /**
     * Query selector seguro
     */
    $(selector, context = document) {
        return context.querySelector(selector);
    },
    
    /**
     * Query selector all
     */
    $$(selector, context = document) {
        return Array.from(context.querySelectorAll(selector));
    },
    
    /**
     * Criar elemento
     */
    create(tag, attrs = {}, children = []) {
        const element = document.createElement(tag);
        
        Object.entries(attrs).forEach(([key, value]) => {
            if (key === 'class') {
                UI.classList.add(element, value);
            } else if (key === 'dataset') {
                Object.entries(value).forEach(([dataKey, dataValue]) => {
                    element.dataset[dataKey] = dataValue;
                });
            } else if (key.startsWith('on') && typeof value === 'function') {
                element.addEventListener(key.substring(2).toLowerCase(), value);
            } else {
                element.setAttribute(key, value);
            }
        });
        
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child instanceof Node) {
                element.appendChild(child);
            }
        });
        
        return element;
    },
    
    /**
     * Remove elemento
     */
    remove(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }
};

/**
 * Gerenciador de estado
 */
UI.state = {
    _store: {},
    
    set(key, value) {
        this._store[key] = value;
        this._notify(key, value);
    },
    
    get(key, defaultValue = null) {
        return this._store[key] !== undefined ? this._store[key] : defaultValue;
    },
    
    _listeners: {},
    
    subscribe(key, callback) {
        if (!this._listeners[key]) {
            this._listeners[key] = [];
        }
        this._listeners[key].push(callback);
        
        return () => {
            this._listeners[key] = this._listeners[key].filter(cb => cb !== callback);
        };
    },
    
    _notify(key, value) {
        if (this._listeners[key]) {
            this._listeners[key].forEach(callback => callback(value));
        }
    }
};

/**
 * Event Bus para comunicação entre componentes
 */
UI.events = {
    _events: {},
    
    on(event, callback) {
        if (!this._events[event]) {
            this._events[event] = [];
        }
        this._events[event].push(callback);
        
        return () => {
            this._events[event] = this._events[event].filter(cb => cb !== callback);
        };
    },
    
    emit(event, data) {
        if (this._events[event]) {
            this._events[event].forEach(callback => callback(data));
        }
    },
    
    off(event, callback) {
        if (this._events[event]) {
            if (callback) {
                this._events[event] = this._events[event].filter(cb => cb !== callback);
            } else {
                this._events[event] = [];
            }
        }
    }
};

/**
 * Utilitários de animação
 */
UI.animate = {
    /**
     * Fade in element
     */
    fadeIn(element, duration = 300) {
        return new Promise(resolve => {
            element.style.opacity = '0';
            element.style.display = 'block';
            
            setTimeout(() => {
                element.style.transition = `opacity ${duration}ms ease-in-out`;
                element.style.opacity = '1';
                
                setTimeout(resolve, duration);
            }, 10);
        });
    },
    
    /**
     * Fade out element
     */
    fadeOut(element, duration = 300) {
        return new Promise(resolve => {
            element.style.transition = `opacity ${duration}ms ease-in-out`;
            element.style.opacity = '0';
            
            setTimeout(() => {
                element.style.display = 'none';
                resolve();
            }, duration);
        });
    },
    
    /**
     * Slide down (accordion style)
     */
    slideDown(element, duration = 300) {
        return new Promise(resolve => {
            element.style.height = '0';
            element.style.overflow = 'hidden';
            element.style.display = 'block';
            
            const height = element.scrollHeight;
            
            setTimeout(() => {
                element.style.transition = `height ${duration}ms ease-out`;
                element.style.height = height + 'px';
                
                setTimeout(() => {
                    element.style.height = 'auto';
                    element.style.overflow = 'visible';
                    resolve();
                }, duration);
            }, 10);
        });
    },
    
    /**
     * Slide up (accordion style)
     */
    slideUp(element, duration = 300) {
        return new Promise(resolve => {
            const height = element.scrollHeight;
            element.style.height = height + 'px';
            element.style.overflow = 'hidden';
            
            setTimeout(() => {
                element.style.transition = `height ${duration}ms ease-out`;
                element.style.height = '0';
                
                setTimeout(() => {
                    element.style.display = 'none';
                    resolve();
                }, duration);
            }, 10);
        });
    }
};

/**
 * Utilitários gerais
 */
UI.utils = {
    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    /**
     * Get CSRF token
     */
    getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    },
    
    /**
     * Gerar ID único
     */
    generateId(prefix = 'ui') {
        return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    },
    
    /**
     * Sanitizar HTML
     */
    escapeHtml(unsafe) {
        const div = document.createElement('div');
        div.textContent = unsafe;
        return div.innerHTML;
    },
    
    /**
     * Verificar se elemento está visível
     */
    isVisible(element) {
        return !!(element.offsetWidth || element.offsetHeight || element.getClientRects().length);
    },
    
    /**
     * Scroll suave para elemento
     */
    scrollTo(element, options = {}) {
        if (!element) return;
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            ...options
        });
    }
};

/**
 * Gerenciador de componentes
 */
UI.components = {
    _registry: {},
    
    /**
     * Registrar componente
     */
    register(name, component) {
        this._registry[name] = component;
    },
    
    /**
     * Obter componente registrado
     */
    get(name) {
        return this._registry[name];
    },
    
    /**
     * Inicializar todos os componentes na página
     */
    initAll() {
        Object.entries(this._registry).forEach(([name, Component]) => {
            if (Component.init && typeof Component.init === 'function') {
                Component.init();
            }
        });
    }
};

/**
 * Gerenciador de modais/overlays
 */
UI.overlay = {
    _stack: [],
    
    /**
     * Abrir overlay
     */
    open(element) {
        this._stack.push(element);
        document.body.style.overflow = 'hidden';
        UI.classList.add(element, 'block');
        element.setAttribute('data-state', 'open');
        
        // Trap focus
        this._trapFocus(element);
    },
    
    /**
     * Fechar overlay
     */
    close(element) {
        const index = this._stack.indexOf(element);
        if (index > -1) {
            this._stack.splice(index, 1);
        }
        
        if (this._stack.length === 0) {
            document.body.style.overflow = '';
        }
        
        element.setAttribute('data-state', 'closed');
        
        setTimeout(() => {
            UI.classList.remove(element, 'block');
            UI.classList.add(element, 'hidden');
        }, 300);
    },
    
    /**
     * Fechar último overlay
     */
    closeLast() {
        if (this._stack.length > 0) {
            this.close(this._stack[this._stack.length - 1]);
        }
    },
    
    /**
     * Trap focus dentro do overlay
     */
    _trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            } else if (e.key === 'Escape') {
                UI.overlay.close(element);
            }
        });
        
        // Focus primeiro elemento
        if (firstElement) {
            firstElement.focus();
        }
    }
};

/**
 * Gerenciador de toasts
 */
UI.toast = {
    _container: null,
    _toasts: [],
    
    /**
     * Inicializar container de toasts
     */
    init() {
        if (!this._container) {
            this._container = UI.dom.create('div', {
                class: 'toast-viewport',
                'aria-live': 'polite',
                'aria-atomic': 'true'
            });
            document.body.appendChild(this._container);
        }
    },
    
    /**
     * Mostrar toast
     */
    show(options = {}) {
        this.init();
        
        const {
            title = '',
            description = '',
            variant = 'default',
            duration = 5000,
            action = null
        } = options;
        
        const id = UI.utils.generateId('toast');
        
        const toast = UI.dom.create('div', {
            class: `toast toast-${variant}`,
            'data-state': 'open',
            id: id
        }, [
            UI.dom.create('div', { class: 'grid gap-1' }, [
                title ? UI.dom.create('div', { class: 'toast-title' }, [title]) : null,
                description ? UI.dom.create('div', { class: 'toast-description' }, [description]) : null
            ].filter(Boolean)),
            UI.dom.create('button', {
                class: 'absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100',
                'aria-label': 'Close',
                onClick: () => this.dismiss(id)
            }, ['×'])
        ]);
        
        this._container.appendChild(toast);
        this._toasts.push({ id, element: toast });
        
        // Auto dismiss
        if (duration > 0) {
            setTimeout(() => this.dismiss(id), duration);
        }
        
        return id;
    },
    
    /**
     * Dismiss toast
     */
    dismiss(id) {
        const toastObj = this._toasts.find(t => t.id === id);
        if (!toastObj) return;
        
        toastObj.element.setAttribute('data-state', 'closed');
        
        setTimeout(() => {
            UI.dom.remove(toastObj.element);
            this._toasts = this._toasts.filter(t => t.id !== id);
        }, 300);
    },
    
    /**
     * Success toast
     */
    success(title, description) {
        return this.show({ title: '✅ ' + title, description, variant: 'default' });
    },
    
    /**
     * Error toast
     */
    error(title, description) {
        return this.show({ title: '❌ ' + title, description, variant: 'destructive' });
    },
    
    /**
     * Info toast
     */
    info(title, description) {
        return this.show({ title: 'ℹ️ ' + title, description, variant: 'default' });
    }
};

/**
 * Gerenciador de validação de formulários
 */
UI.form = {
    /**
     * Validar campo
     */
    validate(input, rules = {}) {
        const errors = [];
        const value = input.value;
        
        if (rules.required && !value.trim()) {
            errors.push('Este campo é obrigatório');
        }
        
        if (rules.minLength && value.length < rules.minLength) {
            errors.push(`Mínimo de ${rules.minLength} caracteres`);
        }
        
        if (rules.maxLength && value.length > rules.maxLength) {
            errors.push(`Máximo de ${rules.maxLength} caracteres`);
        }
        
        if (rules.pattern && !new RegExp(rules.pattern).test(value)) {
            errors.push(rules.patternMessage || 'Formato inválido');
        }
        
        if (rules.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            errors.push('Email inválido');
        }
        
        if (rules.phone && !/^\(\d{2}\)\s?\d{4,5}-?\d{4}$/.test(value)) {
            errors.push('Telefone inválido');
        }
        
        if (rules.custom && typeof rules.custom === 'function') {
            const customError = rules.custom(value);
            if (customError) errors.push(customError);
        }
        
        return {
            valid: errors.length === 0,
            errors
        };
    },
    
    /**
     * Mostrar erros no formulário
     */
    showErrors(input, errors) {
        const formItem = input.closest('[data-form-item]');
        if (!formItem) return;
        
        // Remove erros anteriores
        const oldError = formItem.querySelector('[data-form-error]');
        if (oldError) UI.dom.remove(oldError);
        
        if (errors.length > 0) {
            const errorDiv = UI.dom.create('p', {
                class: 'text-sm font-medium text-destructive mt-1',
                'data-form-error': ''
            }, [errors[0]]);
            
            formItem.appendChild(errorDiv);
            UI.classList.add(input, 'border-destructive');
        } else {
            UI.classList.remove(input, 'border-destructive');
        }
    }
};

/**
 * Utilitários de API
 */
UI.api = {
    /**
     * Fazer requisição fetch com configurações padrão
     */
    async fetch(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': UI.utils.getCsrfToken()
            }
        };
        
        const response = await fetch(url, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    },
    
    /**
     * GET request
     */
    get(url, options = {}) {
        return this.fetch(url, { ...options, method: 'GET' });
    },
    
    /**
     * POST request
     */
    post(url, data, options = {}) {
        return this.fetch(url, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * PUT request
     */
    put(url, data, options = {}) {
        return this.fetch(url, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    /**
     * DELETE request
     */
    delete(url, options = {}) {
        return this.fetch(url, { ...options, method: 'DELETE' });
    }
};

/**
 * Gerenciador de temas
 */
UI.theme = {
    /**
     * Obter tema atual
     */
    get() {
        return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    },
    
    /**
     * Definir tema
     */
    set(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        localStorage.setItem('theme', theme);
        UI.events.emit('theme:changed', theme);
    },
    
    /**
     * Toggle tema
     */
    toggle() {
        const currentTheme = this.get();
        this.set(currentTheme === 'dark' ? 'light' : 'dark');
    },
    
    /**
     * Inicializar tema salvo
     */
    init() {
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme) {
            this.set(savedTheme);
        } else if (prefersDark) {
            this.set('dark');
        }
        
        // Escutar mudanças de preferência do sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.set(e.matches ? 'dark' : 'light');
            }
        });
    }
};

/**
 * Inicialização global
 */
UI.init = function() {
    console.log('🎨 UI Core initialized');
    
    // Inicializar tema
    UI.theme.init();
    
    // Inicializar componentes
    UI.components.initAll();
    
    // Fechar overlays com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            UI.overlay.closeLast();
        }
    });
    
    // Marcar como inicializado
    document.documentElement.setAttribute('data-ui-initialized', 'true');
};

// Auto-inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => UI.init());
} else {
    UI.init();
}

// Exportar para uso global
window.UI = UI;

