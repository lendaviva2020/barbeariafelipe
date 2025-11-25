// App.js - JavaScript principal
// API_BASE é definido em config.js (carregado antes)
const API_BASE = window.API_BASE || '/api';

// Funções de autenticação
const auth = {
    getToken() {
        return localStorage.getItem('access_token');
    },
    
    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },
    
    removeTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    },
    
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },
    
    isAuthenticated() {
        return !!this.getToken();
    },
    
    async logout() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
            try {
                await fetch(`${API_BASE}/users/logout/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.getToken()}`
                    },
                    body: JSON.stringify({ refresh: refreshToken })
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
        this.removeTokens();
        window.location.href = '/';
    }
};

// Fetch com autenticação
async function fetchAPI(url, options = {}) {
    const token = auth.getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers,
    });
    
    if (response.status === 401) {
        // Token expirado, fazer logout
        auth.removeTokens();
        window.location.href = '/auth/';
        return;
    }
    
    return response;
}

// Mostrar/ocultar menu do usuário
function updateAuthUI() {
    const user = auth.getUser();
    const userMenu = document.getElementById('userMenu');
    const loginLink = document.getElementById('loginLink');
    
    if (user && userMenu && loginLink) {
        userMenu.style.display = 'flex';
        loginLink.style.display = 'none';
    } else if (userMenu && loginLink) {
        userMenu.style.display = 'none';
        loginLink.style.display = 'block';
    }
}

// Menu mobile toggle
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Deseja realmente sair?')) {
                auth.logout();
            }
        });
    }
    
    // Atualizar UI de autenticação
    updateAuthUI();
});

// Função para formatar data
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Função para formatar moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Mostrar mensagem
function showMessage(element, message, type = 'success') {
    element.style.display = 'block';
    element.className = `message ${type}`;
    element.textContent = message;
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Export functions
window.auth = auth;
window.fetchAPI = fetchAPI;
window.showMessage = showMessage;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;

