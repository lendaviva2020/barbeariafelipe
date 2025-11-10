/**
 * Commissions System
 */

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

document.addEventListener('DOMContentLoaded', () => {
    populateMonthYear();
    loadCommissions();
});

function populateMonthYear() {
    const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
    const monthSelect = document.getElementById('monthSelect');
    months.forEach((m, i) => {
        monthSelect.innerHTML += `<option value="${i}" ${i === currentMonth ? 'selected' : ''}>${m}</option>`;
    });
    
    const yearSelect = document.getElementById('yearSelect');
    for (let y = currentYear; y >= currentYear - 3; y--) {
        yearSelect.innerHTML += `<option value="${y}" ${y === currentYear ? 'selected' : ''}>${y}</option>`;
    }
}

async function loadCommissions() {
    currentMonth = parseInt(document.getElementById('monthSelect').value);
    currentYear = parseInt(document.getElementById('yearSelect').value);
    
    try {
        const response = await fetchAPI(`/api/commissions/?month=${currentMonth + 1}&year=${currentYear}`);
        const data = await response.json();
        
        document.getElementById('totalServices').textContent = data.total_services || 0;
        document.getElementById('totalRevenue').textContent = `R$ ${(data.total_revenue || 0).toFixed(2)}`;
        document.getElementById('commissionAmount').textContent = `R$ ${(data.commission_amount || 0).toFixed(2)}`;
        document.getElementById('paymentStatus').textContent = data.is_paid ? 'Pago ✓' : 'Pendente';
    } catch (error) {
        console.error(error);
    }
}

function previousMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    document.getElementById('monthSelect').value = currentMonth;
    document.getElementById('yearSelect').value = currentYear;
    loadCommissions();
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    document.getElementById('monthSelect').value = currentMonth;
    document.getElementById('yearSelect').value = currentYear;
    loadCommissions();
}

window.previousMonth = previousMonth;
window.nextMonth = nextMonth;
window.loadCommissions = loadCommissions;

