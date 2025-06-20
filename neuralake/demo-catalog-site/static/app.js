
// Neuralake Catalog Interactive JavaScript

class CatalogApp {
    constructor() {
        this.searchIndex = [];
        this.currentFilter = 'all';
        this.init();
    }
    
    async init() {
        await this.loadSearchIndex();
        this.setupEventListeners();
        this.renderTables();
    }
    
    async loadSearchIndex() {
        try {
            const response = await fetch('./search-index.json');
            this.searchIndex = await response.json();
        } catch (error) {
            console.error('Failed to load search index:', error);
        }
    }
    
    setupEventListeners() {
        const searchBox = document.getElementById('searchBox');
        if (searchBox) {
            searchBox.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }
        
        const filterTags = document.querySelectorAll('.filter-tag');
        filterTags.forEach(tag => {
            tag.addEventListener('click', (e) => {
                this.handleFilter(e.target.dataset.filter);
            });
        });
        
        // Copy button functionality
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('copy-button')) {
                this.copyToClipboard(e.target);
            }
        });
    }
    
    handleSearch(query) {
        const filteredTables = this.searchIndex.filter(table => 
            table.name.toLowerCase().includes(query.toLowerCase()) ||
            table.description.toLowerCase().includes(query.toLowerCase()) ||
            table.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
        );
        this.renderFilteredTables(filteredTables);
    }
    
    handleFilter(filter) {
        // Update active filter
        document.querySelectorAll('.filter-tag').forEach(tag => {
            tag.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        
        this.currentFilter = filter;
        
        let filteredTables = this.searchIndex;
        if (filter !== 'all') {
            filteredTables = this.searchIndex.filter(table => 
                table.table_type === filter
            );
        }
        
        this.renderFilteredTables(filteredTables);
    }
    
    renderFilteredTables(tables) {
        const grid = document.getElementById('tableGrid');
        if (!grid) return;
        
        grid.innerHTML = tables.map(table => `
            <div class="table-card" onclick="window.location.href='./tables/${table.name}.html'">
                <div class="table-type">${table.table_type}</div>
                <div class="table-title">${table.name}</div>
                <div class="table-description">${table.description || 'No description available'}</div>
                <div class="tags">
                    ${table.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <div class="table-meta">
                    <span>Columns: ${Object.keys(table.schema || {}).length}</span>
                    <span>Owner: ${table.owner || 'Unknown'}</span>
                </div>
            </div>
        `).join('');
    }
    
    renderTables() {
        this.renderFilteredTables(this.searchIndex);
    }
    
    async copyToClipboard(button) {
        const codeBlock = button.parentElement.querySelector('pre code');
        if (codeBlock) {
            try {
                await navigator.clipboard.writeText(codeBlock.textContent);
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            } catch (error) {
                console.error('Failed to copy:', error);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CatalogApp();
});
