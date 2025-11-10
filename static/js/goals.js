/**
 * Goals Page - Sistema completo de metas e objetivos
 * Extraído 100% do React Goals.tsx (556 linhas)
 */

// State
let goals = [];
let barbers = [];
let editingGoal = null;
let isSubmitting = false;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadBarbers();
    await loadGoals();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Goal type change
    const goalTypeSelect = document.getElementById('goal_type');
    if (goalTypeSelect) {
        goalTypeSelect.addEventListener('change', updateTargetValueLabel);
    }
    
    // Form submit
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            submitGoal();
        });
    }
}

// Update target value label based on goal type
function updateTargetValueLabel() {
    const goalType = document.getElementById('goal_type').value;
    const label = document.getElementById('target_value_label');
    const input = document.getElementById('target_value');
    
    const labels = {
        'revenue': 'Valor da Meta (R$) *',
        'appointments': 'Número de Atendimentos *',
        'customer_satisfaction': 'Satisfação do Cliente (%) *'
    };
    
    const placeholders = {
        'revenue': '5000.00',
        'appointments': '100',
        'customer_satisfaction': '95'
    };
    
    const steps = {
        'revenue': '0.01',
        'appointments': '1',
        'customer_satisfaction': '1'
    };
    
    label.textContent = labels[goalType];
    input.placeholder = placeholders[goalType];
    input.step = steps[goalType];
}

