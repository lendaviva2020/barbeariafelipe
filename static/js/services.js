/**
 * SERVICES PAGE - Catálogo de Serviços
 * Filtros, carregamento dinâmico e integração com API
 */

// API_BASE é definido em config.js (carregado antes)
// Usar função helper para evitar redeclaração de const
function getApiBase() {
    return (typeof window !== 'undefined' && window.API_BASE) ? window.API_BASE : '/api';
}
let allServices = [];
let currentCategory = 'all';

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', function() {
    initializeServicesPage();
});

function initializeServicesPage() {
    loadServices();
    setupCategoryFilters();
    setupBookingButtons();
}

// ========== LOAD SERVICES ==========
async function loadServices() {
    console.log('=== INICIO loadServices() ===');
    const servicesGrid = document.getElementById('servicesGrid');
    const combosGrid = document.getElementById('combosGrid');
    
    console.log('servicesGrid encontrado:', servicesGrid !== null);
    console.log('combosGrid encontrado:', combosGrid !== null);
    
    // Mostrar loading
    if (servicesGrid) {
        servicesGrid.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Carregando serviços...</p></div>';
    }
    
    try {
        console.log('Fazendo fetch para:', `${getApiBase()}/servicos/`);
        const response = await fetch(`${getApiBase()}/servicos/`);
        console.log('Response status:', response.status);
        console.log('Response OK:', response.ok);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: Erro ao carregar serviços`);
        }
        
        allServices = await response.json();
        console.log('Total de serviços recebidos:', allServices.length);
        console.log('Dados dos serviços:', allServices);
        
        // Separar serviços individuais e combos
        const individualServices = allServices.filter(s => !s.is_combo);
        const combos = allServices.filter(s => s.is_combo);
        
        console.log('Serviços individuais:', individualServices.length);
        console.log('Combos:', combos.length);
        
        // Renderizar serviços
        if (servicesGrid) {
            renderServices(individualServices, servicesGrid);
        }
        
        // Renderizar combos
        if (combosGrid) {
            renderCombos(combos, combosGrid);
        }
        
        console.log('=== FIM loadServices() - Sucesso ===');
        
    } catch (error) {
        console.error('=== ERRO em loadServices() ===');
        console.error('Tipo do erro:', error.name);
        console.error('Mensagem:', error.message);
        console.error('Stack:', error.stack);
        
        if (servicesGrid) {
            servicesGrid.innerHTML = `
                <div class="empty-state">
                    <p style="color: red;">Erro ao carregar serviços</p>
                    <p>${error.message}</p>
                    <button class="btn" onclick="loadServices()">Tentar Novamente</button>
                </div>
            `;
        }
    }
}

// ========== RENDER SERVICES ==========
function renderServices(services, container) {
    if (!services || services.length === 0) {
        container.innerHTML = '<p class="empty-state">Nenhum serviço encontrado.</p>';
        return;
    }
    
    container.innerHTML = '';
    
    services.forEach(service => {
        const serviceCard = createServiceCard(service);
        container.appendChild(serviceCard);
    });
}

function createServiceCard(service) {
    const card = document.createElement('div');
    card.className = 'service-card';
    card.setAttribute('data-category', service.category);
    
    // Badge (se houver)
    const badgeHtml = service.badge ? `<div class="service-badge">${service.badge}</div>` : '';
    
    // Features
    const featuresHtml = service.features && service.features.length > 0 ? 
        service.features.map(f => `<li><i class="fas fa-check"></i> ${f}</li>`).join('') :
        '<li><i class="fas fa-check"></i> Atendimento profissional</li>';
    
    // Imagem
    const imageStyle = service.image_url ? 
        `background-image: url('${service.image_url}')` :
        `background-color: #ddd`;
    
    card.innerHTML = `
        ${badgeHtml}
        <div class="service-image" style="${imageStyle}"></div>
        <div class="service-content">
            <h3>${service.name}</h3>
            <p>${service.description || 'Serviço de qualidade realizado por profissionais especializados.'}</p>
            
            <ul class="service-features">
                ${featuresHtml}
            </ul>
            
            <div class="service-meta">
                <div class="service-price">R$ ${formatPrice(service.price)}</div>
                <div class="service-duration">
                    <i class="far fa-clock"></i> ${service.duration} min
                </div>
            </div>
            
            <div class="service-actions">
                <a href="/agendar/?service=${service.id}" class="btn btn-book" data-service-id="${service.id}">Agendar</a>
                <button class="btn btn-secondary btn-details" data-service-id="${service.id}">Detalhes</button>
            </div>
        </div>
    `;
    
    return card;
}

// ========== RENDER COMBOS ==========
function renderCombos(combos, container) {
    if (!combos || combos.length === 0) {
        container.innerHTML = '<p class="empty-state">Nenhum combo disponível.</p>';
        return;
    }
    
    container.innerHTML = '';
    
    combos.forEach(combo => {
        const comboCard = createComboCard(combo);
        container.appendChild(comboCard);
    });
}

function createComboCard(combo) {
    const card = document.createElement('div');
    card.className = 'combo-card';
    card.setAttribute('data-category', 'combos');
    
    // Badge
    const badgeHtml = combo.badge ? 
        `<div class="combo-badge">${combo.badge}</div>` : '';
    
    // Features/Serviços incluídos
    const featuresHtml = combo.features && combo.features.length > 0 ? 
        combo.features.map(f => `<li>${f}</li>`).join('') :
        '';
    
    // Economia
    const savingsHtml = combo.original_price ? `
        <div class="combo-meta">
            <div class="combo-price">
                <span class="original-price">R$ ${formatPrice(combo.original_price)}</span>
                <span class="service-price">R$ ${formatPrice(combo.price)}</span>
            </div>
            <div class="combo-savings">Economize ${combo.savings_percentage}%</div>
        </div>
    ` : `
        <div class="service-price">R$ ${formatPrice(combo.price)}</div>
    `;
    
    // Imagem
    const imageStyle = combo.image_url ? 
        `background-image: url('${combo.image_url}')` :
        `background-color: #ddd`;
    
    card.innerHTML = `
        ${badgeHtml}
        <div class="combo-image" style="${imageStyle}"></div>
        <div class="combo-content">
            <h3>${combo.name}</h3>
            <p>${combo.description || 'Combo especial com serviços combinados.'}</p>
            
            ${featuresHtml ? `
                <div class="combo-services">
                    <h4>Serviços Incluídos:</h4>
                    <ul>${featuresHtml}</ul>
                </div>
            ` : ''}
            
            ${savingsHtml}
            
            <div class="service-duration">
                <i class="far fa-clock"></i> ${combo.duration} min
            </div>
            
            <div class="service-actions">
                <a href="/agendar/?service=${combo.id}" class="btn btn-book">Agendar Combo</a>
            </div>
        </div>
    `;
    
    return card;
}

// ========== CATEGORY FILTERS ==========
function setupCategoryFilters() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Atualizar botão ativo
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filtrar serviços
            const category = this.getAttribute('data-category');
            currentCategory = category;
            filterServices(category);
        });
    });
}

