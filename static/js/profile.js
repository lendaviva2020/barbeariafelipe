/**
 * Profile Page - Extraído de Profile.tsx (600+ linhas)
 */

let userData = null;

document.addEventListener('DOMContentLoaded', async () => {
    if (!auth.isAuthenticated()) {
        window.location.href = '/auth/?redirect=/perfil/';
        return;
    }
    
    await loadProfile();
    await loadStats();
    await checkAdminPermission(); // Verificar se usuário tem permissão de admin
});

async function loadProfile() {
    try {
        const response = await fetchAPI('/api/users/me/');
        userData = await response.json();
        
        // Update form
        document.getElementById('displayName').value = userData.name || '';
        document.getElementById('email').value = userData.email || '';
        document.getElementById('phone').value = userData.phone || '';
        
        // Update avatar
        const initials = (userData.name || userData.email || 'U')[0].toUpperCase();
        document.getElementById('avatarInitials').textContent = initials;
        
        if (userData.avatar_url) {
            const img = document.getElementById('avatarImage');
            img.src = userData.avatar_url;
            img.style.display = 'block';
            document.getElementById('avatarInitials').style.display = 'none';
        }
    } catch (error) {
        console.error('Erro ao carregar perfil:', error);
        showToast('Erro', 'Não foi possível carregar o perfil', 'error');
    }
}

async function loadStats() {
    try {
        const response = await fetchAPI('/api/agendamentos/');
        const appointments = await response.json();
        
        const completed = appointments.filter(a => a.status === 'completed').length;
        
        document.getElementById('totalAppointments').textContent = appointments.length;
        document.getElementById('completedAppointments').textContent = completed;
        
        if (userData?.created_at) {
            const memberDate = new Date(userData.created_at);
            document.getElementById('memberSince').textContent = 
                memberDate.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

/**
 * Verifica se o usuário atual tem permissão de administrador
 * Consulta o banco de dados para verificar se o email está autorizado
 */
async function checkAdminPermission() {
    try {
        // Aguardar um pouco para garantir que app.js foi carregado
        if (typeof fetchAPI === 'undefined') {
            console.warn('fetchAPI não disponível, tentando novamente em 100ms...');
            setTimeout(checkAdminPermission, 100);
            return;
        }
        
        const response = await fetchAPI('/api/users/check-admin/');
        
        if (!response.ok) {
            console.log('Erro ao verificar permissão de admin:', response.status);
            return;
        }
        
        const data = await response.json();
        
        // Se o usuário é admin, mostrar o botão
        if (data.is_admin) {
            const adminButtonContainer = document.getElementById('admin-button-container');
            if (adminButtonContainer) {
                adminButtonContainer.style.display = 'block';
                console.log('✅ Usuário autorizado como administrador. Email:', data.email);
            }
        } else {
            console.log('❌ Usuário não tem permissão de administrador. Email:', data.email);
        }
    } catch (error) {
        console.error('Erro ao verificar permissão de admin:', error);
    }
}

async function saveProfile(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('displayName').value,
        phone: document.getElementById('phone').value
    };
    
    try {
        const response = await fetchAPI('/api/users/me/', {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Erro ao salvar');
        
        showToast('Sucesso', 'Perfil atualizado com sucesso', 'success');
        userData = await response.json();
    } catch (error) {
        console.error(error);
        showToast('Erro', 'Não foi possível atualizar o perfil', 'error');
    }
}

function cancelEdit() {
    if (userData) {
        document.getElementById('displayName').value = userData.name || '';
        document.getElementById('phone').value = userData.phone || '';
    }
}

function triggerAvatarUpload() {
    document.getElementById('avatarInput').click();
}

async function handleAvatarUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file
    if (!file.type.startsWith('image/')) {
        showToast('Erro', 'Arquivo deve ser uma imagem', 'error');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showToast('Erro', 'Imagem deve ter no máximo 5MB', 'error');
        return;
    }
    
    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.getElementById('avatarImage');
        img.src = e.target.result;
        img.style.display = 'block';
        document.getElementById('avatarInitials').style.display = 'none';
    };
    reader.readAsDataURL(file);
    
    // TODO: Upload to server
    showToast('Aviso', 'Upload de avatar será implementado em breve', 'info');
}

async function changePassword(event) {
    event.preventDefault();
    
    const current = document.getElementById('currentPassword').value;
    const newPass = document.getElementById('newPassword').value;
    const confirm = document.getElementById('confirmPassword').value;
    
    if (newPass !== confirm) {
        showToast('Erro', 'As senhas não coincidem', 'error');
        return;
    }
    
    if (newPass.length < 6) {
        showToast('Erro', 'Senha deve ter no mínimo 6 caracteres', 'error');
        return;
    }
    
    try {
        const response = await fetchAPI('/api/users/change-password/', {
            method: 'POST',
            body: JSON.stringify({ current_password: current, new_password: newPass })
        });
        
        if (!response.ok) throw new Error('Erro ao alterar senha');
        
        showToast('Sucesso', 'Senha alterada com sucesso', 'success');
        document.getElementById('passwordForm').reset();
    } catch (error) {
        showToast('Erro', 'Não foi possível alterar a senha. Verifique a senha atual.', 'error');
    }
}

async function deleteAccount() {
    if (!confirm('⚠️ ATENÇÃO: Deseja realmente deletar sua conta? Esta ação é IRREVERSÍVEL!')) {
        return;
    }
    
    if (!confirm('Tem CERTEZA ABSOLUTA? Todos os seus dados serão perdidos permanentemente.')) {
        return;
    }
    
    try {
        const response = await fetchAPI('/api/users/me/', { method: 'DELETE' });
        
        if (!response.ok) throw new Error('Erro ao deletar conta');
        
        showToast('Conta deletada', 'Sua conta foi removida com sucesso', 'info');
        
        setTimeout(() => {
            localStorage.clear();
            window.location.href = '/';
        }, 2000);
    } catch (error) {
        showToast('Erro', 'Não foi possível deletar a conta', 'error');
    }
}

window.saveProfile = saveProfile;
window.cancelEdit = cancelEdit;
window.triggerAvatarUpload = triggerAvatarUpload;
window.handleAvatarUpload = handleAvatarUpload;
window.changePassword = changePassword;
window.deleteAccount = deleteAccount;

