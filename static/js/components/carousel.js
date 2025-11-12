/**
 * Carousel Component JavaScript
 */
(function() {
    const Carousel = {
        carousels: new Map(),
        
        init() {
            document.querySelectorAll('[data-carousel]').forEach(carousel => {
                this.setup(carousel);
            });
        },
        
        setup(carousel) {
            const container = carousel.querySelector('[data-carousel-container]');
            const items = carousel.querySelectorAll('[data-carousel-item]');
            const prevBtn = carousel.querySelector('[data-carousel-prev]');
            const nextBtn = carousel.querySelector('[data-carousel-next]');
            const indicators = carousel.querySelectorAll('[data-carousel-indicator]');
            
            const state = {
                currentIndex: 0,
                totalItems: items.length,
                autoPlay: carousel.dataset.autoPlay === 'true',
                interval: parseInt(carousel.dataset.interval) || 5000,
                timer: null
            };
            
            this.carousels.set(carousel, state);
            
            // Event listeners
            if (prevBtn) {
                prevBtn.addEventListener('click', () => this.prev(carousel));
            }
            
            if (nextBtn) {
                nextBtn.addEventListener('click', () => this.next(carousel));
            }
            
            indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', () => this.goTo(carousel, index));
            });
            
            // Auto play
            if (state.autoPlay) {
                this.startAutoPlay(carousel);
                
                // Pausar no hover
                carousel.addEventListener('mouseenter', () => this.stopAutoPlay(carousel));
                carousel.addEventListener('mouseleave', () => this.startAutoPlay(carousel));
            }
            
            // Inicializar posição
            this.updatePosition(carousel);
        },
        
        next(carousel) {
            const state = this.carousels.get(carousel);
            state.currentIndex = (state.currentIndex + 1) % state.totalItems;
            this.updatePosition(carousel);
        },
        
        prev(carousel) {
            const state = this.carousels.get(carousel);
            state.currentIndex = (state.currentIndex - 1 + state.totalItems) % state.totalItems;
            this.updatePosition(carousel);
        },
        
        goTo(carousel, index) {
            const state = this.carousels.get(carousel);
            state.currentIndex = index;
            this.updatePosition(carousel);
        },
        
        updatePosition(carousel) {
            const state = this.carousels.get(carousel);
            const container = carousel.querySelector('[data-carousel-container]');
            const indicators = carousel.querySelectorAll('[data-carousel-indicator]');
            
            // Mover container
            container.style.transform = `translateX(-${state.currentIndex * 100}%)`;
            
            // Atualizar indicators
            indicators.forEach((indicator, index) => {
                if (index === state.currentIndex) {
                    indicator.classList.remove('bg-white/50');
                    indicator.classList.add('bg-white');
                } else {
                    indicator.classList.remove('bg-white');
                    indicator.classList.add('bg-white/50');
                }
            });
        },
        
        startAutoPlay(carousel) {
            const state = this.carousels.get(carousel);
            if (state.timer) clearInterval(state.timer);
            
            state.timer = setInterval(() => {
                this.next(carousel);
            }, state.interval);
        },
        
        stopAutoPlay(carousel) {
            const state = this.carousels.get(carousel);
            if (state.timer) {
                clearInterval(state.timer);
                state.timer = null;
            }
        }
    };
    
    UI.components.register('carousel', Carousel);
})();

