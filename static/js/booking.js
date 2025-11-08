// Booking JavaScript
let currentStep = 1;
let bookingData = {
    service: null,
    date: null,
    time: null,
    barber: null,
    customer_name: '',
    customer_phone: '',
    customer_email: '',
    notes: '',
    payment_method: 'cash',
    price: 0
};

document.addEventListener('DOMContentLoaded', () => {
    // Verificar autenticação
    if (!auth.isAuthenticated()) {
        window.location.href = '/auth/?redirect=/agendar/';
        return;
    }
    
    loadServices();
    loadBarbers();
    setupNavigation();
    setupFormHandlers();
});

// Carregar serviços
async function loadServices() {
    try {
        const response = await fetchAPI('/servicos/');
        const services = await response.json();
        
        const servicesList = document.getElementById('servicesList');
        servicesList.innerHTML = '';
        
        services.forEach(service => {
            const serviceCard = document.createElement('div');
            serviceCard.className = 'service-card';
            serviceCard.innerHTML = `
                <h3>${service.name}</h3>
                <p>${service.description}</p>
                <div class="service-info">
                    <span class="service-price">R$ ${service.price}</span>
                    <span class="service-duration">${service.duration} min</span>
                </div>
            `;
            serviceCard.addEventListener('click', () => selectService(service));
            servicesList.appendChild(serviceCard);
        });
    } catch (error) {
        console.error('Error loading services:', error);
        showMessage(document.getElementById('bookingMessage'), 'Erro ao carregar serviços', 'error');
    }
}

// Carregar barbeiros
async function loadBarbers() {
    try {
        const response = await fetchAPI('/barbeiros/');
        const barbers = await response.json();
        
        const barberSelect = document.getElementById('barber');
        barberSelect.innerHTML = '<option value="">Selecione um barbeiro</option>';
        
        barbers.forEach(barber => {
            const option = document.createElement('option');
            option.value = barber.id;
            option.textContent = barber.name;
            option.dataset.barberData = JSON.stringify(barber);
            barberSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading barbers:', error);
    }
}

// Selecionar serviço
function selectService(service) {
    bookingData.service = service.id;
    bookingData.price = parseFloat(service.price);
    
    document.querySelectorAll('.service-card').forEach(card => card.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    
    nextStep();
}

// Navegação entre steps
function setupNavigation() {
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            nextStep();
        }
    });
    
    prevBtn.addEventListener('click', prevStep);
    
    document.getElementById('bookingForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitBooking();
    });
}

function nextStep() {
    if (currentStep < 4) {
        currentStep++;
        updateStepUI();
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        updateStepUI();
    }
}

