/**
 * Dialog Component JavaScript
 */
(function() {
    const Dialog = {
        init() {
            // Registrar helper global para abrir dialogs
            window.openDialog = (id) => this.open(id);
            window.closeDialog = (id) => this.close(id);
        },
        
        open(id) {
            const dialog = document.getElementById(id);
            if (!dialog) return;
            
            UI.overlay.open(dialog);
        },
        
        close(id) {
            const dialog = document.getElementById(id);
            if (!dialog) return;
            
            UI.overlay.close(dialog);
        }
    };
    
    UI.components.register('dialog', Dialog);
})();

