/**
 * Public Coupons Page - For users to view and copy available coupons
 * Extraído de Coupons.tsx (usuário final)
 */

let allCoupons = [];

document.addEventListener('DOMContentLoaded', loadCoupons);

async function loadCoupons() {
    try {
        const response = await fetchAPI('/api/cupons/');
        allCoupons = await response.json();
        renderCoupons();
    } catch (error) {
        console.error('Erro ao carregar cupons:', error);
        showError();
    }
}

function renderCoupons() {
    const now = new Date();
    
    // Separar cupons ativos e expirados
    const active = allCoupons.filter(c => 
        c.active && 
        (!c.expiry_date || new Date(c.expiry_date) >= now) &&
        (c.max_uses === null || c.current_uses < c.max_uses)
    );
    
    const expired = allCoupons.filter(c => 
        !c.active || 
        (c.expiry_date && new Date(c.expiry_date) < now) ||
        (c.max_uses !== null && c.current_uses >= c.max_uses)
    );
    
    // Update counters
    document.getElementById('activeCount').textContent = `${active.length} disponíveis`;
    
    // Render active coupons
    const activeGrid = document.getElementById('activeCoupons');
    const emptyState = document.getElementById('emptyState');
    
    if (active.length === 0) {
        activeGrid.style.display = 'none';
        emptyState.style.display = 'block';
    } else {
        activeGrid.style.display = 'grid';
        emptyState.style.display = 'none';
        activeGrid.innerHTML = active.map(renderCouponCard).join('');
    }
    
    // Render expired coupons
    const expiredGrid = document.getElementById('expiredCoupons');
    if (expired.length > 0) {
        expiredGrid.innerHTML = expired.map(c => renderCouponCard(c, true)).join('');
    }
}

function renderCouponCard(coupon, isExpired = false) {
    const discountText = coupon.discount_type === 'percentage' 
        ? `${coupon.discount}% OFF`
        : `R$ ${parseFloat(coupon.discount).toFixed(2)} OFF`;
    
    const expiryText = coupon.expiry_date 
        ? `Válido até ${formatDate(coupon.expiry_date)}`
        : 'Sem data de expiração';
    
    const usageText = coupon.max_uses 
        ? `${coupon.current_uses}/${coupon.max_uses} usos`
        : `${coupon.current_uses} usos`;
    
    const isLimited = coupon.max_uses && (coupon.max_uses - coupon.current_uses) <= 5;
    
    return `
        <div class="coupon-card ${isExpired ? 'expired' : ''} ${isLimited ? 'limited' : ''}">
            <div class="coupon-header">
                <div class="discount-badge ${coupon.discount_type}">
                    ${discountText}
                </div>
                ${isLimited && !isExpired ? '<div class="limited-badge">🔥 Últimos</div>' : ''}
                ${isExpired ? '<div class="expired-badge">Expirado</div>' : ''}
            </div>
            
            <div class="coupon-body">
                <h3 class="coupon-code">${coupon.code}</h3>
                <p class="coupon-description">${coupon.description || 'Cupom de desconto'}</p>
            </div>
            
            <div class="coupon-footer">
                <div class="coupon-meta">
                    <span class="meta-item">📅 ${expiryText}</span>
                    <span class="meta-item">👥 ${usageText}</span>
                </div>
                
                ${!isExpired ? `
                    <button class="btn-copy" onclick="copyCouponCode('${coupon.code}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        Copiar Código
                    </button>
                ` : '<button class="btn-copy disabled" disabled>Indisponível</button>'}
            </div>
            
            ${isLimited && !isExpired ? '<div class="coupon-urgency">⚡ Corra! Estoque limitado</div>' : ''}
        </div>
    `;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
}

async function copyCouponCode(code) {
    try {
        await navigator.clipboard.writeText(code);
        showCopyToast();
    } catch (err) {
        // Fallback para navegadores antigos
        const textarea = document.createElement('textarea');
        textarea.value = code;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showCopyToast();
    }
}

function showCopyToast() {
    const toast = document.getElementById('copyToast');
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function toggleExpired() {
    const grid = document.getElementById('expiredCoupons');
    const btn = event.target;
    
    if (grid.style.display === 'none') {
        grid.style.display = 'grid';
        btn.textContent = 'Ocultar';
    } else {
        grid.style.display = 'none';
        btn.textContent = 'Mostrar';
    }
}

function showError() {
    const activeGrid = document.getElementById('activeCoupons');
    activeGrid.innerHTML = `
        <div class="error-state">
            <span class="error-icon">⚠️</span>
            <p>Erro ao carregar cupons. Tente novamente.</p>
            <button class="btn btn-primary" onclick="loadCoupons()">Recarregar</button>
        </div>
    `;
}

// Export global functions
window.copyCouponCode = copyCouponCode;
window.toggleExpired = toggleExpired;