// Load barbers
async function loadBarbers() {
    try {
        const response = await fetchAPI('/api/barbeiros/');
        barbers = await response.json();
        
        const select = document.getElementById('barber_id');
        if (select && barbers.length > 0) {
            barbers.forEach(barber => {
                if (barber.active) {
                    const option = document.createElement('option');
                    option.value = barber.id;
                    option.textContent = barber.name;
                    select.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Erro ao carregar barbeiros:', error);
    }
}

// Load goals
async function loadGoals() {
    showLoading();
    
    try {
        const response = await fetchAPI('/api/goals/');
        if (!response.ok) throw new Error('Erro ao carregar metas');
        
        goals = await response.json();
        renderGoals();
        updateGoalsCount();
    } catch (error) {
        console.error('Erro ao carregar metas:', error);
        showError();
    } finally {
        hideLoading();
    }
}

// Render goals
function renderGoals() {
    const grid = document.getElementById('goalsGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (goals.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    grid.innerHTML = goals.map(goal => createGoalCard(goal)).join('');
}

// Create goal card HTML
function createGoalCard(goal) {
    const progress = Math.min((goal.current_value / goal.target_value) * 100, 100);
    const isCompleted = progress >= 100;
    const isExpired = new Date(goal.period_end) < new Date() && !isCompleted;
    const isActive = goal.status === 'active' && !isCompleted && !isExpired;
    
    const barber = goal.barber_id ? barbers.find(b => b.id === goal.barber_id) : null;
    
    return `
        <div class="goal-card ${isCompleted ? 'completed' : ''} ${isExpired ? 'expired' : ''}">
            <!-- Header -->
            <div class="goal-header">
                <div>
                    <div class="goal-title">
                        🎯 ${getGoalTypeLabel(goal.goal_type)}
                    </div>
                    ${barber ? `
                        <div class="goal-barber">
                            👤 ${barber.name}
                        </div>
                    ` : `
                        <div class="goal-barber">Meta Geral da Barbearia</div>
                    `}
                </div>
                ${getStatusBadge(goal, isCompleted, isExpired)}
            </div>
            
            <!-- Progress -->
            <div class="goal-progress">
                <div class="progress-header">
                    <span class="progress-label">Progresso</span>
                    <span class="progress-value">${progress.toFixed(1)}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill ${isCompleted ? 'completed' : ''}" 
                         style="width: ${progress}%"></div>
                </div>
            </div>
            
            <!-- Values -->
            <div class="values-grid">
                <div class="value-item">
                    <p>Atual</p>
                    <p class="value-current">${getValueDisplay(goal.current_value, goal.goal_type)}</p>
                </div>
                <div class="value-item">
                    <p>Meta</p>
                    <p class="value-target">${getValueDisplay(goal.target_value, goal.goal_type)}</p>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="goal-footer">
                <div class="goal-period">
                    📅 ${formatDate(goal.period_start)} - ${formatDate(goal.period_end)}
                </div>
                <div class="goal-actions">
                    ${isActive ? `
                        <button onclick="editGoal('${goal.id}')">
                            ✏️
                        </button>
                    ` : ''}
                    <button class="delete-btn" onclick="deleteGoal('${goal.id}')">
                        🗑️
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Get goal type label
function getGoalTypeLabel(type) {
    const labels = {
        'revenue': 'Faturamento',
        'appointments': 'Atendimentos',
        'customer_satisfaction': 'Satisfação'
    };
    return labels[type] || type;
}

// Get value display
function getValueDisplay(value, type) {
    switch (type) {
        case 'revenue':
            return `R$ ${value.toFixed(2)}`;
        case 'customer_satisfaction':
            return `${value}%`;
        default:
            return value.toString();
    }
}

// Get status badge
function getStatusBadge(goal, isCompleted, isExpired) {
    if (isCompleted) {
        return `<span class="goal-status completed"><span class="trophy-icon">🏆</span>Concluída</span>`;
    }
    if (isExpired) {
        return `<span class="goal-status expired">Expirada</span>`;
    }
    if (goal.status === 'cancelled') {
        return `<span class="goal-status cancelled">Cancelada</span>`;
    }
    return `<span class="goal-status active">Ativa</span>`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// Update goals count
function updateGoalsCount() {
    const count = document.getElementById('goalsCount');
    if (count) {
        const text = goals.length === 1 ? 'meta cadastrada' : 'metas cadastradas';
        count.textContent = `${goals.length} ${text}`;
    }
}

// Open goal dialog
function openGoalDialog() {
    editingGoal = null;
    document.getElementById('goalModalTitle').textContent = 'Nova Meta';
    document.getElementById('goalForm').reset();
    document.getElementById('goalId').value = '';
    document.getElementById('submitBtn').textContent = 'Criar Meta';
    document.getElementById('formError').style.display = 'none';
    
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('period_start').min = today;
    document.getElementById('period_end').min = today;
    
    document.getElementById('goalDialog').style.display = 'flex';
}

// Close goal dialog
function closeGoalDialog() {
    document.getElementById('goalDialog').style.display = 'none';
    editingGoal = null;
}

// Edit goal
function editGoal(id) {
    const goal = goals.find(g => g.id === id);
    if (!goal) return;
    
    editingGoal = goal;
    document.getElementById('goalModalTitle').textContent = 'Editar Meta';
    document.getElementById('goalId').value = goal.id;
    document.getElementById('barber_id').value = goal.barber_id || '';
    document.getElementById('goal_type').value = goal.goal_type;
    document.getElementById('target_value').value = goal.target_value;
    document.getElementById('period_start').value = goal.period_start.split('T')[0];
    document.getElementById('period_end').value = goal.period_end.split('T')[0];
    document.getElementById('submitBtn').textContent = 'Atualizar Meta';
    
    updateTargetValueLabel();
    document.getElementById('goalDialog').style.display = 'flex';
}

// Submit goal
async function submitGoal() {
    if (isSubmitting) return;
    
    const formData = {
        barber_id: document.getElementById('barber_id').value || null,
        goal_type: document.getElementById('goal_type').value,
        target_value: parseFloat(document.getElementById('target_value').value),
        period_start: document.getElementById('period_start').value,
        period_end: document.getElementById('period_end').value
    };
    
    // Validate
    const error = validateGoalForm(formData);
    if (error) {
        showFormError(error);
        return;
    }
    
    isSubmitting = true;
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Salvando...';
    
    try {
        let response;
        if (editingGoal) {
            response = await fetchAPI(`/api/goals/${editingGoal.id}/`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
        } else {
            response = await fetchAPI('/api/goals/', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
        }
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Erro ao salvar meta');
        }
        
        showToast(
            editingGoal ? 'Meta atualizada' : 'Meta criada',
            'Meta salva com sucesso',
            'success'
        );
        
        closeGoalDialog();
        await loadGoals();
    } catch (error) {
        console.error('Erro ao salvar meta:', error);
        showFormError(error.message);
    } finally {
        isSubmitting = false;
        submitBtn.disabled = false;
        submitBtn.textContent = editingGoal ? 'Atualizar Meta' : 'Criar Meta';
    }
}

// Validate goal form
function validateGoalForm(data) {
    if (data.target_value <= 0) {
        return 'O valor da meta deve ser maior que zero';
    }
    
    if (!data.period_start || !data.period_end) {
        return 'As datas de início e fim são obrigatórias';
    }
    
    if (new Date(data.period_start) > new Date(data.period_end)) {
        return 'A data de início deve ser anterior à data de fim';
    }
    
    if (data.goal_type === 'customer_satisfaction' && data.target_value > 100) {
        return 'Satisfação do cliente não pode ser maior que 100%';
    }
    
    return null;
}

// Show form error
function showFormError(message) {
    const errorDiv = document.getElementById('formError');
    errorDiv.textContent = `⚠️ ${message}`;
    errorDiv.style.display = 'flex';
}

// Delete goal
async function deleteGoal(id) {
    if (!confirm('Tem certeza que deseja excluir esta meta? Esta ação não pode ser desfeita.')) {
        return;
    }
    
    try {
        const response = await fetchAPI(`/api/goals/${id}/`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao excluir meta');
        
        showToast('Meta excluída', 'Meta excluída com sucesso', 'success');
        await loadGoals();
    } catch (error) {
        console.error('Erro ao excluir meta:', error);
        showToast('Erro', 'Não foi possível excluir a meta', 'error');
    }
}

// Show loading
function showLoading() {
    document.getElementById('loadingState').style.display = 'grid';
    document.getElementById('goalsGrid').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

// Hide loading
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

// Show error
function showError() {
    document.getElementById('emptyState').innerHTML = `
        <div class="empty-icon">⚠️</div>
        <h3>Erro ao carregar</h3>
        <p>Não foi possível carregar as metas. Tente novamente.</p>
        <button class="btn btn-primary" onclick="loadGoals()">Tentar Novamente</button>
    `;
    document.getElementById('emptyState').style.display = 'block';
}

// Show toast
function showToast(title, message, type = 'success') {
    if (window.showToast) {
        window.showToast(title, message, type);
    } else {
        alert(`${title}: ${message}`);
    }
}

// Export functions for inline onclick
window.openGoalDialog = openGoalDialog;
window.closeGoalDialog = closeGoalDialog;
window.editGoal = editGoal;
window.deleteGoal = deleteGoal;
window.submitGoal = submitGoal;

