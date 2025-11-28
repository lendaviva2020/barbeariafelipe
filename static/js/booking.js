// Estado global do agendamento
const bookingState = {
    currentStep: 1,
    selectedService: null,
    selectedBarber: null,
    selectedDate: null,
    selectedTime: null,
    appliedCoupon: null,
    services: [],
    barbers: [],
    availableSlots: []
};

// Verificar autenticação antes de inicializar
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se o usuário está autenticado
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        // Capturar serviço selecionado da URL antes de redirecionar
        const urlParams = new URLSearchParams(window.location.search);
        const serviceId = urlParams.get('service');
        
        // Mostrar mensagem informativa
        if (serviceId) {
            alert('Você precisa fazer login para agendar o serviço escolhido.\n\nVocê será redirecionado para a página de login.');
        } else {
            alert('Você precisa fazer login para agendar um horário.\n\nVocê será redirecionado para a página de login.');
        }
        
        // Redirecionar para login mantendo o serviço selecionado
        if (serviceId) {
            window.location.href = `/auth/?service=${serviceId}&next=/agendar/?service=${serviceId}`;
        } else {
            window.location.href = '/auth/?next=/agendar/';
        }
        return;
    }
    
    // Verificar se o token ainda é válido fazendo uma requisição
    fetch('/api/users/me/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            // Token inválido ou expirado
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            
            // Capturar serviço selecionado da URL antes de redirecionar
            const urlParams = new URLSearchParams(window.location.search);
            const serviceId = urlParams.get('service');
            
            // Mostrar mensagem informativa
            if (serviceId) {
                alert('Sua sessão expirou. Você precisa fazer login novamente para agendar o serviço escolhido.');
            } else {
                alert('Sua sessão expirou. Você precisa fazer login novamente para agendar.');
            }
            
            if (serviceId) {
                window.location.href = `/auth/?service=${serviceId}&next=/agendar/?service=${serviceId}`;
            } else {
                window.location.href = '/auth/?next=/agendar/';
            }
        } else {
            // Token válido, inicializar agendamento
            initBooking();
        }
    })
    .catch(error => {
        console.error('Erro ao verificar autenticação:', error);
        // Em caso de erro, redirecionar para login
        const urlParams = new URLSearchParams(window.location.search);
        const serviceId = urlParams.get('service');
        
        // Mostrar mensagem informativa
        if (serviceId) {
            alert('Erro ao verificar autenticação. Você precisa fazer login para agendar o serviço escolhido.');
        } else {
            alert('Erro ao verificar autenticação. Você precisa fazer login para agendar.');
        }
        
        if (serviceId) {
            window.location.href = `/auth/?service=${serviceId}&next=/agendar/?service=${serviceId}`;
        } else {
            window.location.href = '/auth/?next=/agendar/';
        }
    });
});

function initBooking() {
    loadServices();
    setupEventListeners();
    
    // Verificar se há um serviço ou barbeiro pré-selecionado na URL
    const urlParams = new URLSearchParams(window.location.search);
    const serviceId = urlParams.get('service');
    const barberId = urlParams.get('barber');
    
    if (serviceId) {
        // Aguardar serviços carregarem e então pré-selecionar
        // Usar um intervalo para verificar quando os serviços estiverem carregados
        const checkAndSelect = setInterval(() => {
            const serviceCard = document.querySelector(`[data-service-id="${serviceId}"]`);
            if (serviceCard && bookingState.services.length > 0) {
                clearInterval(checkAndSelect);
                selectService(serviceCard);
                // Habilitar botão próximo automaticamente
                const nextBtn = document.getElementById('nextStep1');
                if (nextBtn) {
                    nextBtn.disabled = false;
                }
            }
        }, 100);
        
        // Limpar intervalo após 5 segundos para evitar loop infinito
        setTimeout(() => clearInterval(checkAndSelect), 5000);
    }
    
    // Se houver barbeiro na URL, ir direto para o step 2 (seleção de barbeiro)
    if (barberId && !serviceId) {
        // Aguardar barbeiros carregarem e então pré-selecionar
        const checkAndSelectBarber = setInterval(() => {
            if (bookingState.barbers.length > 0) {
                clearInterval(checkAndSelectBarber);
                const barberCard = document.querySelector(`[data-barber-id="${barberId}"]`);
                if (barberCard) {
                    // Ir para step 2 e selecionar o barbeiro
                    goToStep(2);
                    setTimeout(() => {
                        selectBarber(barberCard);
                    }, 100);
                }
            }
        }, 100);
        
        // Limpar intervalo após 5 segundos
        setTimeout(() => clearInterval(checkAndSelectBarber), 5000);
    }
}

