/**
 * Slider Component JavaScript
 */
(function() {
    const Slider = {
        init() {
            document.querySelectorAll('[data-slider]').forEach(slider => {
                const input = slider.querySelector('input[type="range"]');
                const range = slider.querySelector('[data-slider-range]');
                const thumb = slider.querySelector('[data-slider-thumb]');
                
                if (!input) return;
                
                input.addEventListener('input', () => {
                    this.update(input, range, thumb);
                });
                
                // Inicializar posição
                this.update(input, range, thumb);
            });
        },
        
        update(input, range, thumb) {
            const min = parseFloat(input.min) || 0;
            const max = parseFloat(input.max) || 100;
            const value = parseFloat(input.value) || 0;
            
            const percentage = ((value - min) / (max - min)) * 100;
            
            if (range) {
                range.style.width = percentage + '%';
            }
            
            if (thumb) {
                thumb.style.left = percentage + '%';
            }
        }
    };
    
    UI.components.register('slider', Slider);
})();

