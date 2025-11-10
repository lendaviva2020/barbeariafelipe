/**
 * ADMIN DASHBOARD - Extraído de admin/Dashboard.tsx (826 linhas)
 * Gráficos, métricas, filtros avançados
 */

// ========== CHART.JS CONFIGURATION ==========
const CHART_COLORS = {
    primary: 'rgba(201, 169, 97, 1)', // Gold
    primaryLight: 'rgba(212, 184, 118, 1)',
    secondary: 'rgba(139, 38, 53, 1)', // Burgundy
    success: 'rgba(16, 185, 129, 1)',
    warning: 'rgba(245, 158, 11, 1)',
    danger: 'rgba(239, 68, 68, 1)',
    info: 'rgba(59, 130, 246, 1)',
    grid: 'rgba(92, 64, 51, 0.1)',
    text: 'rgba(232, 217, 197, 0.8)'
};

const CHART_OPTIONS_BASE = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: CHART_COLORS.text,
                font: {
                    family: 'Inter',
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(44, 24, 16, 0.95)',
            titleColor: CHART_COLORS.primary,
            bodyColor: CHART_COLORS.text,
            borderColor: CHART_COLORS.primary,
            borderWidth: 1,
            padding: 12,
            displayColors: true,
            titleFont: {
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                size: 13
            }
        }
    },
    scales: {
        x: {
            grid: {
                color: CHART_COLORS.grid
            },
            ticks: {
                color: CHART_COLORS.text
            }
        },
        y: {
            grid: {
                color: CHART_COLORS.grid
            },
            ticks: {
                color: CHART_COLORS.text
            }
        }
    }
};

// ========== GLOBAL STATE ==========
const adminState = {
    timeRange: '30days',
    stats: null,
    appointments: [],
    charts: {},
    activeFilter: 'all'
};

// ========== API CALLS ==========
async function fetchDashboardStats(startDate, endDate) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/admin/dashboard-stats/?start_date=${startDate}&end_date=${endDate}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Erro ao carregar estatísticas');
        
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar stats:', error);
        return null;
    }
}

async function fetchAppointments(status = null) {
    try {
        const token = localStorage.getItem('access_token');
        const url = status ? `/api/admin/agendamentos/?status=${status}` : '/api/admin/agendamentos/';
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Erro ao carregar agendamentos');
        
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar agendamentos:', error);
        return [];
    }
}

// ========== STATS RENDERING ==========
function renderStats(stats) {
    if (!stats) return;
    
    // Update stat cards
    document.getElementById('stat_revenue').textContent = formatCurrency(stats.total_revenue || 0);
    document.getElementById('stat_appointments').textContent = stats.total_appointments || 0;
    document.getElementById('stat_completed').textContent = stats.completed_appointments || 0;
    document.getElementById('stat_pending').textContent = stats.pending_appointments || 0;
    document.getElementById('stat_barbers').textContent = stats.active_barbers || 0;
    document.getElementById('stat_avg_ticket').textContent = formatCurrency(stats.average_ticket || 0);
    
    // Update today stats
    if (stats.today) {
        document.getElementById('today_completed').textContent = stats.today.completed || 0;
        document.getElementById('today_pending').textContent = stats.today.pending || 0;
        document.getElementById('today_cancelled').textContent = stats.today.cancelled || 0;
    }
}

// ========== CHARTS ==========

// Revenue Chart (Line Chart)
function createRevenueChart(data) {
    const ctx = document.getElementById('revenueChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (adminState.charts.revenue) {
        adminState.charts.revenue.destroy();
    }
    
    adminState.charts.revenue = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Faturamento (R$)',
                data: data.map(d => d.revenue),
                borderColor: CHART_COLORS.primary,
                backgroundColor: `${CHART_COLORS.primary}33`,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            ...CHART_OPTIONS_BASE,
            plugins: {
                ...CHART_OPTIONS_BASE.plugins,
                title: {
                    display: true,
                    text: 'Faturamento Diário',
                    color: CHART_COLORS.primary,
                    font: {
                        size: 16,
                        weight: 'bold',
                        family: 'Playfair Display'
                    }
                }
            }
        }
    });
}

