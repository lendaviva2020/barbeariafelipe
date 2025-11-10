/**
 * BOOKING SYSTEM - Extraído de BookingOptimized.tsx (1289 linhas)
 * Sistema completo de agendamento com 4 steps, validações, cupons e promoções
 */

// ========== CONFIGURAÇÕES ==========
const TIME_SLOTS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"
];

const QUICK_DATES = [
    { label: "Hoje", days: 0 },
    { label: "Amanhã", days: 1 },
    { label: "Em 2 dias", days: 2 },
    { label: "Em 3 dias", days: 3 },
    { label: "Em 1 semana", days: 7 }
];

const PAYMENT_METHODS = [
    { value: 'cash', label: 'Dinheiro', icon: '💵' },
    { value: 'credit_card', label: 'Cartão de Crédito', icon: '💳' },
    { value: 'debit_card', label: 'Cartão de Débito', icon: '💳' },
    { value: 'pix', label: 'PIX', icon: '📱' }
];

// ========== STATE MANAGEMENT ==========
const bookingState = {
    currentStep: 1,
    selectedService: null,
    selectedBarber: null,
    selectedDate: null,
    selectedTime: null,
    customerInfo: {
        name: '',
        phone: '',
        email: '',
        notes: ''
    },
    paymentMethod: 'cash',
    couponCode: '',
    appliedCoupon: null,
    appliedPromotion: null,
    enableRecurrence: false,
    recurrenceType: 'weekly',
    isSubmitting: false
};

