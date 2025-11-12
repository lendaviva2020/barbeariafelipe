/**
 * Dropdown Menu Component JavaScript
 */
(function() {
    const Dropdown = {
        init() {
            document.querySelectorAll('[data-dropdown]').forEach(dropdown => {
                const trigger = dropdown.querySelector('[data-dropdown-trigger]');
                const menu = dropdown.querySelector('[data-dropdown-menu]');
                
                if (!trigger || !menu) return;
                
                trigger.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.toggle(dropdown, trigger, menu);
                });
                
                // Fechar ao clicar fora
                document.addEventListener('click', (e) => {
                    if (!dropdown.contains(e.target) && menu.dataset.state === 'open') {
                        this.close(trigger, menu);
                    }
                });
            });
        },
        
        toggle(dropdown, trigger, menu) {
            const isOpen = menu.dataset.state === 'open';
            
            if (isOpen) {
                this.close(trigger, menu);
            } else {
                this.open(trigger, menu);
            }
        },
        
        open(trigger, menu) {
            menu.dataset.state = 'open';
            trigger.setAttribute('aria-expanded', 'true');
            menu.classList.remove('hidden');
            UI.classList.add(menu, 'animate-fade-in', 'animate-zoom-in');
        },
        
        close(trigger, menu) {
            menu.dataset.state = 'closed';
            trigger.setAttribute('aria-expanded', 'false');
            UI.classList.remove(menu, 'animate-fade-in', 'animate-zoom-in');
            
            setTimeout(() => {
                menu.classList.add('hidden');
            }, 200);
        }
    };
    
    UI.components.register('dropdown', Dropdown);
})();

