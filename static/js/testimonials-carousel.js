/**
 * Testimonials Carousel Component
 * Carrossel de depoimentos com auto-play, navegação por teclado e touch
 */

class TestimonialsCarousel {
    constructor(element) {
        this.element = element;
        
        if (!this.element) {
            console.warn('Testimonials carousel element not found');
            return;
        }
        
        this.slides = this.element.querySelectorAll('[data-slide]');
        this.prevBtn = this.element.querySelector('[data-carousel-prev]');
        this.nextBtn = this.element.querySelector('[data-carousel-next]');
        this.dotsContainer = this.element.querySelector('[data-carousel-dots]');
        this.toggleBtn = this.element.querySelector('[data-carousel-toggle]');
        
        this.currentIndex = 0;
        this.totalSlides = this.slides.length;
        this.isAutoPlaying = true;
        this.isPaused = false;
        this.autoPlayInterval = null;
        this.autoPlayDelay = 5000; // 5 segundos
        
        this.touchStartX = 0;
        this.touchEndX = 0;
        
        if (this.totalSlides > 0) {
            this.init();
        }
    }
    
    init() {
        this.setupDots();
        this.setupNavigation();
        this.setupKeyboard();
        this.setupTouch();
        this.setupAutoPlay();
        this.goToSlide(0);
    }
    
    setupDots() {
        if (!this.dotsContainer) return;
        
        this.dotsContainer.innerHTML = '';
        
        for (let i = 0; i < this.totalSlides; i++) {
            const dot = document.createElement('button');
            dot.className = 'carousel-dot';
            dot.setAttribute('aria-label', `Ir para depoimento ${i + 1}`);
            dot.addEventListener('click', () => this.goToSlide(i));
            this.dotsContainer.appendChild(dot);
        }
    }
    
    setupNavigation() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.previous());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggleAutoPlay());
        }
    }
    
    setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            // Apenas se o carrossel estiver visível
            if (!this.isInViewport()) return;
            
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                this.previous();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                this.next();
            }
        });
    }
    
    setupTouch() {
        this.element.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        this.element.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
        }, { passive: true });
        
        // Pausar auto-play ao tocar
        this.element.addEventListener('touchstart', () => {
            this.pause();
        }, { passive: true });
        
        this.element.addEventListener('touchend', () => {
            this.resume();
        }, { passive: true });
    }
    
    setupAutoPlay() {
        // Pausar ao hover
        this.element.addEventListener('mouseenter', () => this.pause());
        this.element.addEventListener('mouseleave', () => this.resume());
        
        // Iniciar auto-play
        this.startAutoPlay();
    }
    
    handleSwipe() {
        const swipeThreshold = 50;
        const diff = this.touchStartX - this.touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                this.next(); // Swipe left - próximo
            } else {
                this.previous(); // Swipe right - anterior
            }
        }
    }
    
    next() {
        this.goToSlide((this.currentIndex + 1) % this.totalSlides);
    }
    
    previous() {
        this.goToSlide((this.currentIndex - 1 + this.totalSlides) % this.totalSlides);
    }
    
    goToSlide(index) {
        if (index < 0 || index >= this.totalSlides) return;
        
        // Remover active de todos
        this.slides.forEach((slide) => {
            slide.classList.remove('active');
            slide.setAttribute('aria-hidden', 'true');
        });
        
        // Adicionar active ao atual
        this.slides[index].classList.add('active');
        this.slides[index].setAttribute('aria-hidden', 'false');
        
        // Atualizar dots
        if (this.dotsContainer) {
            const dots = this.dotsContainer.querySelectorAll('.carousel-dot');
            dots.forEach((dot, i) => {
                if (i === index) {
                    dot.classList.add('active');
                    dot.setAttribute('aria-current', 'true');
                } else {
                    dot.classList.remove('active');
                    dot.setAttribute('aria-current', 'false');
                }
            });
        }
        
        this.currentIndex = index;
        
        // Anunciar para leitores de tela
        this.announceSlide(index);
    }
    
    startAutoPlay() {
        if (!this.isAutoPlaying) return;
        
        this.stopAutoPlay(); // Limpar interval anterior
        
        this.autoPlayInterval = setInterval(() => {
            if (!this.isPaused) {
                this.next();
            }
        }, this.autoPlayDelay);
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    pause() {
        this.isPaused = true;
    }
    
    resume() {
        this.isPaused = false;
    }
    
    toggleAutoPlay() {
        this.isAutoPlaying = !this.isAutoPlaying;
        
        if (this.isAutoPlaying) {
            this.startAutoPlay();
            if (this.toggleBtn) {
                this.toggleBtn.textContent = '⏸ Pausar rotação automática';
            }
        } else {
            this.stopAutoPlay();
            if (this.toggleBtn) {
                this.toggleBtn.textContent = '▶ Ativar rotação automática';
            }
        }
    }
    
    isInViewport() {
        const rect = this.element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
    
    announceSlide(index) {
        const announcer = document.getElementById('carousel-announcer');
        if (announcer) {
            announcer.textContent = `Depoimento ${index + 1} de ${this.totalSlides}`;
        }
    }
    
    destroy() {
        this.stopAutoPlay();
    }
}

// Inicializar todos os carrosséis na página
function initTestimonialsCarousels() {
    const carousels = document.querySelectorAll('[data-testimonials-carousel]');
    const instances = [];
    
    carousels.forEach((carousel) => {
        instances.push(new TestimonialsCarousel(carousel));
    });
    
    // Cleanup ao descarregar
    window.addEventListener('beforeunload', () => {
        instances.forEach(instance => instance.destroy());
    });
}

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTestimonialsCarousels);
} else {
    initTestimonialsCarousels();
}

