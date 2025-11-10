/**
 * Reviews System - Completo
 */

let reviews = [];
let selectedRating = 0;
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', async () => {
    await loadBarbers();
    await loadServices();
    await loadReviews();
});

async function loadBarbers() {
    try {
        const response = await fetchAPI('/api/barbeiros/');
        const barbers = await response.json();
        const select = document.getElementById('barber_id');
        barbers.forEach(b => {
            select.innerHTML += `<option value="${b.id}">${b.name}</option>`;
        });
    } catch (error) {
        console.error(error);
    }
}

async function loadServices() {
    try {
        const response = await fetchAPI('/api/servicos/');
        const services = await response.json();
        const select = document.getElementById('service_id');
        services.forEach(s => {
            select.innerHTML += `<option value="${s.id}">${s.name}</option>`;
        });
    } catch (error) {
        console.error(error);
    }
}

async function loadReviews() {
    try {
        const response = await fetchAPI('/api/reviews/');
        reviews = await response.json();
        updateRatingSummary();
        renderReviews();
    } catch (error) {
        console.error(error);
    }
}

function updateRatingSummary() {
    const total = reviews.length;
    const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
    const avg = total > 0 ? (sum / total).toFixed(1) : '0.0';
    
    document.getElementById('avgRating').textContent = avg;
    document.getElementById('totalReviews').textContent = `${total} avaliações`;
    document.getElementById('avgStars').innerHTML = createStars(parseFloat(avg));
}

function setRating(rating) {
    selectedRating = rating;
    document.getElementById('rating').value = rating;
    
    document.querySelectorAll('.star-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i < rating);
    });
}

function setRatingFilter(rating) {
    currentFilter = rating;
    document.querySelectorAll('[data-rating]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.rating == rating);
    });
    renderReviews();
}

function renderReviews() {
    const filtered = currentFilter === 'all' ? reviews : reviews.filter(r => r.rating == currentFilter);
    const list = document.getElementById('reviewsList');
    const empty = document.getElementById('emptyState');
    
    if (filtered.length === 0) {
        list.style.display = 'none';
        empty.style.display = 'block';
        return;
    }
    
    list.style.display = 'grid';
    empty.style.display = 'none';
    
    list.innerHTML = filtered.map(review => `
        <div class="review-card">
            <div class="review-header">
                <div class="review-user">
                    <div class="user-avatar">${review.user_name[0]}</div>
                    <div>
                        <strong>${review.user_name}</strong>
                        <div class="review-stars">${createStars(review.rating)}</div>
                    </div>
                </div>
                <span class="review-date">${formatDate(review.created_at)}</span>
            </div>
            <p class="review-comment">${review.comment}</p>
            ${review.barber_name ? `<p class="review-meta">Barbeiro: ${review.barber_name}</p>` : ''}
            ${review.service_name ? `<p class="review-meta">Serviço: ${review.service_name}</p>` : ''}
        </div>
    `).join('');
}

function createStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? '⭐' : '☆';
    }
    return stars;
}

function openReviewDialog() {
    if (!auth.isAuthenticated()) {
        showToast('Atenção', 'Faça login para avaliar', 'warning');
        window.location.href = '/auth/?redirect=/reviews/';
        return;
    }
    document.getElementById('reviewDialog').style.display = 'flex';
}

function closeReviewDialog() {
    document.getElementById('reviewDialog').style.display = 'none';
    document.getElementById('comment').value = '';
    selectedRating = 0;
    document.querySelectorAll('.star-btn').forEach(btn => btn.classList.remove('active'));
}

async function submitReview() {
    if (selectedRating === 0) {
        showToast('Erro', 'Selecione uma avaliação', 'error');
        return;
    }
    
    const data = {
        rating: selectedRating,
        comment: document.getElementById('comment').value,
        barber_id: document.getElementById('barber_id').value || null,
        service_id: document.getElementById('service_id').value || null
    };
    
    try {
        const response = await fetchAPI('/api/reviews/create/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Erro ao enviar');
        
        showToast('Sucesso', 'Avaliação enviada! Aguardando aprovação.', 'success');
        closeReviewDialog();
    } catch (error) {
        showToast('Erro', 'Não foi possível enviar a avaliação', 'error');
    }
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

window.openReviewDialog = openReviewDialog;
window.closeReviewDialog = closeReviewDialog;
window.submitReview = submitReview;
window.setRating = setRating;
window.setRatingFilter = setRatingFilter;

