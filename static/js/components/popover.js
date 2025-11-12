/**
 * Popover Component JavaScript
 */
(function() {
    const Popover = {
        init() {
            document.querySelectorAll('[data-popover-trigger]').forEach(trigger => {
                const popoverId = trigger.dataset.popoverTrigger;
                const popover = document.getElementById(popoverId);
                
                if (!popover) return;
                
                trigger.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.toggle(trigger, popover);
                });
                
                // Fechar ao clicar fora
                document.addEventListener('click', (e) => {
                    if (!popover.contains(e.target) && !trigger.contains(e.target)) {
                        this.close(popover);
                    }
                });
            });
        },
        
        toggle(trigger, popover) {
            const isOpen = popover.dataset.state === 'open';
            
            if (isOpen) {
                this.close(popover);
            } else {
                this.open(trigger, popover);
            }
        },
        
        open(trigger, popover) {
            popover.dataset.state = 'open';
            popover.classList.remove('hidden');
            
            // Posicionar próximo ao trigger
            const triggerRect = trigger.getBoundingClientRect();
            popover.style.position = 'absolute';
            popover.style.top = (triggerRect.bottom + 8) + 'px';
            popover.style.left = triggerRect.left + 'px';
        },
        
        close(popover) {
            popover.dataset.state = 'closed';
            setTimeout(() => {
                popover.classList.add('hidden');
            }, 200);
        }
    };
    
    UI.components.register('popover', Popover);
})();

