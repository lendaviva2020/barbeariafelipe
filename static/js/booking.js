/**
 * BOOKING SYSTEM - Sistema Moderno de Agendamento
 * Integração completa com API REST Django
 */

// ========== CONFIGURAÇÕES ==========
const API_BASE = '/api';
const TIME_SLOTS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "13:00", "13:30", "14:00", "14:30",
    "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"
];

// ========== STATE MANAGEMENT ==========
const bookingState = {
    currentStep: 1,
    selectedService: null,
    selectedBarber: null,
    selectedDate: null,
    selectedTime: null,
    coupon: null,
    discount: 0,
    currentMonth: new Date().getMonth(),
    currentYear: new Date().getFullYear()
};

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', function() {
    initializeBookingSystem();
});

function initializeBookingSystem() {
    loadServices();
    loadBarbers();
    initCalendar();
    setupStepNavigation();
    setupFormEvents();
}

// ========== API CALLS ==========
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ========== LOAD SERVICES ==========
async function loadServices() {
    const servicesGrid = document.getElementById('servicesGrid');
    
    if (!servicesGrid) {
        console.error('servicesGrid element not found');
        return;
    }
    
    try {
        console.log('Carregando serviços da API...');
        const allServices = await apiCall('/api/servicos/');
        console.log('Serviços recebidos:', allServices);
        
        // Filtrar apenas serviços individuais (não combos)
        const services = allServices.filter(s => !s.is_combo);
        console.log('Serviços individuais:', services);
        
        servicesGrid.innerHTML = '';
        
        if (!services || services.length === 0) {
            servicesGrid.innerHTML = '<p class="empty-state">Nenhum serviço disponível no momento.</p>';
            return;
        }
        
        services.forEach(service => {
            const serviceCard = document.createElement('div');
            serviceCard.className = 'service-card';
            
            // Determinar ícone baseado na categoria
            const icon = getServiceIcon(service.category || 'haircut');
            
            serviceCard.innerHTML = `
                <div class="service-icon">
                    <i class="${icon}"></i>
                </div>
                <div class="service-duration">${service.duration} min</div>
                <h3>${service.name}</h3>
                <p>${service.description || 'Serviço profissional de qualidade'}</p>
                <div class="service-price">R$ ${parseFloat(service.price).toFixed(2).replace('.', ',')}</div>
            `;
            
            serviceCard.addEventListener('click', () => selectService(serviceCard, service));
            servicesGrid.appendChild(serviceCard);
        });
        
        console.log(`${services.length} serviços renderizados`);
        
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
        servicesGrid.innerHTML = `<p class="empty-state">Erro ao carregar serviços: ${error.message}</p>`;
    }
}

function getServiceIcon(category) {
    const icons = {
        'haircut': 'fas fa-cut',
        'beard': 'fas fa-user',
        'combo': 'fas fa-gem',
        'treatment': 'fas fa-spa'
    };
    return icons[category] || 'fas fa-cut';
}

function selectService(card, service) {
    document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    bookingState.selectedService = service;
    document.getElementById('nextStep1').disabled = false;
}

// ========== LOAD BARBERS ==========
async function loadBarbers() {
    const barbersGrid = document.getElementById('barbersGrid');
    
    try {
        const barbers = await apiCall('/api/barbeiros/');
        
        barbersGrid.innerHTML = '';
        
        // Opção "Qualquer barbeiro"
        const anyBarberCard = document.createElement('div');
        anyBarberCard.className = 'barber-card selected';
        anyBarberCard.innerHTML = `
            <div class="barber-avatar">
                <i class="fas fa-random"></i>
            </div>
            <h3>Qualquer Barbeiro</h3>
            <p>Será atendido por qualquer barbeiro disponível</p>
        `;
        anyBarberCard.addEventListener('click', () => selectBarber(anyBarberCard, null));
        barbersGrid.appendChild(anyBarberCard);
        
        // Barbeiros disponíveis
        if (barbers && barbers.length > 0) {
            barbers.forEach(barber => {
                const barberCard = document.createElement('div');
                barberCard.className = 'barber-card';
                barberCard.innerHTML = `
                    <div class="barber-avatar">
                        ${barber.photo_url ? 
                            `<img src="${barber.photo_url}" alt="${barber.name}">` : 
                            '<i class="fas fa-user"></i>'}
                    </div>
                    <h3>${barber.name}</h3>
                    <p>${barber.specialty || 'Barbeiro profissional'}</p>
                    <div class="barber-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt"></i>
                    </div>
                `;
                barberCard.addEventListener('click', () => selectBarber(barberCard, barber));
                barbersGrid.appendChild(barberCard);
            });
        }
        
    } catch (error) {
        barbersGrid.innerHTML = '<p class="empty-state">Erro ao carregar barbeiros.</p>';
    }
}

