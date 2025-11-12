/**
 * Tabs Component JavaScript
 */
(function() {
    const Tabs = {
        init() {
            document.querySelectorAll('[data-tabs]').forEach(tabs => {
                const triggers = tabs.querySelectorAll('[data-tabs-trigger]');
                
                triggers.forEach(trigger => {
                    trigger.addEventListener('click', () => {
                        this.switchTab(trigger, tabs);
                    });
                });
            });
        },
        
        switchTab(trigger, container) {
            const tabId = trigger.dataset.tabsTrigger;
            
            // Atualizar triggers
            container.querySelectorAll('[data-tabs-trigger]').forEach(t => {
                t.dataset.state = 'inactive';
                t.setAttribute('aria-selected', 'false');
            });
            
            trigger.dataset.state = 'active';
            trigger.setAttribute('aria-selected', 'true');
            
            // Atualizar contents
            container.querySelectorAll('[data-tabs-content]').forEach(content => {
                content.classList.add('hidden');
            });
            
            const activeContent = container.querySelector(`[data-tabs-content="${tabId}"]`);
            if (activeContent) {
                activeContent.classList.remove('hidden');
            }
        }
    };
    
    UI.components.register('tabs', Tabs);
})();

