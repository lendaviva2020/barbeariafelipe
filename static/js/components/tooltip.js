/**
 * Tooltip Component JavaScript
 */
(function() {
    const Tooltip = {
        init() {
            document.querySelectorAll('[data-tooltip]').forEach(tooltipEl => {
                const tooltipId = tooltipEl.id;
                const triggers = document.querySelectorAll(`[data-tooltip="${tooltipId}"]`);
                
                triggers.forEach(trigger => {
                    trigger.addEventListener('mouseenter', () => {
                        this.show(trigger, tooltipEl);
                    });
                    
                    trigger.addEventListener('mouseleave', () => {
                        this.hide(tooltipEl);
                    });
                    
                    trigger.addEventListener('focus', () => {
                        this.show(trigger, tooltipEl);
                    });
                    
                    trigger.addEventListener('blur', () => {
                        this.hide(tooltipEl);
                    });
                });
            });
        },
        
        show(trigger, tooltip) {
            tooltip.dataset.state = 'visible';
            tooltip.classList.remove('hidden');
            
            // Posicionar
            const triggerRect = trigger.getBoundingClientRect();
            tooltip.style.position = 'fixed';
            tooltip.style.top = (triggerRect.top - tooltip.offsetHeight - 8) + 'px';
            tooltip.style.left = (triggerRect.left + (triggerRect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
        },
        
        hide(tooltip) {
            tooltip.dataset.state = 'hidden';
            setTimeout(() => {
                tooltip.classList.add('hidden');
            }, 200);
        }
    };
    
    UI.components.register('tooltip', Tooltip);
})();

