/**
 * Services Page - Filtros e busca
 */

let services = [];
let currentCategory = 'all';

document.addEventListener('DOMContentLoaded', loadServices);

async function loadServices() {
    try {
        const response = await fetchAPI('/api/servicos/');
        services = await response.json();
        renderServices();
    } catch (error) {
        console.error(error);
    }
}

function setCategory(category) {
    currentCategory = category;
    document.querySelectorAll('[data-category]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === category);
    });
    renderServices();
}

function renderServices() {
    const filtered = currentCategory === 'all' ? services : services.filter(s => s.category === currentCategory);
    const grid = document.getElementById('servicesGrid');
    
    if (!grid) return;
    
    grid.innerHTML = filtered.map(service => `
        <div class="service-card">
            <h3>${service.name}</h3>
            <p class="service-description">${service.description || ''}</p>
            <div class="service-details">
                <span class="service-price">R$ ${service.price.toFixed(2)}</span>
                <span class="service-duration">${service.duration} min</span>
            </div>
            <a href="/agendar/?service=${service.id}" class="btn btn-primary btn-block">Agendar</a>
        </div>
    `).join('');
}

window.setCategory = setCategory;