// ========== UTILITY FUNCTIONS ==========
function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${year}-${month}-${day}`;
}

function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatPhoneForWhatsApp(phone) {
    return phone.replace(/\D/g, '');
}

function showToast(title, description, type = 'success') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <strong>${title}</strong>
        <p>${description}</p>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ========== API FUNCTIONS ==========
async function fetchServices() {
    try {
        const response = await fetch('/api/servicos/');
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
        return [];
    }
}

async function fetchBarbers() {
    try {
        const response = await fetch('/api/barbeiros/');
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar barbeiros:', error);
        return [];
    }
}

async function fetchAvailableSlots(date, barberId) {
    try {
        const response = await fetch(`/api/agendamentos/available-slots/?date=${date}&barber_id=${barberId}`);
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar horários:', error);
        return [];
    }
}

async function validateCoupon(code) {
    try {
        const response = await fetch('/api/cupons/validate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ code })
        });
        
        if (response.ok) {
            return await response.json();
        }
        return null;
    } catch (error) {
        console.error('Erro ao validar cupom:', error);
        return null;
    }
}

async function createBooking(data) {
    try {
        const response = await fetch('/api/agendamentos/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro ao criar agendamento');
        }
        
        return await response.json();
    } catch (error) {
        throw error;
    }
}

// ========== STEP NAVIGATION ==========
function updateProgress() {
    const progress = (bookingState.currentStep / 4) * 100;
    const progressBar = document.getElementById('bookingProgress');
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
    }
    
    // Update step indicators
    document.querySelectorAll('.step-indicator').forEach((indicator, index) => {
        const stepNum = index + 1;
        indicator.classList.toggle('active', stepNum === bookingState.currentStep);
        indicator.classList.toggle('completed', stepNum < bookingState.currentStep);
    });
}

function showStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.booking-step').forEach(step => {
        step.style.display = 'none';
    });
    
    // Show current step
    const currentStepEl = document.getElementById(`step${stepNumber}`);
    if (currentStepEl) {
        currentStepEl.style.display = 'block';
        currentStepEl.classList.add('animate-slide-up');
    }
    
    bookingState.currentStep = stepNumber;
    updateProgress();
    updateNavigationButtons();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevStepBtn');
    const nextBtn = document.getElementById('nextStepBtn');
    const submitBtn = document.getElementById('submitBookingBtn');
    
    if (prevBtn) {
        prevBtn.style.display = bookingState.currentStep === 1 ? 'none' : 'inline-flex';
    }
    
    if (nextBtn) {
        nextBtn.style.display = bookingState.currentStep === 4 ? 'none' : 'inline-flex';
    }
    
    if (submitBtn) {
        submitBtn.style.display = bookingState.currentStep === 4 ? 'inline-flex' : 'none';
    }
}

function goToNextStep() {
    if (!validateCurrentStep()) {
        return;
    }
    
    if (bookingState.currentStep < 4) {
        showStep(bookingState.currentStep + 1);
        
        // Load data for next step
        if (bookingState.currentStep === 2) {
            loadAvailableSlots();
        } else if (bookingState.currentStep === 4) {
            updateSummary();
        }
    }
}

function goToPreviousStep() {
    if (bookingState.currentStep > 1) {
        showStep(bookingState.currentStep - 1);
    }
}

// ========== VALIDATION ==========
function validateCurrentStep() {
    const step = bookingState.currentStep;
    
    if (step === 1) {
        if (!bookingState.selectedService) {
            showToast('Atenção', 'Selecione um serviço', 'error');
            return false;
        }
        if (!bookingState.selectedBarber) {
            showToast('Atenção', 'Selecione um barbeiro', 'error');
            return false;
        }
        return true;
    }
    
    if (step === 2) {
        if (!bookingState.selectedDate) {
            showToast('Atenção', 'Selecione uma data', 'error');
            return false;
        }
        if (!bookingState.selectedTime) {
            showToast('Atenção', 'Selecione um horário', 'error');
            return false;
        }
        return true;
    }
    
    if (step === 3) {
        const { name, phone, email } = bookingState.customerInfo;
        
        if (!name || name.trim().length < 3) {
            showToast('Atenção', 'Digite seu nome completo', 'error');
            return false;
        }
        
        if (!phone || phone.replace(/\D/g, '').length < 10) {
            showToast('Atenção', 'Digite um telefone válido', 'error');
            return false;
        }
        
        if (email && !email.includes('@')) {
            showToast('Atenção', 'Digite um e-mail válido', 'error');
            return false;
        }
        
        return true;
    }
    
    return true;
}

// ========== STEP 1: SERVICE & BARBER ==========
async function loadServicesAndBarbers() {
    const servicesContainer = document.getElementById('servicesGrid');
    const barbersContainer = document.getElementById('barbersGrid');
    
    // Show loading
    if (servicesContainer) {
        servicesContainer.innerHTML = '<div class="loader"></div>';
    }
    if (barbersContainer) {
        barbersContainer.innerHTML = '<div class="loader"></div>';
    }
    
    // Load services
    const services = await fetchServices();
    if (servicesContainer && services.length > 0) {
        servicesContainer.innerHTML = services
            .filter(s => s.active)
            .map(service => `
                <div class="service-card ${bookingState.selectedService === service.id ? 'selected' : ''}" 
                     onclick="selectService(${service.id}, '${service.name}', ${service.price}, ${service.duration})">
                    <div class="service-icon">✂️</div>
                    <h3 class="service-name">${service.name}</h3>
                    <p class="service-description">${service.description || ''}</p>
                    <div class="service-details">
                        <span class="service-price">${formatCurrency(service.price)}</span>
                        <span class="service-duration">${service.duration} min</span>
                    </div>
                    ${bookingState.selectedService === service.id ? '<div class="selected-badge">✓ Selecionado</div>' : ''}
                </div>
            `).join('');
    }
    
    // Load barbers
    const barbers = await fetchBarbers();
    if (barbersContainer && barbers.length > 0) {
        barbersContainer.innerHTML = barbers
            .filter(b => b.active)
            .map(barber => `
                <div class="barber-card ${bookingState.selectedBarber === barber.id ? 'selected' : ''}"
                     onclick="selectBarber(${barber.id}, '${barber.name}')">
                    <div class="barber-avatar">${barber.name.split(' ').map(n => n[0]).join('').slice(0, 2)}</div>
                    <h3 class="barber-name">${barber.name}</h3>
                    ${barber.specialty ? `<p class="barber-specialty">${barber.specialty}</p>` : ''}
                    ${bookingState.selectedBarber === barber.id ? '<div class="selected-badge">✓ Selecionado</div>' : ''}
                </div>
            `).join('');
    }
}

function selectService(id, name, price, duration) {
    bookingState.selectedService = id;
    bookingState.serviceData = { id, name, price, duration };
    loadServicesAndBarbers(); // Reload to update UI
}

function selectBarber(id, name) {
    bookingState.selectedBarber = id;
    bookingState.barberData = { id, name };
    loadServicesAndBarbers(); // Reload to update UI
}

// ========== STEP 2: DATE & TIME ==========
function initializeDatePicker() {
    const dateInput = document.getElementById('selectedDate');
    if (dateInput) {
        // Set min date to today
        const today = new Date();
        dateInput.min = formatDate(today);
        
        // Set max date to 60 days from now
        const maxDate = addDays(today, 60);
        dateInput.max = formatDate(maxDate);
        
        dateInput.addEventListener('change', (e) => {
            bookingState.selectedDate = e.target.value;
            loadAvailableSlots();
        });
    }
    
    // Quick date buttons
    const quickDatesContainer = document.getElementById('quickDates');
    if (quickDatesContainer) {
        quickDatesContainer.innerHTML = QUICK_DATES.map(qd => `
            <button class="btn btn-outline btn-sm" onclick="selectQuickDate(${qd.days})">
                ${qd.label}
            </button>
        `).join('');
    }
}

function selectQuickDate(days) {
    const date = addDays(new Date(), days);
    const dateStr = formatDate(date);
    bookingState.selectedDate = dateStr;
    
    const dateInput = document.getElementById('selectedDate');
    if (dateInput) {
        dateInput.value = dateStr;
    }
    
    loadAvailableSlots();
}

async function loadAvailableSlots() {
    if (!bookingState.selectedDate || !bookingState.selectedBarber) {
        return;
    }
    
    const slotsContainer = document.getElementById('timeSlotsGrid');
    if (!slotsContainer) return;
    
    slotsContainer.innerHTML = '<div class="loader"></div>';
    
    const slots = await fetchAvailableSlots(bookingState.selectedDate, bookingState.selectedBarber);
    
    if (slots.length === 0) {
        slotsContainer.innerHTML = '<p class="text-center">Nenhum horário disponível para esta data</p>';
        return;
    }
    
    slotsContainer.innerHTML = slots.map(slot => `
        <button class="time-slot ${!slot.available ? 'disabled' : ''} ${bookingState.selectedTime === slot.time_slot ? 'selected' : ''}"
                onclick="selectTimeSlot('${slot.time_slot}')"
                ${!slot.available ? 'disabled' : ''}>
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            ${slot.time_slot}
        </button>
    `).join('');
}

function selectTimeSlot(time) {
    bookingState.selectedTime = time;
    loadAvailableSlots(); // Reload to update UI
}

// ========== STEP 3: CUSTOMER INFO ==========
function initializeCustomerInfo() {
    const nameInput = document.getElementById('customerName');
    const phoneInput = document.getElementById('customerPhone');
    const emailInput = document.getElementById('customerEmail');
    const notesInput = document.getElementById('customerNotes');
    
    // Pre-fill from localStorage if available
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.name) bookingState.customerInfo.name = user.name;
    if (user.phone) bookingState.customerInfo.phone = user.phone;
    if (user.email) bookingState.customerInfo.email = user.email;
    
    if (nameInput) nameInput.value = bookingState.customerInfo.name;
    if (phoneInput) phoneInput.value = bookingState.customerInfo.phone;
    if (emailInput) emailInput.value = bookingState.customerInfo.email;
    
    // Event listeners
    if (nameInput) {
        nameInput.addEventListener('input', (e) => {
            bookingState.customerInfo.name = e.target.value;
        });
    }
    
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            // Format phone
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            
            if (value.length > 6) {
                value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
            } else if (value.length > 2) {
                value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
            }
            
            e.target.value = value;
            bookingState.customerInfo.phone = value;
        });
    }
    
    if (emailInput) {
        emailInput.addEventListener('input', (e) => {
            bookingState.customerInfo.email = e.target.value;
        });
    }
    
    if (notesInput) {
        notesInput.addEventListener('input', (e) => {
            bookingState.customerInfo.notes = e.target.value;
        });
    }
}

// Coupon handling
async function applyCoupon() {
    const couponInput = document.getElementById('couponInput');
    if (!couponInput || !couponInput.value) {
        showToast('Atenção', 'Digite um código de cupom', 'error');
        return;
    }
    
    const code = couponInput.value.toUpperCase();
    const coupon = await validateCoupon(code);
    
    if (coupon) {
        bookingState.appliedCoupon = coupon;
        bookingState.couponCode = code;
        showToast('Sucesso', `Cupom aplicado! Desconto de ${coupon.discount_type === 'percentage' ? coupon.discount + '%' : formatCurrency(coupon.discount)}`, 'success');
        updateSummary();
    } else {
        showToast('Erro', 'Cupom inválido ou expirado', 'error');
    }
}

function removeCoupon() {
    bookingState.appliedCoupon = null;
    bookingState.couponCode = '';
    const couponInput = document.getElementById('couponInput');
    if (couponInput) couponInput.value = '';
    showToast('Info', 'Cupom removido', 'info');
    updateSummary();
}

// ========== STEP 4: PAYMENT & SUMMARY ==========
function initializePayment() {
    const paymentMethodsContainer = document.getElementById('paymentMethods');
    if (paymentMethodsContainer) {
        paymentMethodsContainer.innerHTML = PAYMENT_METHODS.map(pm => `
            <div class="payment-method ${bookingState.paymentMethod === pm.value ? 'selected' : ''}"
                 onclick="selectPaymentMethod('${pm.value}')">
                <span class="payment-icon">${pm.icon}</span>
                <span class="payment-label">${pm.label}</span>
                ${bookingState.paymentMethod === pm.value ? '<span class="selected-check">✓</span>' : ''}
            </div>
        `).join('');
    }
    
    updateSummary();
}

function selectPaymentMethod(method) {
    bookingState.paymentMethod = method;
    initializePayment(); // Reload to update UI
}

function updateSummary() {
    // Calculate price
    let basePrice = bookingState.serviceData?.price || 0;
    let discount = 0;
    
    if (bookingState.appliedCoupon) {
        const coupon = bookingState.appliedCoupon;
        if (coupon.discount_type === 'percentage') {
            discount = (basePrice * coupon.discount) / 100;
        } else {
            discount = coupon.discount;
        }
    }
    
    const finalPrice = Math.max(0, basePrice - discount);
    
    // Update summary HTML
    const summaryEl = document.getElementById('bookingSummary');
    if (summaryEl) {
        summaryEl.innerHTML = `
            <div class="summary-item">
                <span>Serviço:</span>
                <strong>${bookingState.serviceData?.name || '-'}</strong>
            </div>
            <div class="summary-item">
                <span>Barbeiro:</span>
                <strong>${bookingState.barberData?.name || '-'}</strong>
            </div>
            <div class="summary-item">
                <span>Data:</span>
                <strong>${bookingState.selectedDate ? new Date(bookingState.selectedDate).toLocaleDateString('pt-BR') : '-'}</strong>
            </div>
            <div class="summary-item">
                <span>Horário:</span>
                <strong>${bookingState.selectedTime || '-'}</strong>
            </div>
            <div class="summary-item">
                <span>Duração:</span>
                <strong>${bookingState.serviceData?.duration || 0} minutos</strong>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-item">
                <span>Preço base:</span>
                <span>${formatCurrency(basePrice)}</span>
            </div>
            ${discount > 0 ? `
                <div class="summary-item discount">
                    <span>Desconto (${bookingState.couponCode}):</span>
                    <span>-${formatCurrency(discount)}</span>
                </div>
            ` : ''}
            <div class="summary-divider"></div>
            <div class="summary-item total">
                <span>Total:</span>
                <strong>${formatCurrency(finalPrice)}</strong>
            </div>
        `;
    }
}

// ========== SUBMIT BOOKING ==========
async function submitBooking() {
    if (!validateCurrentStep()) {
        return;
    }
    
    if (bookingState.isSubmitting) {
        return;
    }
    
    bookingState.isSubmitting = true;
    const submitBtn = document.getElementById('submitBookingBtn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="loader"></div> Processando...';
    }
    
    try {
        // Calculate final price
        let finalPrice = bookingState.serviceData?.price || 0;
        if (bookingState.appliedCoupon) {
            const coupon = bookingState.appliedCoupon;
            if (coupon.discount_type === 'percentage') {
                finalPrice -= (finalPrice * coupon.discount) / 100;
            } else {
                finalPrice -= coupon.discount;
            }
        }
        finalPrice = Math.max(0, finalPrice);
        
        // Prepare booking data
        const bookingData = {
            service_id: bookingState.selectedService,
            barber_id: bookingState.selectedBarber,
            appointment_date: bookingState.selectedDate,
            appointment_time: bookingState.selectedTime,
            customer_name: bookingState.customerInfo.name,
            customer_phone: bookingState.customerInfo.phone,
            customer_email: bookingState.customerInfo.email,
            notes: bookingState.customerInfo.notes,
            payment_method: bookingState.paymentMethod,
            price: finalPrice,
            coupon_code: bookingState.couponCode || null
        };
        
        // Create booking
        const result = await createBooking(bookingData);
        
        showToast('Sucesso', 'Agendamento realizado com sucesso!', 'success');
        
        // Send WhatsApp confirmation (if phone provided)
        if (bookingState.customerInfo.phone) {
            const phone = formatPhoneForWhatsApp(bookingState.customerInfo.phone);
            const message = `Olá ${bookingState.customerInfo.name}! Seu agendamento foi confirmado:\n\n` +
                          `📅 Data: ${new Date(bookingState.selectedDate).toLocaleDateString('pt-BR')}\n` +
                          `⏰ Horário: ${bookingState.selectedTime}\n` +
                          `✂️ Serviço: ${bookingState.serviceData.name}\n` +
                          `👨‍💼 Barbeiro: ${bookingState.barberData.name}\n` +
                          `💰 Valor: ${formatCurrency(finalPrice)}\n\n` +
                          `Aguardamos você! 🎩`;
            
            // Open WhatsApp (optional)
            // window.open(`https://wa.me/55${phone}?text=${encodeURIComponent(message)}`, '_blank');
        }
        
        // Redirect to success page or history
        setTimeout(() => {
            window.location.href = '/historico/';
        }, 2000);
        
    } catch (error) {
        console.error('Erro ao criar agendamento:', error);
        showToast('Erro', error.message || 'Erro ao criar agendamento. Tente novamente.', 'error');
        
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Confirmar Agendamento';
        }
    } finally {
        bookingState.isSubmitting = false;
    }
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    // Initialize first step
    loadServicesAndBarbers();
    initializeDatePicker();
    initializeCustomerInfo();
    initializePayment();
    updateProgress();
    
    // Event listeners for navigation
    const prevBtn = document.getElementById('prevStepBtn');
    if (prevBtn) {
        prevBtn.addEventListener('click', goToPreviousStep);
    }
    
    const nextBtn = document.getElementById('nextStepBtn');
    if (nextBtn) {
        nextBtn.addEventListener('click', goToNextStep);
    }
    
    const submitBtn = document.getElementById('submitBookingBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitBooking);
    }
    
    // Coupon button
    const applyCouponBtn = document.getElementById('applyCouponBtn');
    if (applyCouponBtn) {
        applyCouponBtn.addEventListener('click', applyCoupon);
    }
});
