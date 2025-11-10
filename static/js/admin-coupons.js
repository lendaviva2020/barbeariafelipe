/**
 * Admin Coupons Page - CRUD completo de cupons
 * Extraído 100% do React Coupons.tsx (595 linhas)
 */

// State
let coupons = [];
let editingCoupon = null;
let isSubmitting = false;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadCoupons();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Discount type change
    const typeSelect = document.getElementById('discount_type');
    if (typeSelect) {
        typeSelect.addEventListener('change', updateDiscountLabel);
    }
    
    // Code input - uppercase only
    const codeInput = document.getElementById('code');
    if (codeInput) {
        codeInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }
    
    // Set min date to today
    const expiryDate = document.getElementById('expiry_date');
    if (expiryDate) {
        expiryDate.min = new Date().toISOString().split('T')[0];
    }
}

// Update discount label based on type
function updateDiscountLabel() {
    const type = document.getElementById('discount_type').value;
    const label = document.getElementById('discountLabel');
    const input = document.getElementById('discount');
    
    if (type === 'percentage') {
        label.textContent = 'Desconto (%) *';
        input.placeholder = '10';
        input.step = '1';
        input.max = '100';
    } else {
        label.textContent = 'Valor (R$) *';
        input.placeholder = '15.00';
        input.step = '0.01';
        input.max = '10000';
    }
}

// Load coupons
async function loadCoupons() {
    showLoading();
    
    try {
        const response = await fetchAPI('/api/cupons/admin/');
        if (!response.ok) throw new Error('Erro ao carregar cupons');
        
        coupons = await response.json();
        renderCoupons();
    } catch (error) {
        console.error('Erro ao carregar cupons:', error);
        showError();
    } finally {
        hideLoading();
    }
}

