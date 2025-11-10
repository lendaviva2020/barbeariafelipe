/**
 * Admin Promotions - Sistema de promoções automáticas
 * Extraído de Promotions.tsx (687 linhas)
 */

let promotions = [];
let currentFilter = 'active';
let editingPromotion = null;

document.addEventListener('DOMContentLoaded', loadPromotions);

async function loadPromotions() {
    try {
        const response = await fetchAPI('/api/admin/promotions/');
        promotions = await response.json();
        updateCounts();
        renderPromotions();
    } catch (error) {
        console.error(error);
    }
}

function updateCounts() {
    const now = new Date();
    const active = promotions.filter(p => 
        p.active && 
        (!p.start_date || new Date(p.start_date) <= now) &&
        (!p.end_date || new Date(p.end_date) >= now)
    ).length;
    
    const inactive = promotions.filter(p => !p.active).length;
    const expired = promotions.filter(p => 
        p.active && p.end_date && new Date(p.end_date) < now
    ).length;
    
    document.getElementById('countActive').textContent = active;
    document.getElementById('countInactive').textContent = inactive;
    document.getElementById('countExpired').textContent = expired;
}

function setFilter(filter) {
    currentFilter = filter;
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    renderPromotions();
}

function renderPromotions() {
    const now = new Date();
    const filtered = promotions.filter(p => {
        if (currentFilter === 'active') {
            return p.active && 
                   (!p.start_date || new Date(p.start_date) <= now) &&
                   (!p.end_date || new Date(p.end_date) >= now);
        } else if (currentFilter === 'inactive') {
            return !p.active;
        } else if (currentFilter === 'expired') {
            return p.active && p.end_date && new Date(p.end_date) < now;
        }
        return true;
    });
    
    const grid = document.getElementById('promotionsGrid');
    const empty = document.getElementById('emptyState');
    
    if (filtered.length === 0) {
        grid.style.display = 'none';
        empty.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    empty.style.display = 'none';
    
    grid.innerHTML = filtered.map(promo => `
        <div class="promotion-card ${!promo.active ? 'inactive' : ''}">
            <div class="promotion-header">
                <div>
                    <h3>${promo.name}</h3>
                    <span class="promotion-type-badge ${promo.promotion_type}">
                        ${getPromotionTypeIcon(promo.promotion_type)} ${getPromotionTypeLabel(promo.promotion_type)}
                    </span>
                </div>
                <div class="promotion-toggle">
                    <input type="checkbox" ${promo.active ? 'checked' : ''} 
                           onchange="togglePromotion(${promo.id}, this.checked)">
                </div>
            </div>
            
            <p class="promotion-description">${promo.description || ''}</p>
            
            <div class="promotion-discount">
                ${promo.discount_type === 'percentage' 
                    ? `<strong>${promo.discount_value}%</strong> de desconto`
                    : `<strong>R$ ${parseFloat(promo.discount_value).toFixed(2)}</strong> de desconto`}
            </div>
            
            ${promo.conditions && Object.keys(promo.conditions).length > 0 ? `
                <div class="promotion-conditions">
                    <strong>Condições:</strong>
                    <pre>${JSON.stringify(promo.conditions, null, 2)}</pre>
                </div>
            ` : ''}
            
            ${promo.start_date || promo.end_date ? `
                <div class="promotion-period">
                    📅 ${promo.start_date ? formatDate(promo.start_date) : 'Sem início'} - 
                    ${promo.end_date ? formatDate(promo.end_date) : 'Sem fim'}
                </div>
            ` : ''}
            
            <div class="promotion-actions">
                <button class="btn-sm btn-outline" onclick="editPromotion(${promo.id})">✏️ Editar</button>
                <button class="btn-sm btn-danger" onclick="deletePromotion(${promo.id})">🗑️ Excluir</button>
            </div>
        </div>
    `).join('');
}

function getPromotionTypeIcon(type) {
    const icons = {
        'happy_hour': '⏰',
        'first_visit': '🎁',
        'birthday': '🎂',
        'bulk_discount': '👥',
        'loyalty_bonus': '⭐',
        'seasonal': '🌟'
    };
    return icons[type] || '⚡';
}

function getPromotionTypeLabel(type) {
    const labels = {
        'happy_hour': 'Happy Hour',
        'first_visit': 'Primeira Visita',
        'birthday': 'Aniversário',
        'bulk_discount': 'Desconto em Massa',
        'loyalty_bonus': 'Bônus Fidelidade',
        'seasonal': 'Sazonal'
    };
    return labels[type] || type;
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR');
}

function updateDiscountLabel() {
    const type = document.getElementById('discount_type').value;
    const label = document.getElementById('discountLabel');
    
    if (type === 'percentage') {
        label.textContent = 'Valor do Desconto (%) *';
    } else {
        label.textContent = 'Valor do Desconto (R$) *';
    }
}

function updateConditionsHelp() {
    const type = document.getElementById('promotion_type').value;
    const help = document.getElementById('conditionsHelp');
    
    const examples = {
        'happy_hour': '{"days_of_week": [0, 1, 2, 3, 4], "time_start": "08:00", "time_end": "12:00"}',
        'first_visit': '{}',
        'birthday': '{"days_before": 7, "days_after": 7}',
        'bulk_discount': '{"min_appointments": 5}',
        'loyalty_bonus': '{"min_points": 500}',
        'seasonal': '{"season": "summer"}'
    };
    
    help.textContent = `Ex: ${examples[type] || '{}'}`;
}

function openPromotionDialog() {
    editingPromotion = null;
    document.getElementById('promotionModalTitle').textContent = 'Nova Promoção';
    document.querySelector('#promotionDialog form').reset();
    document.getElementById('conditions').value = '{}';
    document.getElementById('promotionDialog').style.display = 'flex';
}

function closePromotionDialog() {
    document.getElementById('promotionDialog').style.display = 'none';
}

function editPromotion(id) {
    const promo = promotions.find(p => p.id === id);
    if (!promo) return;
    
    editingPromotion = promo;
    document.getElementById('promotionModalTitle').textContent = 'Editar Promoção';
    document.getElementById('promotionId').value = promo.id;
    document.getElementById('name').value = promo.name;
    document.getElementById('description').value = promo.description || '';
    document.getElementById('promotion_type').value = promo.promotion_type;
    document.getElementById('discount_type').value = promo.discount_type;
    document.getElementById('discount_value').value = promo.discount_value;
    document.getElementById('conditions').value = JSON.stringify(promo.conditions || {}, null, 2);
    document.getElementById('start_date').value = promo.start_date || '';
    document.getElementById('end_date').value = promo.end_date || '';
    document.getElementById('active').checked = promo.active;
    
    updateDiscountLabel();
    updateConditionsHelp();
    
    document.getElementById('promotionDialog').style.display = 'flex';
}

async function submitPromotion() {
    const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        promotion_type: document.getElementById('promotion_type').value,
        discount_type: document.getElementById('discount_type').value,
        discount_value: parseFloat(document.getElementById('discount_value').value),
        conditions: JSON.parse(document.getElementById('conditions').value || '{}'),
        start_date: document.getElementById('start_date').value || null,
        end_date: document.getElementById('end_date').value || null,
        active: document.getElementById('active').checked
    };
    
    try {
        const url = editingPromotion 
            ? `/api/admin/promotions/${editingPromotion.id}/`
            : '/api/admin/promotions/create/';
        const method = editingPromotion ? 'PUT' : 'POST';
        
        const response = await fetchAPI(url, {
            method,
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Erro ao salvar');
        
        showToast('Sucesso', 'Promoção salva com sucesso', 'success');
        closePromotionDialog();
        loadPromotions();
    } catch (error) {
        console.error(error);
        showToast('Erro', 'Não foi possível salvar a promoção', 'error');
    }
}

async function deletePromotion(id) {
    if (!confirm('Tem certeza que deseja excluir esta promoção?')) return;
    
    try {
        const response = await fetchAPI(`/api/admin/promotions/${id}/delete/`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao excluir');
        
        showToast('Sucesso', 'Promoção excluída', 'success');
        loadPromotions();
    } catch (error) {
        showToast('Erro', 'Não foi possível excluir', 'error');
    }
}

async function togglePromotion(id, active) {
    try {
        const response = await fetchAPI(`/api/admin/promotions/${id}/toggle/`, {
            method: 'PATCH'
        });
        
        if (!response.ok) throw new Error('Erro ao alterar status');
        
        showToast('Sucesso', `Promoção ${active ? 'ativada' : 'desativada'}`, 'success');
        loadPromotions();
    } catch (error) {
        showToast('Erro', 'Não foi possível alterar o status', 'error');
        loadPromotions(); // Reload to reset checkbox
    }
}

window.openPromotionDialog = openPromotionDialog;
window.closePromotionDialog = closePromotionDialog;
window.editPromotion = editPromotion;
window.submitPromotion = submitPromotion;
window.deletePromotion = deletePromotion;
window.togglePromotion = togglePromotion;
window.setFilter = setFilter;
window.updateDiscountLabel = updateDiscountLabel;
window.updateConditionsHelp = updateConditionsHelp;

