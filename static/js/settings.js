/**
 * Settings Page
 */

document.addEventListener('DOMContentLoaded', loadSettings);

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('userSettings') || '{}');
    
    document.getElementById('emailNotif').checked = settings.emailNotif !== false;
    document.getElementById('whatsappNotif').checked = settings.whatsappNotif !== false;
    document.getElementById('publicProfile').checked = settings.publicProfile || false;
    document.getElementById('theme').value = settings.theme || 'light';
}

function switchTab(tab) {
    document.querySelectorAll('.settings-tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    
    document.querySelectorAll('.settings-section').forEach(section => {
        section.style.display = 'none';
    });
    
    document.getElementById(`${tab}Section`).style.display = 'block';
}

function saveSettings() {
    const settings = {
        emailNotif: document.getElementById('emailNotif').checked,
        whatsappNotif: document.getElementById('whatsappNotif').checked,
        publicProfile: document.getElementById('publicProfile').checked,
        theme: document.getElementById('theme').value
    };
    
    localStorage.setItem('userSettings', JSON.stringify(settings));
    showToast('Sucesso', 'Configurações salvas', 'success');
}

window.switchTab = switchTab;
window.saveSettings = saveSettings;

