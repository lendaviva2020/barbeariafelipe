// Authentication JavaScript
// Garantir que o objeto auth existe (definir se não existir)
if (typeof auth === 'undefined') {
    window.auth = {
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
        }
    };
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const toggleAuth = document.getElementById('toggleAuth');
    const toggleText = document.getElementById('toggleText');
    const authMessage = document.getElementById('authMessage');
    
    let isLoginMode = true;
    
    // Toggle entre login e registro
    toggleAuth.addEventListener('click', (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;
        
        if (isLoginMode) {
            loginForm.style.display = 'block';
            registerForm.style.display = 'none';
            toggleText.innerHTML = 'Não tem uma conta? <a href="#" id="toggleAuth">Criar conta</a>';
        } else {
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
            toggleText.innerHTML = 'Já tem uma conta? <a href="#" id="toggleAuth">Entrar</a>';
        }
        
        // Re-bind o event listener
        document.getElementById('toggleAuth').addEventListener('click', arguments.callee);
    });
    
    // Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const loginBtn = document.getElementById('loginBtn');
        const loginBtnText = document.getElementById('loginBtnText');
        const loginBtnLoader = document.getElementById('loginBtnLoader');
        
        // Mostrar loader
        loginBtnText.style.display = 'none';
        loginBtnLoader.style.display = 'inline-block';
        loginBtn.disabled = true;
        
        const formData = new FormData(loginForm);
        const data = {
            email: formData.get('email'),
            password: formData.get('password'),
        };
        
        try {
            const response = await fetch('/api/users/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data),
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                // Salvar tokens e usuário
                if (result.tokens) {
                    auth.setTokens(result.tokens.access, result.tokens.refresh);
                }
                if (result.user) {
                    auth.setUser(result.user);
                }
                
                // Mostrar mensagem de sucesso
                const successMsg = result.message || 'Login realizado com sucesso!';
                showMessage(authMessage, successMsg, 'success');
                
                // Redirecionar para página de agendamento ou home
                setTimeout(() => {
                    const redirectUrl = new URLSearchParams(window.location.search).get('next') || '/agendar/';
                    window.location.href = redirectUrl;
                }, 1000);
            } else {
                const errorMsg = result.error || 'Email ou senha incorretos';
                showMessage(authMessage, errorMsg, 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showMessage(authMessage, 'Erro ao fazer login. Tente novamente.', 'error');
        } finally {
            loginBtnText.style.display = 'inline';
            loginBtnLoader.style.display = 'none';
            loginBtn.disabled = false;
        }
    });
    
    // Register
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const registerBtn = document.getElementById('registerBtn');
        const registerBtnText = document.getElementById('registerBtnText');
        const registerBtnLoader = document.getElementById('registerBtnLoader');
        
        const formData = new FormData(registerForm);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            password: formData.get('password'),
            password_confirm: formData.get('password_confirm'),
        };
        
        // Validação básica
        if (data.password !== data.password_confirm) {
            showMessage(authMessage, 'As senhas não coincidem', 'error');
            return;
        }
        
        if (data.password.length < 6) {
            showMessage(authMessage, 'A senha deve ter no mínimo 6 caracteres', 'error');
            return;
        }
        
        // Mostrar loader
        registerBtnText.style.display = 'none';
        registerBtnLoader.style.display = 'inline-block';
        registerBtn.disabled = true;
        
        try {
            const response = await fetch('/api/users/register/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data),
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                // Salvar tokens e usuário
                if (result.tokens) {
                    auth.setTokens(result.tokens.access, result.tokens.refresh);
                }
                if (result.user) {
                    auth.setUser(result.user);
                }
                
                // Mostrar mensagem de sucesso
                const successMsg = result.message || 'Conta criada com sucesso! Bem-vindo à Barbearia Francisco!';
                showMessage(authMessage, successMsg, 'success');
                
                // Redirecionar para página de agendamento ou home
                setTimeout(() => {
                    const redirectUrl = result.redirect || new URLSearchParams(window.location.search).get('next') || '/agendar/';
                    window.location.href = redirectUrl;
                }, 2000);
            } else {
                const errorMsg = result.error || result.email?.[0] || 'Erro ao criar conta';
                showMessage(authMessage, errorMsg, 'error');
            }
        } catch (error) {
            console.error('Register error:', error);
            showMessage(authMessage, 'Erro ao criar conta. Tente novamente.', 'error');
        } finally {
            registerBtnText.style.display = 'inline';
            registerBtnLoader.style.display = 'none';
            registerBtn.disabled = false;
        }
    });
});

// Função para mostrar mensagens
function showMessage(element, message, type) {
    if (!element) return;
    
    element.textContent = message;
    element.className = `auth-message ${type}`;
    element.style.display = 'block';
    
    // Remover mensagem após 5 segundos
    setTimeout(() => {
        element.style.display = 'none';
        element.textContent = '';
    }, 5000);
}

