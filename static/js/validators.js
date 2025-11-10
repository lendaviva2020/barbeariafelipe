/**
 * Validadores brasileiros: CPF, CNPJ, Telefone
 * Para uso no frontend
 */

function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11) return false;
    if (/^(\d)\1+$/.test(cpf)) return false;
    
    // Primeiro dígito
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf[i]) * (10 - i);
    }
    let resto = soma % 11;
    let digito1 = resto < 2 ? 0 : 11 - resto;
    
    if (parseInt(cpf[9]) !== digito1) return false;
    
    // Segundo dígito
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf[i]) * (11 - i);
    }
    resto = soma % 11;
    let digito2 = resto < 2 ? 0 : 11 - resto;
    
    return parseInt(cpf[10]) === digito2;
}

function validateCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    
    if (cnpj.length !== 14) return false;
    if (/^(\d)\1+$/.test(cnpj)) return false;
    
    // Primeiro dígito
    const pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let soma = 0;
    for (let i = 0; i < 12; i++) {
        soma += parseInt(cnpj[i]) * pesos1[i];
    }
    let resto = soma % 11;
    let digito1 = resto < 2 ? 0 : 11 - resto;
    
    if (parseInt(cnpj[12]) !== digito1) return false;
    
    // Segundo dígito
    const pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    soma = 0;
    for (let i = 0; i < 13; i++) {
        soma += parseInt(cnpj[i]) * pesos2[i];
    }
    resto = soma % 11;
    let digito2 = resto < 2 ? 0 : 11 - resto;
    
    return parseInt(cnpj[13]) === digito2;
}

function formatCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11) return cpf;
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

function formatCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    if (cnpj.length !== 14) return cnpj;
    return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}

function formatPhone(phone) {
    phone = phone.replace(/\D/g, '');
    if (phone.length === 11) {
        return phone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (phone.length === 10) {
        return phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    return phone;
}

// Auto-formatação em inputs
function setupCPFInput(input) {
    input.addEventListener('input', (e) => {
        e.target.value = formatCPF(e.target.value);
    });
    
    input.addEventListener('blur', (e) => {
        if (e.target.value && !validateCPF(e.target.value)) {
            e.target.setCustomValidity('CPF inválido');
        } else {
            e.target.setCustomValidity('');
        }
    });
}

function setupCNPJInput(input) {
    input.addEventListener('input', (e) => {
        e.target.value = formatCNPJ(e.target.value);
    });
    
    input.addEventListener('blur', (e) => {
        if (e.target.value && !validateCNPJ(e.target.value)) {
            e.target.setCustomValidity('CNPJ inválido');
        } else {
            e.target.setCustomValidity('');
        }
    });
}

function setupPhoneInput(input) {
    input.addEventListener('input', (e) => {
        e.target.value = formatPhone(e.target.value);
    });
}

// Export para uso global
window.validateCPF = validateCPF;
window.validateCNPJ = validateCNPJ;
window.formatCPF = formatCPF;
window.formatCNPJ = formatCNPJ;
window.formatPhone = formatPhone;
window.setupCPFInput = setupCPFInput;
window.setupCNPJInput = setupCNPJInput;
window.setupPhoneInput = setupPhoneInput;

