/**
 * Contact Page - Form validation and submission
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
});

async function handleSubmit(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        phone: document.getElementById('contactPhone').value,
        message: document.getElementById('contactMessage').value
    };
    
    // Validation
    if (!formData.name || !formData.email || !formData.message) {
        showToast('Erro', 'Preencha todos os campos obrigatórios', 'error');
        return;
    }
    
    if (!validateEmail(formData.email)) {
        showToast('Erro', 'Email inválido', 'error');
        return;
    }
    
    try {
        // TODO: Implement backend endpoint
        showToast('Sucesso', 'Mensagem enviada! Entraremos em contato em breve.', 'success');
        event.target.reset();
    } catch (error) {
        showToast('Erro', 'Não foi possível enviar a mensagem', 'error');
    }
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

