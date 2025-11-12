/**
 * Command Palette Component JavaScript
 */
(function() {
    const Command = {
        init() {
            document.querySelectorAll('[data-command]').forEach(command => {
                const input = command.querySelector('[data-command-input]');
                const items = command.querySelectorAll('[data-command-item]');
                
                if (!input) return;
                
                input.addEventListener('input', () => {
                    this.filter(input, items);
                });
                
                // Navegação com teclado
                input.addEventListener('keydown', (e) => {
                    this.handleKeyboard(e, command, items);
                });
                
                // Selecionar item ao clicar
                items.forEach((item, index) => {
                    item.addEventListener('click', () => {
                        this.selectItem(item, input);
                    });
                    
                    item.dataset.index = index;
                });
            });
        },
        
        filter(input, items) {
            const query = input.value.toLowerCase();
            let visibleCount = 0;
            
            items.forEach(item => {
                const value = item.dataset.value.toLowerCase();
                const matches = value.includes(query);
                
                if (matches) {
                    item.classList.remove('hidden');
                    visibleCount++;
                } else {
                    item.classList.add('hidden');
                }
            });
            
            // Mostrar mensagem "sem resultados" se necessário
            const list = input.closest('[data-command]').querySelector('[data-command-list]');
            let emptyMsg = list.querySelector('[data-command-empty]');
            
            if (visibleCount === 0) {
                if (!emptyMsg) {
                    emptyMsg = UI.dom.create('div', {
                        class: 'py-6 text-center text-sm',
                        'data-command-empty': ''
                    }, ['Nenhum resultado encontrado']);
                    list.appendChild(emptyMsg);
                }
            } else if (emptyMsg) {
                UI.dom.remove(emptyMsg);
            }
        },
        
        handleKeyboard(e, command, items) {
            const visibleItems = Array.from(items).filter(item => !item.classList.contains('hidden'));
            const selectedItem = command.querySelector('[data-command-item][data-selected="true"]');
            const currentIndex = selectedItem ? parseInt(selectedItem.dataset.index) : -1;
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const nextIndex = Math.min(currentIndex + 1, visibleItems.length - 1);
                this.highlightItem(visibleItems[nextIndex], visibleItems);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prevIndex = Math.max(currentIndex - 1, 0);
                this.highlightItem(visibleItems[prevIndex], visibleItems);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (selectedItem) {
                    selectedItem.click();
                }
            }
        },
        
        highlightItem(item, allItems) {
            allItems.forEach(i => {
                i.dataset.selected = 'false';
                i.classList.remove('bg-accent', 'text-accent-foreground');
            });
            
            if (item) {
                item.dataset.selected = 'true';
                item.classList.add('bg-accent', 'text-accent-foreground');
                item.scrollIntoView({ block: 'nearest' });
            }
        },
        
        selectItem(item, input) {
            const value = item.dataset.value;
            input.value = value;
            UI.events.emit('command:selected', { value });
        }
    };
    
    UI.components.register('command', Command);
})();

