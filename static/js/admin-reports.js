/**
 * Admin Reports - Gráficos e exportação
 */

let charts = {};
let currentType = 'financial';

document.addEventListener('DOMContentLoaded', async () => {
    await loadReportData();
    initCharts();
});

async function loadReportData() {
    // Mock data - seria carregado da API
    return {
        revenue: [5000, 6200, 5800, 7100, 6500],
        payments: { cash: 30, credit: 45, debit: 15, pix: 10 },
        services: { 'Corte': 50, 'Barba': 30, 'Combo': 40 },
        barbers: { 'João': 8500, 'Pedro': 7200, 'Carlos': 6800 }
    };
}

function initCharts() {
    // Revenue Chart
    charts.revenue = new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
            datasets: [{
                label: 'Faturamento (R$)',
                data: [5000, 6200, 5800, 7100, 6500],
                borderColor: '#C9A961',
                backgroundColor: 'rgba(201, 169, 97, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Payment Chart
    charts.payment = new Chart(document.getElementById('paymentChart'), {
        type: 'pie',
        data: {
            labels: ['Dinheiro', 'Crédito', 'Débito', 'PIX'],
            datasets: [{
                data: [30, 45, 15, 10],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6']
            }]
        }
    });

    // Popular Services Chart
    charts.services = new Chart(document.getElementById('popularServicesChart'), {
        type: 'bar',
        data: {
            labels: ['Corte Social', 'Barba Completa', 'Combo Premium'],
            datasets: [{
                label: 'Agendamentos',
                data: [50, 30, 40],
                backgroundColor: '#C9A961'
            }]
        }
    });

    // Barber Performance Chart
    charts.barberPerf = new Chart(document.getElementById('barberPerformanceChart'), {
        type: 'bar',
        data: {
            labels: ['João Silva', 'Pedro Santos', 'Carlos Oliveira'],
            datasets: [{
                label: 'Faturamento (R$)',
                data: [8500, 7200, 6800],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b']
            }]
        }
    });

    // New Clients Chart
    charts.clients = new Chart(document.getElementById('newClientsChart'), {
        type: 'line',
        data: {
            labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
            datasets: [{
                label: 'Novos Clientes',
                data: [12, 15, 18, 22],
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                tension: 0.4
            }]
        }
    });
}

function setReportType(type) {
    currentType = type;
    
    // Update tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.type === type);
    });
    
    // Show/hide sections
    document.querySelectorAll('.report-section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(`${type}Section`).style.display = 'grid';
}

function changeTimeRange() {
    const range = document.getElementById('timeRange').value;
    // Reload charts with new range
    loadReportData().then(initCharts);
}

function exportPDF() {
    showToast('Exportando', 'Gerando PDF...', 'info');
    // TODO: Implement PDF export
}

function exportExcel() {
    showToast('Exportando', 'Gerando Excel...', 'info');
    // TODO: Implement Excel export
}

window.setReportType = setReportType;
window.changeTimeRange = changeTimeRange;
window.exportPDF = exportPDF;
window.exportExcel = exportExcel;

