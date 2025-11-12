/**
 * Form Validations
 * Validações em tempo real para formulários (similar ao React)
 * Integrado com sistema de toast para feedback
 */

const FormValidations = {
    /**
     * Validadores disponíveis
     */
    validators: {
        required: {
            validate: (value) => {
                return value && value.toString().trim().length > 0;
            },
            message: 'Este campo é obrigatório'
        },
        
        email: {
            validate: (value) => {
                if (!value) return true; // Apenas validar se preenchido
                const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return regex.test(value);
            },
            message: 'Email inválido'
        },
        
        phone: {
            validate: (value) => {
                if (!value) return true;
                const clean = value.replace(/\D/g, '');
                return clean.length >= 10 && clean.length <= 13;
            },
            message: 'Telefone inválido. Use o formato (XX) XXXXX-XXXX'
        },
        
        minLength: {
            validate: (value, min = 3) => {
                if (!value) return true;
                return value.toString().length >= min;
            },
            message: (min) => `Mínimo de ${min} caracteres`
        },
        
        maxLength: {
            validate: (value, max = 255) => {
                if (!value) return true;
                return value.toString().length <= max;
            },
            message: (max) => `Máximo de ${max} caracteres`
        },
        
        minValue: {
            validate: (value, min = 0) => {
                if (!value) return true;
                return parseFloat(value) >= min;
            },
            message: (min) => `Valor mínimo: ${min}`
        },
        
        maxValue: {
            validate: (value, max = 999999) => {
                if (!value) return true;
                return parseFloat(value) <= max;
            },
            message: (max) => `Valor máximo: ${max}`
        },
        
        numeric: {
            validate: (value) => {
                if (!value) return true;
                return !isNaN(parseFloat(value)) && isFinite(value);
            },
            message: 'Apenas números são permitidos'
        },
        
        lettersOnly: {
            validate: (value) => {
                if (!value) return true;
                const regex = /^[a-zA-ZÀ-ÿ\s]+$/;
                return regex.test(value);
            },
            message: 'Apenas letras são permitidas'
        },
        
        passwordStrength: {
            validate: (value) => {
                if (!value) return true;
                return value.length >= 6;
            },
            message: 'A senha deve ter pelo menos 6 caracteres'
        },
        
        passwordMatch: {
            validate: (value, compareValue) => {
                return value === compareValue;
            },
            message: 'As senhas não conferem'
        }
    },
    
    /**
     * Aplica validação em um input
     * @param {HTMLElement} input - Input element
     * @param {string|Array} validatorNames - Nome(s) do(s) validador(es)
     * @param {object} options - Opções adicionais
     */
    attachValidation(input, validatorNames, options = {}) {
        if (!input) return;
        
        const validators = Array.isArray(validatorNames) ? validatorNames : [validatorNames];
        
        // Criar container de erro se não existir
        let errorEl = input.nextElementSibling;
        if (!errorEl || !errorEl.classList.contains('field-error')) {
            errorEl = document.createElement('p');
            errorEl.className = 'field-error';
            errorEl.style.display = 'none';
            input.parentNode.insertBefore(errorEl, input.nextSibling);
        }
        
        // Função de validação
        const validate = () => {
            const value = input.value;
            let isValid = true;
            let errorMessage = '';
            
            for (const validatorName of validators) {
                const validator = this.validators[validatorName];
                
                if (!validator) continue;
                
                const result = typeof validator.validate === 'function'
                    ? validator.validate(value, options[validatorName])
                    : false;
                
                if (!result) {
                    isValid = false;
                    errorMessage = typeof validator.message === 'function'
                        ? validator.message(options[validatorName])
                        : validator.message;
                    break;
                }
            }
            
            // Atualizar UI
            if (isValid) {
                input.classList.remove('error');
                input.classList.add('valid');
                errorEl.style.display = 'none';
                errorEl.textContent = '';
            } else {
                input.classList.remove('valid');
                input.classList.add('error');
                errorEl.style.display = 'block';
                errorEl.textContent = errorMessage;
            }
            
            return isValid;
        };
        
        // Eventos
        input.addEventListener('blur', validate);
        
        // Validação em tempo real se configurado
        if (options.realtime) {
            let timeout;
            input.addEventListener('input', () => {
                clearTimeout(timeout);
                timeout = setTimeout(validate, 500);
            });
        }
        
        // Retornar função de validação para uso manual
        return validate;
    },
    
    /**
     * Valida um formulário inteiro
     * @param {HTMLFormElement} form - Formulário
     * @returns {boolean} - True se válido
     */
    validateForm(form) {
        if (!form) return false;
        
        const inputs = form.querySelectorAll('[data-validate]');
        let isValid = true;
        
        inputs.forEach(input => {
            const validators = input.dataset.validate.split(',');
            const options = this.parseOptions(input.dataset.validateOptions);
            
            const validateFn = this.attachValidation(input, validators, options);
            
            if (validateFn && !validateFn()) {
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    /**
     * Inicializa validação automática em formulário
     * @param {HTMLFormElement|string} formOrSelector - Formulário ou seletor
     */
    initForm(formOrSelector) {
        const form = typeof formOrSelector === 'string'
            ? document.querySelector(formOrSelector)
            : formOrSelector;
        
        if (!form) return;
        
        // Aplicar validação em todos os inputs com data-validate
        const inputs = form.querySelectorAll('[data-validate]');
        
        inputs.forEach(input => {
            const validators = input.dataset.validate.split(',').map(v => v.trim());
            const options = this.parseOptions(input.dataset.validateOptions);
            
            this.attachValidation(input, validators, options);
        });
        
        // Validar ao submeter
        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
                
                if (window.toast) {
                    window.toast.warning('Por favor, corrija os erros no formulário');
                }
                
                // Focar no primeiro campo com erro
                const firstError = form.querySelector('.error');
                if (firstError) {
                    firstError.focus();
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    },
    
    /**
     * Parse de opções do data attribute
     */
    parseOptions(optionsString) {
        if (!optionsString) return {};
        
        try {
            return JSON.parse(optionsString);
        } catch (e) {
            console.warn('Invalid validation options:', optionsString);
            return {};
        }
    },
    
    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// CSS inline para erros de validação
const validationStyles = document.createElement('style');
validationStyles.textContent = `
.field-error {
    font-size: 0.813rem;
    color: hsl(var(--destructive));
    margin-top: 6px;
    animation: errorShake 0.3s ease;
}

@keyframes errorShake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-4px); }
    75% { transform: translateX(4px); }
}

input.error,
textarea.error,
select.error {
    border-color: hsl(var(--destructive)) !important;
    box-shadow: 0 0 0 3px hsl(var(--destructive) / 0.1) !important;
}

input.valid,
textarea.valid,
select.valid {
    border-color: #10b981 !important;
}
`;
document.head.appendChild(validationStyles);

// Expor globalmente
window.FormValidations = FormValidations;

// Auto-inicializar formulários com data-auto-validate
document.addEventListener('DOMContentLoaded', () => {
    const autoForms = document.querySelectorAll('[data-auto-validate]');
    autoForms.forEach(form => {
        FormValidations.initForm(form);
    });
});

// Exemplo de uso no HTML:
// <form data-auto-validate>
//     <input 
//         type="email" 
//         name="email" 
//         data-validate="required,email"
//         placeholder="seu@email.com"
//     >
//     <input 
//         type="password" 
//         name="password" 
//         data-validate="required,passwordStrength"
//         data-validate-options='{"minLength": 8}'
//     >
//     <button type="submit">Enviar</button>
// </form>

