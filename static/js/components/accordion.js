/**
 * Accordion Component JavaScript
 */
(function() {
    const Accordion = {
        init() {
            document.querySelectorAll('[data-accordion]').forEach(accordion => {
                const allowMultiple = accordion.dataset.accordion === 'multiple';
                
                accordion.querySelectorAll('[data-accordion-trigger]').forEach(trigger => {
                    trigger.addEventListener('click', () => {
                        this.toggle(trigger, accordion, allowMultiple);
                    });
                });
            });
        },
        
        toggle(trigger, accordion, allowMultiple) {
            const index = trigger.dataset.accordionTrigger;
            const content = accordion.querySelector(`[data-accordion-content="${index}"]`);
            const isOpen = trigger.dataset.state === 'open';
            
            if (!allowMultiple) {
                // Fechar todos os outros
                accordion.querySelectorAll('[data-accordion-trigger]').forEach(otherTrigger => {
                    if (otherTrigger !== trigger && otherTrigger.dataset.state === 'open') {
                        const otherIndex = otherTrigger.dataset.accordionTrigger;
                        const otherContent = accordion.querySelector(`[data-accordion-content="${otherIndex}"]`);
                        this.close(otherTrigger, otherContent);
                    }
                });
            }
            
            if (isOpen) {
                this.close(trigger, content);
            } else {
                this.open(trigger, content);
            }
        },
        
        open(trigger, content) {
            trigger.dataset.state = 'open';
            trigger.setAttribute('aria-expanded', 'true');
            content.dataset.state = 'open';
            UI.animate.slideDown(content);
        },
        
        close(trigger, content) {
            trigger.dataset.state = 'closed';
            trigger.setAttribute('aria-expanded', 'false');
            content.dataset.state = 'closed';
            UI.animate.slideUp(content);
        }
    };
    
    UI.components.register('accordion', Accordion);
})();