function filterServices(category) {
    const serviceCards = document.querySelectorAll('.service-card, .combo-card');
    
    serviceCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ========== BOOKING BUTTONS ==========
function setupBookingButtons() {
    // Delegação de eventos para botões que serão criados dinamicamente
    document.addEventListener('click', function(e) {
        // Botão de agendar
        if (e.target.classList.contains('btn-book') || e.target.closest('.btn-book')) {
            e.preventDefault();
            const btn = e.target.classList.contains('btn-book') ? e.target : e.target.closest('.btn-book');
            const serviceId = btn.getAttribute('data-service-id') || btn.href.split('service=')[1];
            
            if (serviceId) {
                window.location.href = `/agendar/?service=${serviceId}`;
            } else {
                window.location.href = '/agendar/';
            }
        }
        
        // Botão de detalhes
        if (e.target.classList.contains('btn-details')) {
            const serviceId = e.target.getAttribute('data-service-id');
            showServiceDetails(serviceId);
        }
    });
}

// ========== SERVICE DETAILS ==========
function showServiceDetails(serviceId) {
    const service = allServices.find(s => s.id == serviceId);
    
    if (!service) return;
    
    // Criar modal ou mostrar detalhes
    alert(`
Serviço: ${service.name}
Preço: R$ ${formatPrice(service.price)}
Duração: ${service.duration} minutos

${service.description}
    `.trim());
}

// ========== UTILITY FUNCTIONS ==========
function formatPrice(price) {
    return parseFloat(price).toFixed(2).replace('.', ',');
}