function selectBarber(card, barber) {
    document.querySelectorAll('.barber-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    bookingState.selectedBarber = barber;
}

// ========== CALENDAR ==========
function initCalendar() {
    renderCalendar();
}

function renderCalendar() {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';
    
    const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                       "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    
    // Header
    const header = document.createElement('div');
    header.className = 'calendar-header';
    header.innerHTML = `
        <button type="button" id="prevMonth"><i class="fas fa-chevron-left"></i></button>
        <h4>${monthNames[bookingState.currentMonth]} ${bookingState.currentYear}</h4>
        <button type="button" id="nextMonth"><i class="fas fa-chevron-right"></i></button>
    `;
    calendar.appendChild(header);
    
    // Grid de dias
    const daysGrid = document.createElement('div');
    daysGrid.className = 'calendar-grid';
    
    // Dias da semana
    const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
    weekDays.forEach(day => {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = day;
        daysGrid.appendChild(dayElement);
    });
    
    // Dias do mês
    const firstDay = new Date(bookingState.currentYear, bookingState.currentMonth, 1);
    const lastDay = new Date(bookingState.currentYear, bookingState.currentMonth + 1, 0);
    const daysInMonth = lastDay.getDate();
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Dias vazios antes do primeiro dia
    for (let i = 0; i < firstDay.getDay(); i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-date disabled';
        daysGrid.appendChild(emptyDay);
    }
    
    // Dias do mês
    for (let i = 1; i <= daysInMonth; i++) {
        const dateElement = document.createElement('div');
        dateElement.className = 'calendar-date';
        dateElement.textContent = i;
        
        const date = new Date(bookingState.currentYear, bookingState.currentMonth, i);
        date.setHours(0, 0, 0, 0);
        
        if (date < today) {
            dateElement.classList.add('disabled');
        } else {
            dateElement.addEventListener('click', () => selectDate(dateElement, date));
        }
        
        daysGrid.appendChild(dateElement);
    }
    
    calendar.appendChild(daysGrid);
    
    // Event listeners para navegação
    document.getElementById('prevMonth').addEventListener('click', () => {
        if (bookingState.currentMonth === 0) {
            bookingState.currentMonth = 11;
            bookingState.currentYear--;
        } else {
            bookingState.currentMonth--;
        }
        renderCalendar();
    });
    
    document.getElementById('nextMonth').addEventListener('click', () => {
        if (bookingState.currentMonth === 11) {
            bookingState.currentMonth = 0;
            bookingState.currentYear++;
        } else {
            bookingState.currentMonth++;
        }
        renderCalendar();
    });
}

function selectDate(element, date) {
    document.querySelectorAll('.calendar-date').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');
    bookingState.selectedDate = date;
    loadAvailableSlots();
}

// ========== LOAD AVAILABLE SLOTS ==========
async function loadAvailableSlots() {
    const slotsContainer = document.getElementById('availableSlots');
    
    if (!bookingState.selectedDate) {
        slotsContainer.innerHTML = '<p class="empty-state">Selecione uma data primeiro</p>';
        return;
    }
    
    slotsContainer.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Carregando horários...</p></div>';
    
    try {
        const dateStr = bookingState.selectedDate.toISOString().split('T')[0];
        const barberId = bookingState.selectedBarber?.id || '';
        const serviceId = bookingState.selectedService?.id || '';
        
        const availableSlots = await apiCall(
            `/api/agendamentos/available-slots/?date=${dateStr}&barber_id=${barberId}&service_id=${serviceId}`
        );
        
        slotsContainer.innerHTML = '';
        
        if (!availableSlots || availableSlots.length === 0) {
            slotsContainer.innerHTML = '<p class="empty-state">Nenhum horário disponível nesta data</p>';
            return;
        }
        
        availableSlots.forEach(slot => {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = slot.time || slot;
            
            if (slot.available === false) {
                timeSlot.classList.add('disabled');
            } else {
                timeSlot.addEventListener('click', () => selectTimeSlot(timeSlot, slot.time || slot));
            }
            
            slotsContainer.appendChild(timeSlot);
        });
        
    } catch (error) {
        // Fallback para horários padrão
        slotsContainer.innerHTML = '';
        TIME_SLOTS.forEach(time => {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = time;
            timeSlot.addEventListener('click', () => selectTimeSlot(timeSlot, time));
            slotsContainer.appendChild(timeSlot);
        });
    }
}

function selectTimeSlot(element, time) {
    document.querySelectorAll('.time-slot').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');
    bookingState.selectedTime = time;
    document.getElementById('nextStep3').disabled = false;
}

// ========== NAVIGATION ==========
function setupStepNavigation() {
    document.getElementById('nextStep1')?.addEventListener('click', () => navigateToStep(2));
    document.getElementById('nextStep2')?.addEventListener('click', () => navigateToStep(3));
    document.getElementById('nextStep3')?.addEventListener('click', () => {
        updateBookingSummary();
        navigateToStep(4);
    });
    
    document.getElementById('prevStep2')?.addEventListener('click', () => navigateToStep(1));
    document.getElementById('prevStep3')?.addEventListener('click', () => navigateToStep(2));
    document.getElementById('prevStep4')?.addEventListener('click', () => navigateToStep(3));
}

function navigateToStep(step) {
    // Ocultar etapa atual
    const currentStepEl = document.getElementById(`step-${bookingState.currentStep}`);
    if (currentStepEl) {
        currentStepEl.classList.remove('active');
        currentStepEl.style.display = 'none';
    }
    
    // Atualizar indicadores de progresso
    document.querySelectorAll('.step').forEach(stepElement => {
        const stepNumber = parseInt(stepElement.getAttribute('data-step'));
        
        if (stepNumber < step) {
            stepElement.classList.add('completed');
            stepElement.classList.remove('active');
        } else if (stepNumber === step) {
            stepElement.classList.add('active');
            stepElement.classList.remove('completed');
        } else {
            stepElement.classList.remove('active', 'completed');
        }
    });
    
    // Mostrar nova etapa
    const newStepEl = document.getElementById(`step-${step}`);
    if (newStepEl) {
        newStepEl.style.display = 'block';
        newStepEl.classList.add('active');
    }
    
    bookingState.currentStep = step;
    
    // Scroll suave para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========== FORM EVENTS ==========
function setupFormEvents() {
    const applyCouponBtn = document.getElementById('applyCoupon');
    if (applyCouponBtn) {
        applyCouponBtn.addEventListener('click', validateCoupon);
    }
    
    const confirmBtn = document.getElementById('confirmBooking');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', confirmBooking);
    }
}

// ========== VALIDATE COUPON ==========
async function validateCoupon() {
    const couponCode = document.getElementById('couponCode').value.trim();
    const feedback = document.getElementById('couponFeedback');
    
    if (!couponCode) {
        feedback.textContent = 'Por favor, digite um código de cupom.';
        feedback.className = 'coupon-feedback error';
        return;
    }
    
    feedback.textContent = 'Validando...';
    feedback.className = 'coupon-feedback';
    
    try {
        const result = await apiCall('/api/agendamentos/validate-cupom/', {
            method: 'POST',
            body: JSON.stringify({ code: couponCode })
        });
        
        if (result.valid) {
            feedback.textContent = `Cupom aplicado! Desconto: ${result.discount_display || result.discount}`;
            feedback.className = 'coupon-feedback success';
            bookingState.coupon = result;
            bookingState.discount = parseFloat(result.discount) || 0;
            updateBookingSummary();
        } else {
            feedback.textContent = 'Cupom inválido ou expirado.';
            feedback.className = 'coupon-feedback error';
        }
        
    } catch (error) {
        feedback.textContent = 'Erro ao validar cupom.';
        feedback.className = 'coupon-feedback error';
    }
}

// ========== UPDATE SUMMARY ==========
function updateBookingSummary() {
    // Serviço
    if (bookingState.selectedService) {
        document.getElementById('summaryService').textContent = bookingState.selectedService.name;
        document.getElementById('summaryDuration').textContent = `${bookingState.selectedService.duration} min`;
    }
    
    // Barbeiro
    const barberName = bookingState.selectedBarber ? 
        bookingState.selectedBarber.name : 
        'Qualquer um disponível';
    document.getElementById('summaryBarber').textContent = barberName;
    
    // Data
    if (bookingState.selectedDate) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById('summaryDate').textContent = 
            bookingState.selectedDate.toLocaleDateString('pt-BR', options);
    }
    
    // Horário
    if (bookingState.selectedTime) {
        document.getElementById('summaryTime').textContent = bookingState.selectedTime;
    }
    
    // Cálculo de preços
    if (bookingState.selectedService) {
        const price = parseFloat(bookingState.selectedService.price);
        let discount = 0;
        
        if (bookingState.coupon) {
            if (bookingState.coupon.discount_type === 'percentage') {
                discount = (price * bookingState.discount) / 100;
            } else {
                discount = bookingState.discount;
            }
        }
        
        const subtotal = price;
        const total = subtotal - discount;
        
        document.getElementById('summarySubtotal').textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
        document.getElementById('summaryDiscount').textContent = `- R$ ${discount.toFixed(2).replace('.', ',')}`;
        document.getElementById('summaryTotal').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
        
        // Mostrar/ocultar desconto
        const discountItem = document.getElementById('discountItem');
        if (discount > 0) {
            discountItem.style.display = 'flex';
        } else {
            discountItem.style.display = 'none';
        }
    }
}