// ===== CARREGAMENTO DE DADOS =====
async function loadServices() {
    const grid = document.getElementById('servicesGrid');
    
    try {
        // Tentar primeiro o endpoint de booking, depois o padrão
        let response = await fetch('/api/agendamentos/services/');
        if (!response.ok) {
            // Se falhar, tentar endpoint padrão
            response = await fetch('/api/servicos/');
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            const text = await response.text();
            console.error('Resposta não é JSON:', text.substring(0, 200));
            throw new Error('Resposta não é JSON');
        }
        const data = await response.json();
        bookingState.services = data;
        
        if (data.length === 0) {
            grid.innerHTML = '<p class="empty-state">Nenhum serviço disponível no momento.</p>';
            return;
        }
        
        grid.innerHTML = data.map(service => `
            <div class="service-card" data-service-id="${service.id}">
                <div class="service-icon">
                    <i class="fas fa-cut"></i>
                </div>
                <h3 class="service-name">${service.name}</h3>
                <p class="service-description">${service.description || ''}</p>
                <div class="service-details">
                    <span class="service-duration">
                        <i class="fas fa-clock"></i> ${service.duration} min
                    </span>
                    <span class="service-price">R$ ${parseFloat(service.price).toFixed(2).replace('.', ',')}</span>
                </div>
            </div>
        `).join('');
        
        // Adicionar eventos de clique
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('click', () => selectService(card));
        });
        
        // Verificar se há um serviço pré-selecionado na URL e selecioná-lo
        const urlParams = new URLSearchParams(window.location.search);
        const serviceId = urlParams.get('service');
        if (serviceId) {
            const serviceCard = document.querySelector(`[data-service-id="${serviceId}"]`);
            if (serviceCard) {
                selectService(serviceCard);
                // Habilitar botão próximo automaticamente
                const nextBtn = document.getElementById('nextStep1');
                if (nextBtn) {
                    nextBtn.disabled = false;
                }
            }
        }
        
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
        grid.innerHTML = '<p class="error-state">Erro ao carregar serviços. Tente novamente.</p>';
    }
}

async function loadBarbers() {
    const grid = document.getElementById('barbersGrid');
    
    try {
        const token = localStorage.getItem('access_token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch('/api/agendamentos/barbers/', {
            headers: headers
        });
        const data = await response.json();
        bookingState.barbers = data;
        
        // Adicionar opção "Qualquer barbeiro"
        let html = `
            <div class="barber-card" data-barber-id="">
                <div class="barber-avatar">
                    <i class="fas fa-users"></i>
                </div>
                <h3 class="barber-name">Qualquer Barbeiro</h3>
                <p class="barber-description">Primeiro disponível</p>
            </div>
        `;
        
        html += data.map(barber => `
            <div class="barber-card" data-barber-id="${barber.id}">
                <div class="barber-avatar">
                    ${barber.photo ? 
                        `<img src="${barber.photo}" alt="${barber.name}">` : 
                        `<i class="fas fa-user"></i>`
                    }
                </div>
                <h3 class="barber-name">${barber.name}</h3>
                <p class="barber-description">${barber.specialty || 'Barbeiro profissional'}</p>
            </div>
        `).join('');
        
        grid.innerHTML = html;
        
        // Adicionar eventos de clique
        document.querySelectorAll('.barber-card').forEach(card => {
            card.addEventListener('click', () => selectBarber(card));
        });
        
        // Verificar se há um barbeiro pré-selecionado na URL e selecioná-lo
        const urlParams = new URLSearchParams(window.location.search);
        const barberId = urlParams.get('barber');
        if (barberId) {
            const barberCard = document.querySelector(`[data-barber-id="${barberId}"]`);
            if (barberCard) {
                selectBarber(barberCard);
            }
        }
        
    } catch (error) {
        console.error('Erro ao carregar barbeiros:', error);
        grid.innerHTML = '<p class="error-state">Erro ao carregar barbeiros. Tente novamente.</p>';
    }
}

