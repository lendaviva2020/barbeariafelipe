/**
 * Switch Component JavaScript
 */
(function() {
    const Switch = {
        init() {
            // Switches são inicializados via onclick inline
        },
        
        toggle(switchEl) {
            const currentState = switchEl.dataset.state;
            const newState = currentState === 'checked' ? 'unchecked' : 'checked';
            const name = switchEl.dataset.switchName;
            
            // Atualizar UI
            switchEl.dataset.state = newState;
            switchEl.setAttribute('aria-checked', newState === 'checked' ? 'true' : 'false');
            
            // Atualizar input hidden
            const hiddenInput = document.querySelector(`[data-switch-input="${name}"]`);
            if (hiddenInput) {
                hiddenInput.value = newState === 'checked' ? 'on' : 'off';
            }
            
            // Emitir evento
            UI.events.emit('switch:changed', {
                name: name,
                checked: newState === 'checked'
            });
        }
    };
    
    UI.components.register('switch', Switch);
})();