// Status Distribution (Pie Chart)
function createStatusChart(stats) {
    const ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    if (adminState.charts.status) {
        adminState.charts.status.destroy();
    }
    
    const data = [
        stats.completed_appointments || 0,
        stats.confirmed_appointments || 0,
        stats.pending_appointments || 0,
        stats.cancelled_appointments || 0
    ];
    
    adminState.charts.status = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Completados', 'Confirmados', 'Pendentes', 'Cancelados'],
            datasets: [{
                data: data,
                backgroundColor: [
                    CHART_COLORS.success,
                    CHART_COLORS.info,
                    CHART_COLORS.warning,
                    CHART_COLORS.danger
                ],
                borderWidth: 2,
                borderColor: 'rgba(44, 24, 16, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: CHART_COLORS.text,
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Distribuição de Status',
                    color: CHART_COLORS.primary,
                    font: {
                        size: 16,
                        weight: 'bold',
                        family: 'Playfair Display'
                    }
                },
                tooltip: {
                    ...CHART_OPTIONS_BASE.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Services Chart (Bar Chart)
function createServicesChart(services) {
    const ctx = document.getElementById('servicesChart');
    if (!ctx) return;
    
    if (adminState.charts.services) {
        adminState.charts.services.destroy();
    }
    
    adminState.charts.services = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: services.map(s => s.name.substring(0, 15)),
            datasets: [{
                label: 'Agendamentos',
                data: services.map(s => s.count),
                backgroundColor: CHART_COLORS.primary,
                borderColor: CHART_COLORS.primaryLight,
                borderWidth: 1
            }]
        },
        options: {
            ...CHART_OPTIONS_BASE,
            plugins: {
                ...CHART_OPTIONS_BASE.plugins,
                title: {
                    display: true,
                    text: 'Serviços Mais Populares',
                    color: CHART_COLORS.primary,
                    font: {
                        size: 16,
                        weight: 'bold',
                        family: 'Playfair Display'
                    }
                }
            }
        }
    });
}

// Barbers Performance Chart
function createBarbersChart(barbers) {
    const ctx = document.getElementById('barbersChart');
    if (!ctx) return;
    
    if (adminState.charts.barbers) {
        adminState.charts.barbers.destroy();
    }
    
    adminState.charts.barbers = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: barbers.map(b => b.name),
            datasets: [
                {
                    label: 'Faturamento (R$)',
                    data: barbers.map(b => b.revenue),
                    backgroundColor: CHART_COLORS.primary,
                    yAxisID: 'y'
                },
                {
                    label: 'Eficiência (%)',
                    data: barbers.map(b => b.efficiency),
                    backgroundColor: CHART_COLORS.secondary,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    labels: {
                        color: CHART_COLORS.text
                    }
                },
                title: {
                    display: true,
                    text: 'Performance dos Barbeiros',
                    color: CHART_COLORS.primary,
                    font: {
                        size: 16,
                        weight: 'bold',
                        family: 'Playfair Display'
                    }
                },
                tooltip: CHART_OPTIONS_BASE.plugins.tooltip
            },
            scales: {
                x: {
                    grid: {
                        color: CHART_COLORS.grid
                    },
                    ticks: {
                        color: CHART_COLORS.text
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    grid: {
                        color: CHART_COLORS.grid
                    },
                    ticks: {
                        color: CHART_COLORS.text
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    },
                    ticks: {
                        color: CHART_COLORS.text
                    }
                }
            }
        }
    });
}