// Render coupons
function renderCoupons() {
    const list = document.getElementById('couponsList');
    const emptyState = document.getElementById('emptyState');
    
    if (coupons.length === 0) {
        list.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    list.style.display = 'flex';
    emptyState.style.display = 'none';
    
    list.innerHTML = coupons.map(coupon => createCouponCard(coupon)).join('');
}

// Create coupon card
function createCouponCard(coupon) {
    const isExpired = coupon.expiry_date && new Date(coupon.expiry_date) < new Date();
    const isLimitReached = coupon.max_uses > 0 && coupon.current_uses >= coupon.max_uses;
    const isActive = coupon.active && !isExpired && !isLimitReached;
    
    return `
        <div class="coupon-card ${!coupon.active ? 'inactive' : ''}">
            <!-- Header -->
            <div class="coupon-header">
                <div class="coupon-info">
                    <div class="coupon-icon ${isActive ? 'active' : 'inactive'}">
                        🎫
                    </div>
                    <div class="coupon-details">
                        <div class="coupon-code">
                            ${coupon.code}
                            <button class="copy-btn" onclick="copyCouponCode('${coupon.code}')" title="Copiar código">
                                📋
                            </button>
                        </div>
                        <p class="coupon-description">
                            ${coupon.description || 'Sem descrição'}
                        </p>
                    </div>
                </div>
                
                <div class="coupon-status">
                    ${getCouponStatusBadge(coupon, isExpired, isLimitReached)}
                </div>
            </div>
            
            <!-- Stats -->
            <div class="coupon-stats">
                <div class="stat-item">
                    <p class="stat-label">🎫 Desconto</p>
                    <p class="stat-value">
                        ${coupon.discount_type === 'percentage' 
                            ? `${coupon.discount}%` 
                            : `R$ ${coupon.discount.toFixed(2)}`}
                    </p>
                </div>
                
                <div class="stat-item">
                    <p class="stat-label">👥 Usos</p>
                    <p class="stat-value">
                        ${coupon.current_uses} ${coupon.max_uses > 0 ? `/ ${coupon.max_uses}` : '/ ∞'}
                    </p>
                </div>
                
                <div class="stat-item">
                    <p class="stat-label">📅 Expira em</p>
                    <p class="stat-value">
                        ${coupon.expiry_date 
                            ? new Date(coupon.expiry_date).toLocaleDateString('pt-BR')
                            : 'Não expira'}
                    </p>
                </div>
                
                <div class="stat-item">
                    <p class="stat-label">Criado em</p>
                    <p class="stat-value">
                        ${new Date(coupon.created_at).toLocaleDateString('pt-BR')}
                    </p>
                </div>
            </div>
            
            <!-- Actions -->
            <div class="coupon-actions">
                <button class="btn-icon" onclick="editCoupon(${coupon.id})" ${!isActive ? 'disabled' : ''}>
                    ✏️ Editar
                </button>
                <button class="btn-icon btn-delete" onclick="deleteCoupon(${coupon.id})">
                    🗑️ Excluir
                </button>
            </div>
        </div>
    `;
}

// Get coupon status badge
function getCouponStatusBadge(coupon, isExpired, isLimitReached) {
    let badges = [];
    
    // Main status
    if (!coupon.active) {
        badges.push('<span class="status-badge inactive">Inativo</span>');
    } else if (isExpired) {
        badges.push('<span class="status-badge expired">Expirado</span>');
    } else if (isLimitReached) {
        badges.push('<span class="status-badge limit-reached">Limite Atingido</span>');
    } else {
        badges.push('<span class="status-badge active">Ativo</span>');
    }
    
    return badges.join('');
}

// Copy coupon code
function copyCouponCode(code) {
    navigator.clipboard.writeText(code);
    showToast('Código copiado!', `Código ${code} copiado para a área de transferência`, 'success');
}

// Open coupon dialog
function openCouponDialog() {
    editingCoupon = null;
    document.getElementById('couponModalTitle').textContent = 'Novo Cupom';
    document.getElementById('couponForm').reset();
    document.getElementById('couponId').value = '';
    document.getElementById('submitBtn').innerHTML = '➕ Criar Cupom';
    document.getElementById('active').checked = true;
    
    document.getElementById('couponDialog').style.display = 'flex';
}

// Close coupon dialog
function closeCouponDialog() {
    document.getElementById('couponDialog').style.display = 'none';
    editingCoupon = null;
}

// Edit coupon
function editCoupon(id) {
    const coupon = coupons.find(c => c.id === id);
    if (!coupon) return;
    
    editingCoupon = coupon;
    document.getElementById('couponModalTitle').textContent = 'Editar Cupom';
    document.getElementById('couponId').value = coupon.id;
    document.getElementById('code').value = coupon.code;
    document.getElementById('discount_type').value = coupon.discount_type;
    document.getElementById('discount').value = coupon.discount;
    document.getElementById('description').value = coupon.description || '';
    document.getElementById('expiry_date').value = coupon.expiry_date || '';
    document.getElementById('max_uses').value = coupon.max_uses || 0;
    document.getElementById('active').checked = coupon.active;
    document.getElementById('submitBtn').innerHTML = '💾 Atualizar Cupom';
    
    updateDiscountLabel();
    document.getElementById('couponDialog').style.display = 'flex';
}

// Submit coupon
async function submitCoupon() {
    if (isSubmitting) return;
    
    const code = document.getElementById('code').value.trim();
    const discount = parseFloat(document.getElementById('discount').value);
    
    // Validation
    if (!code || code.length < 3) {
        showToast('Erro', 'Código deve ter no mínimo 3 caracteres', 'error');
        return;
    }
    
    if (discount <= 0) {
        showToast('Erro', 'Desconto deve ser maior que zero', 'error');
        return;
    }
    
    const formData = {
        code,
        discount,
        discount_type: document.getElementById('discount_type').value,
        description: document.getElementById('description').value,
        expiry_date: document.getElementById('expiry_date').value || null,
        max_uses: parseInt(document.getElementById('max_uses').value) || 0,
        active: document.getElementById('active').checked
    };
    
    // Validate percentage
    if (formData.discount_type === 'percentage' && formData.discount > 100) {
        showToast('Erro', 'Desconto percentual não pode ser maior que 100%', 'error');
        return;
    }
    
    isSubmitting = true;
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processando...';
    
    try {
        let response;
        if (editingCoupon) {
            response = await fetchAPI(`/api/cupons/admin/${editingCoupon.id}/`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
        } else {
            response = await fetchAPI('/api/cupons/admin/create/', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
        }
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Erro ao salvar cupom');
        }
        
        showToast(
            editingCoupon ? 'Cupom atualizado' : 'Cupom criado',
            'Cupom salvo com sucesso',
            'success'
        );
        
        closeCouponDialog();
        await loadCoupons();
    } catch (error) {
        console.error('Erro ao salvar cupom:', error);
        showToast('Erro', error.message, 'error');
    } finally {
        isSubmitting = false;
        submitBtn.disabled = false;
        submitBtn.innerHTML = editingCoupon ? '💾 Atualizar Cupom' : '➕ Criar Cupom';
    }
}

// Delete coupon
async function deleteCoupon(id) {
    if (!confirm('Tem certeza que deseja excluir este cupom? Esta ação não pode ser desfeita.')) {
        return;
    }
    
    try {
        const response = await fetchAPI(`/api/cupons/admin/${id}/delete/`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao excluir cupom');
        
        showToast('Cupom excluído', 'Cupom excluído com sucesso', 'success');
        await loadCoupons();
    } catch (error) {
        console.error('Erro ao excluir cupom:', error);
        showToast('Erro', 'Não foi possível excluir o cupom', 'error');
    }
}

// Show/Hide loading
function showLoading() {
    document.getElementById('loadingState').style.display = 'flex';
    document.getElementById('couponsList').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function showError() {
    document.getElementById('emptyState').innerHTML = `
        <span class="empty-icon">⚠️</span>
        <h3>Erro ao carregar</h3>
        <p>Não foi possível carregar os cupons. Tente novamente.</p>
        <button class="btn btn-primary" onclick="loadCoupons()">Tentar Novamente</button>
    `;
    document.getElementById('emptyState').style.display = 'block';
}

// Toast
function showToast(title, message, type = 'success') {
    if (window.showToast) {
        window.showToast(title, message, type);
    } else {
        alert(`${title}: ${message}`);
    }
}

// Export
window.openCouponDialog = openCouponDialog;
window.closeCouponDialog = closeCouponDialog;
window.editCoupon = editCoupon;
window.deleteCoupon = deleteCoupon;
window.submitCoupon = submitCoupon;
window.copyCouponCode = copyCouponCode;