function updateStepUI() {
    // Atualizar steps visuais
    document.querySelectorAll('.booking-step').forEach((step, index) => {
        step.style.display = (index + 1) === currentStep ? 'block' : 'none';
    });
    
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        if (index + 1 < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (index + 1 === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
    
    // Atualizar botões
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    prevBtn.style.display = currentStep > 1 ? 'block' : 'none';
    nextBtn.style.display = currentStep < 4 ? 'block' : 'none';
    submitBtn.style.display = currentStep === 4 ? 'block' : 'none';
    
    // Atualizar resumo no step 4
    if (currentStep === 4) {
        updateSummary();
    }
}

function validateStep(step) {
    switch(step) {
        case 1:
            if (!bookingData.service) {
                alert('Selecione um serviço');
                return false;
            }
            return true;
        case 2:
            const date = document.getElementById('date').value;
            const barber = document.getElementById('barber').value;
            const time = document.querySelector('.time-slot.selected')?.dataset.time;
            
            if (!date || !barber || !time) {
                alert('Preencha data, barbeiro e horário');
                return false;
            }
            
            bookingData.date = date;
            bookingData.barber = parseInt(barber);
            bookingData.time = time;
            return true;
        case 3:
            const name = document.getElementById('customer_name').value;
            const phone = document.getElementById('customer_phone').value;
            const payment = document.getElementById('payment_method').value;
            
            if (!name || !phone || !payment) {
                alert('Preencha todos os campos obrigatórios');
                return false;
            }
            
            bookingData.customer_name = name;
            bookingData.customer_phone = phone;
            bookingData.customer_email = document.getElementById('customer_email').value;
            bookingData.notes = document.getElementById('notes').value;
            bookingData.payment_method = payment;
            return true;
        default:
            return true;
    }
}

function updateSummary() {
    const barberSelect = document.getElementById('barber');
    const selectedBarber = barberSelect.options[barberSelect.selectedIndex].text;
    
    document.getElementById('summary_service').textContent = document.querySelector('.service-card.selected h3')?.textContent || '-';
    document.getElementById('summary_date').textContent = formatDate(bookingData.date);
    document.getElementById('summary_time').textContent = bookingData.time;
    document.getElementById('summary_barber').textContent = selectedBarber;
    document.getElementById('summary_customer').textContent = bookingData.customer_name;
    document.getElementById('summary_phone').textContent = bookingData.customer_phone;
    document.getElementById('summary_payment').textContent = document.getElementById('payment_method').options[document.getElementById('payment_method').selectedIndex].text;
    document.getElementById('summary_price').textContent = formatCurrency(bookingData.price);
}

async function submitBooking() {
    const submitBtn = document.getElementById('submitBtn');
    const submitBtnText = document.getElementById('submitBtnText');
    const submitBtnLoader = document.getElementById('submitBtnLoader');
    
    submitBtnText.style.display = 'none';
    submitBtnLoader.style.display = 'inline-block';
    submitBtn.disabled = true;
    
    try {
        const response = await fetchAPI('/agendamentos/create/', {
            method: 'POST',
            body: JSON.stringify(bookingData),
        });
        
        if (response.ok) {
            const result = await response.json();
            showMessage(document.getElementById('bookingMessage'), 'Agendamento realizado com sucesso!', 'success');
            
            // Redirecionar para WhatsApp
            setTimeout(() => {
                const whatsappMsg = `Olá! Acabei de agendar um horário:\n\nServiço: ${document.querySelector('.service-card.selected h3').textContent}\nData: ${formatDate(bookingData.date)}\nHorário: ${bookingData.time}\nValor: ${formatCurrency(bookingData.price)}`;
                const whatsappURL = `https://wa.me/5545999417111?text=${encodeURIComponent(whatsappMsg)}`;
                window.open(whatsappURL, '_blank');
                window.location.href = '/historico/';
            }, 2000);
        } else {
            const error = await response.json();
            showMessage(document.getElementById('bookingMessage'), error.error || 'Erro ao criar agendamento', 'error');
        }
    } catch (error) {
        console.error('Booking error:', error);
        showMessage(document.getElementById('bookingMessage'), 'Erro ao criar agendamento', 'error');
    } finally {
        submitBtnText.style.display = 'inline';
        submitBtnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Event handlers
function setupFormHandlers() {
    const dateInput = document.getElementById('date');
    const barberSelect = document.getElementById('barber');
    
    // Quando data ou barbeiro mudar, carregar horários
    dateInput.addEventListener('change', loadAvailableSlots);
    barberSelect.addEventListener('change', loadAvailableSlots);
}

async function loadAvailableSlots() {
    const date = document.getElementById('date').value;
    const barber = document.getElementById('barber').value;
    
    if (!date || !barber) return;
    
    const timeSlotsContainer = document.getElementById('timeSlots');
    timeSlotsContainer.innerHTML = '<div class="loader"></div>';
    
    try {
        const response = await fetchAPI(`/agendamentos/available-slots/?date=${date}&barber_id=${barber}`);
        const slots = await response.json();
        
        timeSlotsContainer.innerHTML = '';
        slots.forEach(slot => {
            const slotBtn = document.createElement('button');
            slotBtn.type = 'button';
            slotBtn.className = `time-slot ${slot.available ? '' : 'disabled'}`;
            slotBtn.textContent = slot.time_slot;
            slotBtn.dataset.time = slot.time_slot;
            slotBtn.disabled = !slot.available;
            
            if (slot.available) {
                slotBtn.addEventListener('click', function() {
                    document.querySelectorAll('.time-slot').forEach(btn => btn.classList.remove('selected'));
                    this.classList.add('selected');
                });
            }
            
            timeSlotsContainer.appendChild(slotBtn);
        });
    } catch (error) {
        console.error('Error loading slots:', error);
        timeSlotsContainer.innerHTML = '<p class="error">Erro ao carregar horários</p>';
    }
}