// ========== CONFIRM BOOKING ==========
async function confirmBooking() {
    const customerName = document.getElementById('customerName').value.trim();
    const customerPhone = document.getElementById('customerPhone').value.trim();
    const customerEmail = document.getElementById('customerEmail').value.trim();
    const notes = document.getElementById('notes').value.trim();
    
    // Validação
    if (!customerName || !customerPhone) {
        alert('Por favor, preencha nome e telefone.');
        return;
    }
    
    if (!bookingState.selectedService || !bookingState.selectedDate || !bookingState.selectedTime) {
        alert('Por favor, complete todas as etapas do agendamento.');
        return;
    }
    
    // Preparar dados
    const bookingData = {
        service: bookingState.selectedService.id,
        barber: bookingState.selectedBarber?.id || null,
        appointment_date: bookingState.selectedDate.toISOString().split('T')[0],
        appointment_time: bookingState.selectedTime,
        customer_name: customerName,
        customer_phone: customerPhone,
        customer_email: customerEmail,
        notes: notes,
        payment_method: 'cash',
        price: bookingState.selectedService.price,
        discount_amount: 0,
        coupon_code: bookingState.coupon?.code || ''
    };
    
    // Calcular desconto
    if (bookingState.coupon) {
        const price = parseFloat(bookingState.selectedService.price);
        if (bookingState.coupon.discount_type === 'percentage') {
            bookingData.discount_amount = (price * bookingState.discount) / 100;
        } else {
            bookingData.discount_amount = bookingState.discount;
        }
    }
    
    // Desabilitar botão
    const confirmBtn = document.getElementById('confirmBooking');
    confirmBtn.disabled = true;
    confirmBtn.innerHTML = '<div class="spinner"></div> Processando...';
    
    try {
        const result = await apiCall('/api/agendamentos/create/', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
        
        // Mostrar modal de sucesso
        showSuccessModal(result);
        
    } catch (error) {
        alert('Erro ao criar agendamento. Tente novamente.');
        confirmBtn.disabled = false;
        confirmBtn.innerHTML = '<i class="fas fa-check"></i> Confirmar Agendamento';
    }
}

// ========== SUCCESS MODAL ==========
function showSuccessModal(appointmentData) {
    const modal = document.getElementById('successModal');
    const successDetails = document.getElementById('successDetails');
    
    let details = '';
    if (bookingState.selectedService) {
        details += `<strong>Serviço:</strong> ${bookingState.selectedService.name}<br>`;
    }
    if (bookingState.selectedBarber) {
        details += `<strong>Barbeiro:</strong> ${bookingState.selectedBarber.name}<br>`;
    } else {
        details += `<strong>Barbeiro:</strong> Qualquer um disponível<br>`;
    }
    if (bookingState.selectedDate && bookingState.selectedTime) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        details += `<strong>Data:</strong> ${bookingState.selectedDate.toLocaleDateString('pt-BR', options)}<br>`;
        details += `<strong>Horário:</strong> ${bookingState.selectedTime}`;
    }
    
    successDetails.innerHTML = details;
    modal.classList.add('show');
    
    // Fechar modal ao clicar fora
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.remove('show');
        }
    });
}

// ========== UTILITY FUNCTIONS ==========
function formatCurrency(value) {
    return `R$ ${parseFloat(value).toFixed(2).replace('.', ',')}`;
}

function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('pt-BR', options);
}

// ========== ERROR HANDLING ==========
function showError(message) {
    alert(message);
}

function showSuccess(message) {
    alert(message);
}