async function loadAvailableSlots(date) {
    const container = document.getElementById('availableSlots');
    container.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Carregando horários...</p></div>';
    
    try {
        const params = new URLSearchParams({
            date: date,
            service_id: bookingState.selectedService.id,
        });
        
        if (bookingState.selectedBarber && bookingState.selectedBarber.id) {
            params.append('barber_id', bookingState.selectedBarber.id);
        }
        
        const token = localStorage.getItem('access_token');
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`/api/agendamentos/available-slots/?${params}`, {
            headers: headers
        });
        const data = await response.json();
        bookingState.availableSlots = data;
        
        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">Nenhum horário disponível para esta data.</p>';
            return;
        }
        
        // Verificar formato da resposta
        const slots = Array.isArray(data) ? data : [];
        
        if (slots.length === 0) {
            container.innerHTML = '<p class="empty-state">Nenhum horário disponível para esta data.</p>';
            return;
        }
        
        container.innerHTML = slots.map(slot => {
            // O slot pode ter 'time' ou ser uma string direta
            const timeValue = slot.time || slot;
            const isAvailable = slot.available !== false; // Default true se não especificado
            const disabledClass = isAvailable ? '' : 'disabled';
            const disabledAttr = isAvailable ? '' : 'disabled';
            
            return `
                <button class="time-slot ${disabledClass}" data-time="${timeValue}" type="button" ${disabledAttr}>
                    ${timeValue}
                </button>
            `;
        }).join('');
        
        // Adicionar eventos de clique
        document.querySelectorAll('.time-slot').forEach(btn => {
            btn.addEventListener('click', function() {
                selectTimeSlot(this);
            });
        });
        
    } catch (error) {
        console.error('Erro ao carregar horários:', error);
        container.innerHTML = '<p class="error-state">Erro ao carregar horários. Tente novamente.</p>';
    }
}

// ===== SELEÇÕES =====
function selectService(card) {
    // Remove seleção anterior
    document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    
    const serviceId = card.dataset.serviceId;
    bookingState.selectedService = bookingState.services.find(s => s.id == serviceId);
    
    // Habilitar botão próximo
    document.getElementById('nextStep1').disabled = false;
    
    updateSummary();
}

