// Authentication JavaScript
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
            
            if (response.ok) {
                // Salvar tokens e usuário
                auth.setTokens(result.tokens.access, result.tokens.refresh);
                auth.setUser(result.user);
                
                showMessage(authMessage, 'Login realizado com sucesso!', 'success');
                
                // Redirecionar
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage(authMessage, result.error || 'Erro ao fazer login', 'error');
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
            
            if (response.ok) {
                // Salvar tokens e usuário
                auth.setTokens(result.tokens.access, result.tokens.refresh);
                auth.setUser(result.user);
                
                showMessage(authMessage, 'Conta criada com sucesso!', 'success');
                
                // Redirecionar
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                const errorMsg = result.email?.[0] || result.error || 'Erro ao criar conta';
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

