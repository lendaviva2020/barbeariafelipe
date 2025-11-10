/**
 * Recurring Appointments
 */

document.addEventListener('DOMContentLoaded', loadRecurring);

async function loadRecurring() {
    try {
        const response = await fetchAPI('/api/recurring/');
        const recurring = await response.json();
        renderRecurring(recurring);
    } catch (error) {
        console.error(error);
    }
}

function renderRecurring(recurring) {
    const list = document.getElementById('recurringList');
    if (!recurring || recurring.length === 0) {
        list.innerHTML = '<p class="empty">Nenhum agendamento recorrente.</p>';
        return;
    }
    
    list.innerHTML = recurring.map(r => `
        <div class="recurring-card">
            <h3>${r.service_name}</h3>
            <p>🔄 ${getFrequencyLabel(r.frequency)}</p>
            <p>📅 ${getDayLabel(r.day_of_week)} às ${r.time}</p>
            <button class="btn-sm btn-danger" onclick="deleteRecurring(${r.id})">Cancelar</button>
        </div>
    `).join('');
}

function getFrequencyLabel(freq) {
    const labels = { weekly: 'Semanal', biweekly: 'Quinzenal', monthly: 'Mensal' };
    return labels[freq] || freq;
}

function getDayLabel(day) {
    const days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
    return days[day] || day;
}

function openRecurringDialog() {
    document.getElementById('recurringDialog').style.display = 'flex';
}

function closeRecurringDialog() {
    document.getElementById('recurringDialog').style.display = 'none';
}

async function submitRecurring() {
    const data = {
        frequency: document.getElementById('frequency').value,
        day_of_week: document.getElementById('dayOfWeek').value,
        time: document.getElementById('time').value
    };
    
    try {
        await fetchAPI('/api/recurring/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showToast('Sucesso', 'Agendamento recorrente criado', 'success');
        closeRecurringDialog();
        loadRecurring();
    } catch (error) {
        showToast('Erro', 'Não foi possível criar', 'error');
    }
}

async function deleteRecurring(id) {
    if (!confirm('Cancelar agendamento recorrente?')) return;
    
    try {
        await fetchAPI(`/api/recurring/${id}/`, { method: 'DELETE' });
        showToast('Sucesso', 'Cancelado', 'success');
        loadRecurring();
    } catch (error) {
        showToast('Erro', 'Não foi possível cancelar', 'error');
    }
}

window.openRecurringDialog = openRecurringDialog;
window.closeRecurringDialog = closeRecurringDialog;
window.submitRecurring = submitRecurring;
window.deleteRecurring = deleteRecurring;