function selectBarber(card) {
    // Remove seleção anterior
    document.querySelectorAll('.barber-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    
    const barberId = card.dataset.barberId;
    bookingState.selectedBarber = barberId ? 
        bookingState.barbers.find(b => b.id == barberId) : null;
    
    updateSummary();
}

function selectTimeSlot(btn) {
    // Remove seleção anterior
    document.querySelectorAll('.time-slot').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    
    bookingState.selectedTime = btn.dataset.time;
    
    // Habilitar botão próximo
    document.getElementById('nextStep3').disabled = false;
    
    updateSummary();
}

// ===== NAVEGAÇÃO ENTRE STEPS =====
function setupEventListeners() {
    // Navegação
    document.getElementById('nextStep1')?.addEventListener('click', () => goToStep(2));
    document.getElementById('prevStep2')?.addEventListener('click', () => goToStep(1));
    document.getElementById('nextStep2')?.addEventListener('click', () => goToStep(3));
    document.getElementById('prevStep3')?.addEventListener('click', () => goToStep(2));
    document.getElementById('nextStep3')?.addEventListener('click', () => goToStep(4));
    document.getElementById('prevStep4')?.addEventListener('click', () => goToStep(3));
    
    // Confirmação
    document.getElementById('confirmBooking')?.addEventListener('click', confirmBooking);
    
    // Cupom
    document.getElementById('applyCoupon')?.addEventListener('click', applyCoupon);
    
    // Máscara de telefone
    document.getElementById('customerPhone')?.addEventListener('input', maskPhone);
}

function goToStep(stepNumber) {
    // Validações antes de avançar
    if (stepNumber === 2 && !bookingState.selectedService) {
        alert('Por favor, selecione um serviço primeiro.');
        return;
    }
    
    if (stepNumber === 3 && !bookingState.selectedService) {
        alert('Por favor, selecione um serviço primeiro.');
        return;
    }
    
    if (stepNumber === 4 && (!bookingState.selectedDate || !bookingState.selectedTime)) {
        alert('Por favor, selecione data e horário primeiro.');
        return;
    }
    
    // Atualizar estado
    bookingState.currentStep = stepNumber;
    
    // Atualizar UI dos steps
    document.querySelectorAll('.step').forEach((step, index) => {
        if (index + 1 < stepNumber) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (index + 1 === stepNumber) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
    
    // Mostrar conteúdo correto
    document.querySelectorAll('.booking-step-content').forEach((content, index) => {
        content.classList.toggle('active', index + 1 === stepNumber);
    });
    
    // Carregar dados específicos do step
    if (stepNumber === 2) {
        loadBarbers();
    } else if (stepNumber === 3) {
        initCalendar();
    } else if (stepNumber === 4) {
        updateSummary();
    }
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== CALENDÁRIO =====
function initCalendar() {
    const calendarEl = document.getElementById('calendar');
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    
    renderCalendar(currentYear, currentMonth);
}

function renderCalendar(year, month) {
    const calendarEl = document.getElementById('calendar');
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startDay = firstDay.getDay();
    
    const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    
    let html = `
        <div class="calendar-header">
            <button class="btn-calendar-nav" onclick="changeMonth(-1)">
                <i class="fas fa-chevron-left"></i>
            </button>
            <h4>${monthNames[month]} ${year}</h4>
            <button class="btn-calendar-nav" onclick="changeMonth(1)">
                <i class="fas fa-chevron-right"></i>
            </button>
        </div>
        <div class="calendar-weekdays">
            <div>Dom</div><div>Seg</div><div>Ter</div><div>Qua</div>
            <div>Qui</div><div>Sex</div><div>Sáb</div>
        </div>
        <div class="calendar-days">
    `;
    
    // Dias vazios antes do início do mês
    for (let i = 0; i < startDay; i++) {
        html += '<div class="calendar-day empty"></div>';
    }
    
    // Dias do mês
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const dateString = formatDate(date);
        const isToday = date.getTime() === today.getTime();
        const isPast = date < today;
        const isSelected = bookingState.selectedDate === dateString;
        
        let classes = 'calendar-day';
        if (isToday) classes += ' today';
        if (isPast) classes += ' disabled';
        if (isSelected) classes += ' selected';
        
        // Usar addEventListener em vez de onclick inline para melhor compatibilidade
        const dayId = `day-${dateString}`;
        html += `<div class="${classes}" data-date="${dateString}" id="${dayId}" ${isPast ? '' : 'style="cursor: pointer;"'}>
            ${day}
        </div>`;
    }
    
    html += '</div>';
    calendarEl.innerHTML = html;
    
    // Adicionar event listeners após renderizar
    document.querySelectorAll('.calendar-day:not(.empty):not(.disabled)').forEach(day => {
        day.addEventListener('click', function() {
            const dateString = this.dataset.date;
            if (dateString) {
                selectDate(dateString);
            }
        });
    });
}

window.changeMonth = function(direction) {
    const calendarEl = document.getElementById('calendar');
    const header = calendarEl.querySelector('.calendar-header h4').textContent;
    const [monthName, year] = header.split(' ');
    const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    
    let month = monthNames.indexOf(monthName);
    let newYear = parseInt(year);
    
    month += direction;
    if (month < 0) {
        month = 11;
        newYear--;
    } else if (month > 11) {
        month = 0;
        newYear++;
    }
    
    renderCalendar(newYear, month);
}

window.selectDate = function(dateString) {
    bookingState.selectedDate = dateString;
    
    // Atualizar visual
    document.querySelectorAll('.calendar-day').forEach(day => {
        day.classList.remove('selected');
        if (day.dataset.date === dateString) {
            day.classList.add('selected');
        }
    });
    
    // Carregar horários disponíveis
    loadAvailableSlots(dateString);
    
    updateSummary();
}

// ===== CUPOM =====
async function applyCoupon() {
    const code = document.getElementById('couponCode').value.trim();
    const feedback = document.getElementById('couponFeedback');
    
    if (!code) {
        feedback.textContent = 'Digite um código de cupom.';
        feedback.className = 'coupon-feedback error';
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch('/api/agendamentos/validate-coupon/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        
        if (data.valid) {
            bookingState.appliedCoupon = data.coupon;
            feedback.textContent = `Cupom aplicado! Desconto de ${data.coupon.discount}${data.coupon.discount_type === 'percentage' ? '%' : ' reais'}`;
            feedback.className = 'coupon-feedback success';
            updateSummary();
        } else {
            feedback.textContent = data.message || 'Cupom inválido.';
            feedback.className = 'coupon-feedback error';
        }
    } catch (error) {
        console.error('Erro ao validar cupom:', error);
        feedback.textContent = 'Erro ao validar cupom.';
        feedback.className = 'coupon-feedback error';
    }
}

// ===== CONFIRMAÇÃO =====
async function confirmBooking() {
    const form = document.getElementById('bookingForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const bookingData = {
        service_id: bookingState.selectedService.id,
        barber_id: bookingState.selectedBarber?.id || null,
        date: bookingState.selectedDate,
        time: bookingState.selectedTime,
        customer_name: document.getElementById('customerName').value,
        customer_phone: document.getElementById('customerPhone').value,
        customer_email: document.getElementById('customerEmail').value || null,
        notes: document.getElementById('notes').value || null,
        coupon_code: bookingState.appliedCoupon?.code || null
    };
    
    try {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch('/api/agendamentos/bookings/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccessModal(data);
        } else {
            alert(data.message || 'Erro ao confirmar agendamento.');
        }
    } catch (error) {
        console.error('Erro ao confirmar agendamento:', error);
        alert('Erro ao confirmar agendamento. Tente novamente.');
    }
}

function showSuccessModal(data) {
    const modal = document.getElementById('successModal');
    const details = document.getElementById('successDetails');
    
    details.innerHTML = `
        <strong>${bookingState.selectedService.name}</strong><br>
        ${formatDateBR(bookingState.selectedDate)} às ${bookingState.selectedTime}<br>
        ${bookingState.selectedBarber ? `Com ${bookingState.selectedBarber.name}` : 'Com qualquer barbeiro disponível'}
    `;
    
    modal.style.display = 'flex';
}

// ===== RESUMO =====
function updateSummary() {
    if (!bookingState.selectedService) return;
    
    document.getElementById('summaryService').textContent = bookingState.selectedService.name;
    document.getElementById('summaryBarber').textContent = 
        bookingState.selectedBarber ? bookingState.selectedBarber.name : 'Qualquer um disponível';
    document.getElementById('summaryDate').textContent = 
        bookingState.selectedDate ? formatDateBR(bookingState.selectedDate) : '-';
    document.getElementById('summaryTime').textContent = bookingState.selectedTime || '-';
    document.getElementById('summaryDuration').textContent = 
        `${bookingState.selectedService.duration} minutos`;
    
    const subtotal = parseFloat(bookingState.selectedService.price);
    let discount = 0;
    
    if (bookingState.appliedCoupon) {
        if (bookingState.appliedCoupon.discount_type === 'percentage') {
            discount = subtotal * (bookingState.appliedCoupon.discount / 100);
        } else {
            discount = parseFloat(bookingState.appliedCoupon.discount);
        }
    }
    
    const total = subtotal - discount;
    
    document.getElementById('summarySubtotal').textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('summaryDiscount').textContent = `- R$ ${discount.toFixed(2).replace('.', ',')}`;
    document.getElementById('summaryTotal').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    
    document.getElementById('discountItem').style.display = discount > 0 ? 'flex' : 'none';
}

// ===== UTILITÁRIOS =====
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function formatDateBR(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`;
}

function maskPhone(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    
    if (value.length > 10) {
        value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
    } else if (value.length > 6) {
        value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/^(\d*)/, '($1');
    }
    
    e.target.value = value;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
