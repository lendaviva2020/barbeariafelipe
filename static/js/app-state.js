/**
 * App State Management
 * Sistema de estado global simples (similar ao React Context)
 * Para compartilhar estado entre componentes
 */

class AppState {
    constructor() {
        this.state = {
            user: null,
            notifications: [],
            unreadCount: 0,
            isAuthenticated: false,
            searchResults: [],
            selectedAppointment: null
        };
        
        this.listeners = [];
        this.initialized = false;
    }
    
    /**
     * Inicializa o estado com dados do usuário atual
     */
    async init() {
        if (this.initialized) return;
        
        try {
            // Tentar buscar dados do usuário (apenas se autenticado)
            const response = await fetch('/api/users/me/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            if (response.ok) {
                const userData = await response.json();
                this.setState({
                    user: userData,
                    isAuthenticated: true
                });
            } else if (response.status === 401) {
                // Usuário não autenticado - isso é normal, não é erro
                // Silenciar este caso
            }
        } catch (error) {
            // Silenciar erros de rede quando não autenticado
            // Apenas logar se for um erro diferente de 401
            if (error.status !== 401) {
                console.warn('Could not load user data:', error);
            }
        }
        
        this.initialized = true;
    }
    
    /**
     * Atualiza o estado e notifica listeners
     */
    setState(newState) {
        const oldState = { ...this.state };
        this.state = { ...this.state, ...newState };
        
        // Notificar todos os listeners
        this.listeners.forEach(fn => {
            try {
                fn(this.state, oldState);
            } catch (error) {
                console.error('Error in state listener:', error);
            }
        });
    }
    
    /**
     * Retorna o estado atual
     */
    getState() {
        return { ...this.state };
    }
    
    /**
     * Inscreve um listener para mudanças de estado
     * Retorna função para cancelar inscrição
     */
    subscribe(fn) {
        if (typeof fn !== 'function') {
            throw new Error('Subscriber must be a function');
        }
        
        this.listeners.push(fn);
        
        // Retornar unsubscribe function
        return () => {
            this.listeners = this.listeners.filter(l => l !== fn);
        };
    }
    
    /**
     * Atualiza dados do usuário
     */
    setUser(user) {
        this.setState({
            user,
            isAuthenticated: !!user
        });
    }
    
    /**
     * Atualiza notificações
     */
    setNotifications(notifications) {
        const unreadCount = notifications.filter(n => n.status === 'pending').length;
        this.setState({
            notifications,
            unreadCount
        });
    }
    
    /**
     * Adiciona uma nova notificação
     */
    addNotification(notification) {
        const notifications = [notification, ...this.state.notifications];
        const unreadCount = this.state.unreadCount + (notification.status === 'pending' ? 1 : 0);
        
        this.setState({
            notifications,
            unreadCount
        });
    }
    
    /**
     * Marca notificação como lida
     */
    markNotificationRead(notificationId) {
        const notifications = this.state.notifications.map(n => 
            n.id === notificationId ? { ...n, status: 'sent' } : n
        );
        const unreadCount = notifications.filter(n => n.status === 'pending').length;
        
        this.setState({
            notifications,
            unreadCount
        });
    }
    
    /**
     * Remove notificação
     */
    removeNotification(notificationId) {
        const notifications = this.state.notifications.filter(n => n.id !== notificationId);
        const unreadCount = notifications.filter(n => n.status === 'pending').length;
        
        this.setState({
            notifications,
            unreadCount
        });
    }
    
    /**
     * Atualiza resultados de busca
     */
    setSearchResults(results) {
        this.setState({ searchResults: results });
    }
    
    /**
     * Limpa todos os dados (logout)
     */
    clear() {
        this.setState({
            user: null,
            notifications: [],
            unreadCount: 0,
            isAuthenticated: false,
            searchResults: [],
            selectedAppointment: null
        });
    }
}

// Criar instância global
window.appState = new AppState();

// Auto-inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.appState.init();
    });
} else {
    window.appState.init();
}

// Exemplo de uso:
// window.appState.subscribe((newState, oldState) => {
//     console.log('State changed:', newState);
//     if (newState.unreadCount !== oldState.unreadCount) {
//         console.log('Unread count changed:', newState.unreadCount);
//     }
// });