// ========== APPOINTMENTS TABLE ==========
function renderAppointments(appointments) {
    const container = document.getElementById('appointmentsList');
    if (!container) return;
    
    if (appointments.length === 0) {
        container.innerHTML = '<p class="text-center">Nenhum agendamento encontrado</p>';
        return;
    }
    
    const html = `
        <div class="appointments-table">
            <table>
                <thead>
                    <tr>
                        <th>Cliente</th>
                        <th>Serviço</th>
                        <th>Barbeiro</th>
                        <th>Data/Hora</th>
                        <th>Status</th>
                        <th>Valor</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${appointments.map(apt => `
                        <tr>
                            <td>
                                <div class="customer-info">
                                    <strong>${apt.customer_name}</strong>
                                    <small>${apt.customer_phone}</small>
                                </div>
                            </td>
                            <td>${apt.service}</td>
                            <td>${apt.barber}</td>
                            <td>
                                ${new Date(apt.date).toLocaleDateString('pt-BR')}<br>
                                <small>${apt.time}</small>
                            </td>
                            <td>
                                <span class="status-badge status-${apt.status}">
                                    ${getStatusLabel(apt.status)}
                                </span>
                            </td>
                            <td>${formatCurrency(apt.price)}</td>
                            <td>
                                <div class="action-buttons">
                                    ${apt.status === 'pending' ? `
                                        <button onclick="updateStatus(${apt.id}, 'confirmed')" class="btn-action btn-success" title="Confirmar">✓</button>
                                        <button onclick="updateStatus(${apt.id}, 'cancelled')" class="btn-action btn-danger" title="Cancelar">✗</button>
                                    ` : ''}
                                    ${apt.status === 'confirmed' ? `
                                        <button onclick="updateStatus(${apt.id}, 'completed')" class="btn-action btn-success" title="Completar">✓</button>
                                    ` : ''}
                                </div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// ========== UTILITY FUNCTIONS ==========
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function getStatusLabel(status) {
    const labels = {
        'pending': 'Pendente',
        'confirmed': 'Confirmado',
        'completed': 'Completado',
        'cancelled': 'Cancelado'
    };
    return labels[status] || status;
}

function getDateRange(range) {
    const now = new Date();
    let start, end;
    
    switch (range) {
        case '7days':
            start = new Date(now - 7 * 24 * 60 * 60 * 1000);
            break;
        case '30days':
            start = new Date(now - 30 * 24 * 60 * 60 * 1000);
            break;
        case '90days':
            start = new Date(now - 90 * 24 * 60 * 60 * 1000);
            break;
        default:
            start = new Date(now - 30 * 24 * 60 * 60 * 1000);
    }
    
    end = now;
    
    return {
        start: start.toISOString().split('T')[0],
        end: end.toISOString().split('T')[0]
    };
}

// ========== ACTIONS ==========
async function updateStatus(appointmentId, newStatus) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/api/admin/update-agendamento-status/${appointmentId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (!response.ok) throw new Error('Erro ao atualizar status');
        
        alert('Status atualizado com sucesso!');
        loadAppointments(adminState.activeFilter);
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
        alert('Erro ao atualizar status');
    }
}

async function refreshStats() {
    const range = getDateRange(adminState.timeRange);
    const stats = await fetchDashboardStats(range.start, range.end);
    
    if (stats) {
        adminState.stats = stats;
        renderStats(stats);
        
        // Update charts with mock data for demo
        const mockRevenueData = generateMockRevenueData(30);
        createRevenueChart(mockRevenueData);
        createStatusChart(stats);
    }
}

async function loadAppointments(status = 'all') {
    adminState.activeFilter = status;
    
    // Update filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.status === status);
    });
    
    const appointments = await fetchAppointments(status === 'all' ? null : status);
    adminState.appointments = appointments;
    renderAppointments(appointments);
}

// ========== MOCK DATA GENERATORS (for demo) ==========
function generateMockRevenueData(days) {
    const data = [];
    for (let i = days; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        data.push({
            date: date.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }),
            revenue: Math.random() * 2000 + 1000
        });
    }
    return data;
}

// ========== ADMIN TABS ==========
function initAdminTabs() {
    const tabs = document.querySelectorAll('.admin-tab');
    const contents = document.querySelectorAll('.admin-tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active content
            contents.forEach(c => {
                c.style.display = c.dataset.content === targetTab ? 'block' : 'none';
            });
            
            // Load data for specific tab
            if (targetTab === 'agendamentos') {
                loadAppointments('all');
            }
        });
    });
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    // Check auth
    if (!localStorage.getItem('access_token')) {
        window.location.href = '/auth/login/';
        return;
    }
    
    // Initialize tabs
    initAdminTabs();
    
    // Load initial data
    refreshStats();
    
    // Time range selector
    const timeRangeSelect = document.getElementById('timeRange');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', (e) => {
            adminState.timeRange = e.target.value;
            refreshStats();
        });
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshStats);
    }
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            loadAppointments(btn.dataset.status);
        });
    });
});

// Load Chart.js from CDN
if (!window.Chart) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
    document.head.appendChild(script);
}
