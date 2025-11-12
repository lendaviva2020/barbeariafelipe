/**
 * Product Selection Dialog Component
 * Seleção de produtos usados no atendimento com validação de estoque
 */

class ProductSelectionDialog {
    constructor(dialogId = 'product-selection-dialog') {
        this.dialog = document.getElementById(dialogId);
        
        if (!this.dialog) {
            console.warn('Product selection dialog not found');
            return;
        }
        
        this.productsList = this.dialog.querySelector('#products-list');
        this.confirmBtn = this.dialog.querySelector('#confirm-products-btn');
        this.summary = this.dialog.querySelector('#product-summary');
        this.totalProducts = this.dialog.querySelector('#total-products');
        
        this.appointmentId = null;
        this.products = [];
        this.selectedProducts = {};
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Close buttons
        const closeBtns = this.dialog.querySelectorAll('[data-close-product-dialog]');
        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => this.close());
        });
        
        // Confirm button
        if (this.confirmBtn) {
            this.confirmBtn.addEventListener('click', () => {
                this.handleConfirm();
            });
        }
    }
    
    async open(appointmentId) {
        this.appointmentId = appointmentId;
        this.selectedProducts = {};
        this.dialog.showModal();
        await this.loadProducts();
    }
    
    close() {
        this.dialog.close();
        this.selectedProducts = {};
    }
    
    async loadProducts() {
        if (this.productsList) {
            this.productsList.innerHTML = `
                <div class="products-loading">
                    <div class="spinner"></div>
                    <p>Carregando produtos...</p>
                </div>
            `;
        }
        
        try {
            const response = await fetch('/api/products/?active=true', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Erro ao carregar produtos');
            }
            
            const data = await response.json();
            this.products = data.results || data;
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
            if (this.productsList) {
                this.productsList.innerHTML = `
                    <div class="products-error">
                        <p>Erro ao carregar produtos</p>
                    </div>
                `;
            }
        }
    }
    
    renderProducts() {
        if (!this.productsList) return;
        
        this.productsList.innerHTML = '';
        
        if (this.products.length === 0) {
            this.productsList.innerHTML = `
                <div class="products-empty">
                    <p>Nenhum produto disponível no estoque</p>
                </div>
            `;
            return;
        }
        
        this.products.forEach(product => {
            const item = this.createProductItem(product);
            this.productsList.appendChild(item);
        });
    }
    
    createProductItem(product) {
        const template = document.getElementById('product-item-template');
        const clone = template.content.cloneNode(true);
        
        const item = clone.querySelector('.product-item');
        const checkbox = clone.querySelector('.product-check');
        const quantityContainer = clone.querySelector('.product-quantity');
        const quantityInput = clone.querySelector('.quantity-input');
        
        // Preencher informações
        clone.querySelector('.product-name').textContent = product.name;
        clone.querySelector('.product-stock').textContent = `Estoque: ${product.quantity} ${product.category || 'unidades'}`;
        
        // Configurar quantity input
        if (quantityInput) {
            quantityInput.max = product.quantity;
        }
        
        // Checkbox change
        if (checkbox) {
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.selectedProducts[product.id] = {
                        ...product,
                        selected_quantity: 1
                    };
                    if (quantityContainer) {
                        quantityContainer.classList.remove('hidden');
                    }
                } else {
                    delete this.selectedProducts[product.id];
                    if (quantityContainer) {
                        quantityContainer.classList.add('hidden');
                    }
                }
                this.updateSummary();
            });
        }
        
        // Quantity change
        if (quantityInput) {
            quantityInput.addEventListener('change', (e) => {
                const qty = parseInt(e.target.value) || 1;
                
                // Validar quantidade
                if (qty > product.quantity) {
                    if (window.toast) {
                        window.toast.show(`Estoque disponível: ${product.quantity}`, 'warning');
                    }
                    e.target.value = product.quantity;
                    this.selectedProducts[product.id].selected_quantity = product.quantity;
                } else if (qty < 1) {
                    e.target.value = 1;
                    this.selectedProducts[product.id].selected_quantity = 1;
                } else {
                    this.selectedProducts[product.id].selected_quantity = qty;
                }
                
                this.updateSummary();
            });
        }
        
        return clone;
    }
    
    updateSummary() {
        const count = Object.keys(this.selectedProducts).length;
        
        if (count > 0) {
            if (this.summary) {
                this.summary.classList.remove('hidden');
            }
            if (this.totalProducts) {
                this.totalProducts.textContent = count;
            }
            if (this.confirmBtn) {
                this.confirmBtn.disabled = false;
            }
        } else {
            if (this.summary) {
                this.summary.classList.add('hidden');
            }
            if (this.confirmBtn) {
                this.confirmBtn.disabled = true;
            }
        }
    }
    
    async handleConfirm() {
        if (Object.keys(this.selectedProducts).length === 0) {
            this.close();
            return;
        }
        
        // Preparar dados
        const productData = Object.values(this.selectedProducts).map(p => ({
            product_id: p.id,
            quantity: p.selected_quantity
        }));
        
        // Desabilitar botão
        if (this.confirmBtn) {
            this.confirmBtn.disabled = true;
            this.confirmBtn.textContent = 'Registrando...';
        }
        
        try {
            const response = await fetch(`/api/appointments/${this.appointmentId}/register-products/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCsrfToken()
                },
                credentials: 'include',
                body: JSON.stringify({ products: productData })
            });
            
            if (!response.ok) {
                throw new Error('Erro ao registrar produtos');
            }
            
            const data = await response.json();
            
            if (window.toast) {
                window.toast.show('Produtos registrados com sucesso!', 'success');
            } else {
                alert('Produtos registrados com sucesso!');
            }
            
            this.close();
            
            // Callback se houver
            if (this.onSuccess && typeof this.onSuccess === 'function') {
                this.onSuccess(data);
            }
            
        } catch (error) {
            console.error('Error registering products:', error);
            if (window.toast) {
                window.toast.show('Erro ao registrar produtos', 'error');
            } else {
                alert('Erro ao registrar produtos');
            }
        } finally {
            if (this.confirmBtn) {
                this.confirmBtn.disabled = false;
                this.confirmBtn.textContent = 'Confirmar Seleção';
            }
        }
    }
    
    getCsrfToken() {
        const name = 'csrftoken';
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
}

// Inicializar
let productSelectionDialog;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        productSelectionDialog = new ProductSelectionDialog();
        window.productSelectionDialog = productSelectionDialog;
    });
} else {
    productSelectionDialog = new ProductSelectionDialog();
    window.productSelectionDialog = productSelectionDialog;
}

// Função helper para abrir dialog
function openProductSelection(appointmentId) {
    if (window.productSelectionDialog) {
        window.productSelectionDialog.open(appointmentId);
    }
}

