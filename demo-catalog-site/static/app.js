// Neuralake Catalog Interactive JavaScript

class CatalogApp {
    constructor() {
        this.searchIndex = [];
        this.currentFilter = 'all';
        this.init();
    }
    
    async init() {
        console.log('🔧 Initializing Catalog App...');
        await this.loadSearchIndex();
        this.setupEventListeners();
        this.renderTables();
        console.log('✅ Catalog App initialized successfully');
    }
    
    async loadSearchIndex() {
        try {
            console.log('📊 Loading table data...');
            
            // Use embedded data if available, otherwise try to fetch
            if (window.CATALOG_DATA) {
                this.searchIndex = window.CATALOG_DATA;
                console.log(`✅ Loaded ${this.searchIndex.length} tables from embedded data`);
            } else {
                console.log('📡 Fetching search index...');
                const response = await fetch('./search-index.json');
                this.searchIndex = await response.json();
                console.log(`✅ Loaded ${this.searchIndex.length} tables from JSON file`);
            }
        } catch (error) {
            console.error('❌ Failed to load search index:', error);
            // Fallback to empty array if everything fails
            this.searchIndex = [];
        }
    }
    
    setupEventListeners() {
        console.log('🎧 Setting up event listeners...');
        
        const searchBox = document.getElementById('searchBox');
        if (searchBox) {
            searchBox.addEventListener('input', (e) => {
                console.log(`🔍 Search query: "${e.target.value}"`);
                this.handleSearch(e.target.value);
            });
            console.log('✅ Search box listener added');
        } else {
            console.error('❌ Search box not found');
        }
        
        const filterTags = document.querySelectorAll('.filter-tag');
        console.log(`🏷️ Found ${filterTags.length} filter tags`);
        filterTags.forEach((tag, index) => {
            tag.addEventListener('click', (e) => {
                const filter = e.target.dataset.filter;
                console.log(`🎯 Filter clicked: ${filter}`);
                this.handleFilter(filter);
            });
        });
        
        // Copy button functionality
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('copy-button')) {
                console.log('📋 Copy button clicked');
                this.copyToClipboard(e.target);
            }
        });
        
        console.log('✅ All event listeners set up');
    }
    
    handleSearch(query) {
        console.log(`🔍 Processing search: "${query}"`);
        const filteredTables = this.searchIndex.filter(table => 
            table.name.toLowerCase().includes(query.toLowerCase()) ||
            table.description.toLowerCase().includes(query.toLowerCase()) ||
            table.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
        );
        console.log(`📊 Found ${filteredTables.length} matching tables`);
        this.renderFilteredTables(filteredTables);
    }
    
    handleFilter(filter) {
        console.log(`🎯 Processing filter: ${filter}`);
        
        // Update active filter
        document.querySelectorAll('.filter-tag').forEach(tag => {
            tag.classList.remove('active');
        });
        const activeTag = document.querySelector(`[data-filter="${filter}"]`);
        if (activeTag) {
            activeTag.classList.add('active');
        }
        
        this.currentFilter = filter;
        
        let filteredTables = this.searchIndex;
        if (filter !== 'all') {
            filteredTables = this.searchIndex.filter(table => 
                table.table_type === filter
            );
        }
        
        console.log(`📊 Filtered to ${filteredTables.length} tables`);
        this.renderFilteredTables(filteredTables);
    }
    
    renderFilteredTables(tables) {
        console.log(`🎨 Rendering ${tables.length} tables`);
        const grid = document.getElementById('tableGrid');
        if (!grid) {
            console.error('❌ Table grid element not found');
            return;
        }
        
        if (tables.length === 0) {
            grid.innerHTML = '<div style="text-align: center; padding: 2rem; color: #666;">No tables found matching your criteria.</div>';
            return;
        }
        
        grid.innerHTML = tables.map(table => `
            <div class="table-card" onclick="window.location.href='${table.url}'" style="cursor: pointer;">
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
        
        console.log('✅ Tables rendered successfully');
    }
    
    renderTables() {
        console.log('🎨 Initial table render');
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
                console.log('✅ Code copied to clipboard');
            } catch (error) {
                console.error('❌ Failed to copy:', error);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = codeBlock.textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, starting Catalog App...');
    new CatalogApp();
});

// Debug info
console.log('📜 Catalog App script loaded');
console.log('📊 Embedded data available:', !!window.CATALOG_DATA);
if (window.CATALOG_DATA) {
    console.log(`📋 ${window.CATALOG_DATA.length} tables in embedded data`);
}
