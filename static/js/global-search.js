/**
 * Global Search Component
 * Busca global ativada por Cmd/Ctrl+K
 * Busca em tempo real em agendamentos, clientes, serviços e produtos
 */

class GlobalSearch {
    constructor() {
        this.modal = document.getElementById('global-search-modal');
        this.input = document.getElementById('global-search-input');
        this.resultsContainer = document.getElementById('search-results');
        this.isOpen = false;
        this.selectedIndex = -1;
        this.results = [];
        this.searchTimeout = null;
        
        if (!this.modal || !this.input || !this.resultsContainer) {
            console.warn('Global search elements not found');
            return;
        }
        
        this.init();
    }
    
    init() {
        this.setupKeyboardShortcut();
        this.setupEventListeners();
        this.setupCloseHandlers();
    }
    
    setupKeyboardShortcut() {
        document.addEventListener('keydown', (e) => {
            // Cmd+K (Mac) ou Ctrl+K (Windows/Linux)
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                this.toggle();
            }
            
            // ESC para fechar
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }
    
    setupEventListeners() {
        // Input de busca
        this.input.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Navegação por teclado
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.selectNext();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.selectPrevious();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                this.selectCurrent();
            }
        });
    }
    
    setupCloseHandlers() {
        // Fechar ao clicar no overlay
        const overlay = this.modal.querySelector('[data-close-search]');
        if (overlay) {
            overlay.addEventListener('click', () => this.close());
        }
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.modal.classList.remove('hidden');
        this.modal.classList.add('active');
        this.isOpen = true;
        this.input.focus();
        this.input.value = '';
        this.showEmptyState();
        document.body.style.overflow = 'hidden';
    }
    
    close() {
        this.modal.classList.add('hidden');
        this.modal.classList.remove('active');
        this.isOpen = false;
        this.input.value = '';
        this.selectedIndex = -1;
        this.results = [];
        document.body.style.overflow = '';
    }
    
    handleSearch(query) {
        // Debounce - aguardar 300ms após última digitação
        clearTimeout(this.searchTimeout);
        
        if (query.length < 2) {
            this.showEmptyState();
            return;
        }
        
        this.searchTimeout = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }
    
    async performSearch(query) {
        this.showLoading();
        
        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Erro na busca');
            }
            
            const data = await response.json();
            this.results = data.results || [];
            this.displayResults();
        } catch (error) {
            console.error('Search error:', error);
            this.showError();
        }
    }
    
    showLoading() {
        const template = document.getElementById('search-loading-template');
        if (template) {
            const clone = template.content.cloneNode(true);
            this.resultsContainer.innerHTML = '';
            this.resultsContainer.appendChild(clone);
        }
    }
    
    showEmptyState() {
        this.resultsContainer.innerHTML = `
            <div class="search-empty">
                <p>Digite para buscar...</p>
            </div>
        `;
    }
    
    showError() {
        this.resultsContainer.innerHTML = `
            <div class="search-error">
                <p>Erro ao buscar. Tente novamente.</p>
            </div>
        `;
    }
    
    displayResults() {
        if (this.results.length === 0) {
            const template = document.getElementById('search-empty-template');
            if (template) {
                const clone = template.content.cloneNode(true);
                this.resultsContainer.innerHTML = '';
                this.resultsContainer.appendChild(clone);
            }
            return;
        }
        
        // Agrupar por tipo
        const grouped = this.groupByType(this.results);
        
        this.resultsContainer.innerHTML = '';
        
        // Renderizar cada grupo
        Object.entries(grouped).forEach(([type, items]) => {
            const groupEl = this.createGroupElement(type, items);
            this.resultsContainer.appendChild(groupEl);
        });
        
        // Selecionar primeiro resultado
        this.selectedIndex = 0;
        this.updateSelection();
    }
    
    groupByType(results) {
        const groups = {};
        const typeLabels = {
            'appointment': 'Agendamentos',
            'client': 'Clientes',
            'service': 'Serviços',
            'product': 'Produtos'
        };
        
        results.forEach(result => {
            const type = result.type;
            if (!groups[type]) {
                groups[type] = {
                    label: typeLabels[type] || type,
                    items: []
                };
            }
            groups[type].items.push(result);
        });
        
        return groups;
    }
    
    createGroupElement(type, group) {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'search-group';
        
        const heading = document.createElement('div');
        heading.className = 'group-heading';
        heading.textContent = group.label;
        groupDiv.appendChild(heading);
        
        const itemsDiv = document.createElement('div');
        itemsDiv.className = 'group-items';
        
        group.items.forEach((item, index) => {
            const itemEl = this.createResultElement(item, index);
            itemsDiv.appendChild(itemEl);
        });
        
        groupDiv.appendChild(itemsDiv);
        return groupDiv;
    }
    
    createResultElement(result, index) {
        const template = document.getElementById('search-result-template');
        const clone = template.content.cloneNode(true);
        
        const item = clone.querySelector('.search-result-item');
        item.dataset.index = index;
        item.dataset.url = result.url;
        
        // Ícone
        const iconMap = {
            'calendar': 'M8 2v3m8-3v3m-9 8h10M5 6h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2z',
            'user': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
            'scissors': 'M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z',
            'package': 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'
        };
        
        const iconSvg = clone.querySelector('.result-icon svg');
        if (iconSvg && iconMap[result.icon]) {
            iconSvg.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconMap[result.icon]}"/>`;
        }
        
        // Conteúdo
        clone.querySelector('.result-title').textContent = result.title;
        clone.querySelector('.result-subtitle').textContent = result.subtitle;
        
        // Click handler
        item.addEventListener('click', () => {
            window.location.href = result.url;
        });
        
        return clone;
    }
    
    selectNext() {
        if (this.results.length === 0) return;
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.results.length - 1);
        this.updateSelection();
    }
    
    selectPrevious() {
        if (this.results.length === 0) return;
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
        this.updateSelection();
    }
    
    updateSelection() {
        const items = this.resultsContainer.querySelectorAll('.search-result-item');
        items.forEach((item, index) => {
            if (index === this.selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('selected');
            }
        });
    }
    
    selectCurrent() {
        if (this.selectedIndex >= 0 && this.results[this.selectedIndex]) {
            const result = this.results[this.selectedIndex];
            if (result.url) {
                window.location.href = result.url;
            }
        }
    }
}

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.globalSearch = new GlobalSearch();
    });
} else {
    window.globalSearch = new GlobalSearch();
}

