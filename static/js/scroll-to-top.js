/**
 * Scroll to Top Component
 * Botão que aparece após scroll > 300px e volta ao topo suavemente
 */

class ScrollToTop {
    constructor() {
        this.btn = document.getElementById('scroll-to-top');
        
        if (!this.btn) {
            console.warn('Scroll to top button not found');
            return;
        }
        
        this.scrollThreshold = 300;
        this.isVisible = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.checkScroll(); // Verificar posição inicial
    }
    
    setupEventListeners() {
        // Listener de scroll
        window.addEventListener('scroll', () => {
            this.checkScroll();
        }, { passive: true });
        
        // Click no botão
        this.btn.addEventListener('click', () => {
            this.scrollToTop();
        });
    }
    
    checkScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollY > this.scrollThreshold) {
            this.show();
        } else {
            this.hide();
        }
    }
    
    show() {
        if (!this.isVisible) {
            this.btn.classList.remove('hidden');
            this.btn.classList.add('visible');
            this.isVisible = true;
        }
    }
    
    hide() {
        if (this.isVisible) {
            this.btn.classList.remove('visible');
            // Aguardar animação antes de esconder
            setTimeout(() => {
                if (!this.isVisible) {
                    this.btn.classList.add('hidden');
                }
            }, 300);
            this.isVisible = false;
        }
    }
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.scrollToTop = new ScrollToTop();
    });
} else {
    window.scrollToTop = new ScrollToTop();
}

