"""
Static Site Generator for Neuralake "Code as a Catalog" System

Generates browsable HTML documentation from catalog metadata JSON,
following Neuralink's philosophy of automated documentation generation.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader
import shutil

logger = logging.getLogger(__name__)

class CatalogSiteGenerator:
    """
    Static site generator for catalog documentation.
    
    Converts catalog metadata JSON into browsable HTML pages with:
    - Table listing with search and filtering
    - Individual table detail pages
    - Schema visualization
    - Copy-paste Python code snippets
    """
    
    def __init__(self, output_dir: Path = Path("catalog-site")):
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(__file__).parent / "templates"
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )
        
        # Add custom filters
        self.jinja_env.filters['format_datetime'] = self._format_datetime
        self.jinja_env.filters['format_schema'] = self._format_schema
        
    def generate_site(self, catalog_metadata: Dict[str, Any], 
                     project_name: str = "Neuralake Data Catalog") -> None:
        """
        Generate complete static site from catalog metadata.
        
        Args:
            catalog_metadata: Output from Catalog.export_catalog_metadata()
            project_name: Name to display in site header
        """
        logger.info(f"🌐 Generating static site for {len(catalog_metadata.get('tables', {}))} tables")
        
        # Copy static assets
        self._copy_static_assets()
        
        # Generate index page with table listing
        self._generate_index_page(catalog_metadata, project_name)
        
        # Generate individual table pages
        self._generate_table_pages(catalog_metadata.get('tables', {}))
        
        # Generate search index JSON
        self._generate_search_index(catalog_metadata.get('tables', {}))
        
        # Generate API reference
        self._generate_api_reference(catalog_metadata, project_name)
        
        logger.info(f"✅ Static site generated at: {self.output_dir.absolute()}")
        logger.info(f"   Open: file://{self.output_dir.absolute()}/index.html")
        
    def _copy_static_assets(self) -> None:
        """Copy CSS, JS, and other static assets."""
        static_dir = self.output_dir / "static"
        static_dir.mkdir(exist_ok=True)
        
        # Create modern CSS
        css_content = """
/* Neuralake Catalog Modern CSS */
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --bg-color: #f8fafc;
    --text-color: #1e293b;
    --border-color: #e2e8f0;
    --card-bg: #ffffff;
    --code-bg: #f1f5f9;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem 0;
    margin-bottom: 2rem;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

.subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-top: 0.5rem;
}

.search-container {
    margin: 2rem 0;
    position: relative;
}

.search-box {
    width: 100%;
    padding: 12px 20px;
    font-size: 16px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s;
}

.search-box:focus {
    border-color: var(--primary-color);
}

.filters {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.filter-tag {
    padding: 6px 12px;
    background: var(--code-bg);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 14px;
}

.filter-tag:hover,
.filter-tag.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

.table-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.table-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}

.table-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.table-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.table-type {
    display: inline-block;
    padding: 4px 8px;
    background: var(--primary-color);
    color: white;
    border-radius: 4px;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.table-description {
    color: #64748b;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}

.table-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
    color: #64748b;
}

.code-snippet {
    background: var(--code-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    position: relative;
}

.code-snippet pre {
    overflow-x: auto;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 14px;
    line-height: 1.4;
}

.copy-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.copy-button:hover {
    background: var(--secondary-color);
}

.schema-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    background: var(--card-bg);
}

.schema-table th,
.schema-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.schema-table th {
    background: var(--code-bg);
    font-weight: 600;
}

.tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.tag {
    padding: 4px 8px;
    background: var(--code-bg);
    border-radius: 12px;
    font-size: 12px;
    color: var(--text-color);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    display: block;
}

.stat-label {
    color: #64748b;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

footer {
    margin-top: 4rem;
    padding: 2rem 0;
    border-top: 1px solid var(--border-color);
    text-align: center;
    color: #64748b;
}

@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .table-grid {
        grid-template-columns: 1fr;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
"""
        
        with open(static_dir / "styles.css", "w") as f:
            f.write(css_content)
        
        # Create JavaScript for interactivity
        js_content = """
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
"""
        
        with open(static_dir / "app.js", "w") as f:
            f.write(js_content)
            
    def _generate_index_page(self, catalog_metadata: Dict[str, Any], 
                           project_name: str) -> None:
        """Generate the main index page with table listing."""
        tables = catalog_metadata.get('tables', {})
        
        # Calculate statistics
        stats = {
            'total_tables': len(tables),
            'function_tables': len([t for t in tables.values() if t['table_type'] == 'function']),
            'delta_tables': len([t for t in tables.values() if t['table_type'] == 'delta']),
            'parquet_tables': len([t for t in tables.values() if t['table_type'] == 'parquet']),
            'export_time': catalog_metadata.get('export_time', datetime.now().isoformat())
        }
        
        # Get unique table types for filters
        table_types = list(set(t['table_type'] for t in tables.values()))
        
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <link rel="stylesheet" href="./static/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div>
                    <h1>{{ project_name }}</h1>
                    <div class="subtitle">Code as a Catalog • Automatically Generated Documentation</div>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{{ stats.total_tables }}</span>
                <div class="stat-label">Total Tables</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{{ stats.function_tables }}</span>
                <div class="stat-label">Function Tables</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{{ stats.delta_tables }}</span>
                <div class="stat-label">Delta Tables</div>
            </div>
            <div class="stat-card">
                <span class="stat-number">{{ stats.parquet_tables }}</span>
                <div class="stat-label">Parquet Tables</div>
            </div>
        </div>
        
        <!-- Search and Filters -->
        <div class="search-container">
            <input type="text" id="searchBox" class="search-box" 
                   placeholder="Search tables by name, description, or tags...">
        </div>
        
        <div class="filters">
            <div class="filter-tag active" data-filter="all">All Tables</div>
            {% for table_type in table_types %}
            <div class="filter-tag" data-filter="{{ table_type }}">{{ table_type.title() }} Tables</div>
            {% endfor %}
        </div>
        
        <!-- Table Grid -->
        <div id="tableGrid" class="table-grid">
            <!-- Tables will be populated by JavaScript -->
        </div>
        
        <!-- Quick Start -->
        <section style="margin-top: 3rem;">
            <h2>Quick Start</h2>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code># Install and use the catalog
from neuralake.src.catalog_core import default_catalog

# List all available tables
tables = default_catalog.list_tables()
print(f"Available tables: {tables}")

# Get a table as a Polars LazyFrame
df = default_catalog.table("your_table_name")
data = df.collect()  # Execute the query</code></pre>
            </div>
        </section>
    </div>
    
    <footer>
        <div class="container">
            <p>Generated on {{ stats.export_time | format_datetime }} • 
               <a href="./api-reference.html">API Reference</a> • 
               Powered by Neuralake</p>
        </div>
    </footer>
    
    <script src="./static/app.js"></script>
</body>
</html>
"""
        
        template = Template(template_content)
        html_content = template.render(
            project_name=project_name,
            stats=stats,
            table_types=table_types,
            tables=tables
        )
        
        with open(self.output_dir / "index.html", "w") as f:
            f.write(html_content)
            
    def _generate_table_pages(self, tables: Dict[str, Any]) -> None:
        """Generate individual pages for each table."""
        tables_dir = self.output_dir / "tables"
        tables_dir.mkdir(exist_ok=True)
        
        for table_name, table_info in tables.items():
            self._generate_table_page(table_name, table_info, tables_dir)
            
    def _generate_table_page(self, table_name: str, table_info: Dict[str, Any], 
                           tables_dir: Path) -> None:
        """Generate individual table detail page."""
        
        # Generate Python code snippets
        snippets = self._generate_code_snippets(table_name, table_info)
        
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ table_name }} - Neuralake Catalog</title>
    <link rel="stylesheet" href="../static/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div>
                    <h1>{{ table_name }}</h1>
                    <div class="subtitle">
                        <span class="table-type">{{ table_info.table_type }}</span>
                        {{ table_info.description or "No description available" }}
                    </div>
                </div>
                <div>
                    <a href="../index.html" style="color: white; text-decoration: none;">← Back to Catalog</a>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <!-- Table Information -->
        <section>
            <h2>Table Information</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
                <div>
                    <strong>Type:</strong> {{ table_info.table_type.title() }}
                </div>
                <div>
                    <strong>Owner:</strong> {{ table_info.owner or "Unknown" }}
                </div>
                <div>
                    <strong>Created:</strong> {{ table_info.created_at | format_datetime }}
                </div>
                <div>
                    <strong>Source:</strong> {{ table_info.source_module }}.{{ table_info.source_function }}
                </div>
            </div>
            
            {% if table_info.tags %}
            <div class="tags">
                {% for tag in table_info.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </section>
        
        <!-- Schema -->
        {% if table_info.schema %}
        <section>
            <h2>Schema</h2>
            <table class="schema-table">
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    {% for column, type in table_info.schema.items() %}
                    <tr>
                        <td><code>{{ column }}</code></td>
                        <td>{{ type }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% endif %}
        
        <!-- Code Snippets -->
        <section>
            <h2>Usage Examples</h2>
            
            <h3>Basic Usage</h3>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>{{ snippets.basic }}</code></pre>
            </div>
            
            <h3>Advanced Query</h3>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>{{ snippets.advanced }}</code></pre>
            </div>
            
            {% if table_info.table_type == 'function' %}
            <h3>Direct Function Call</h3>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>{{ snippets.direct }}</code></pre>
            </div>
            {% endif %}
            
            <h3>Export to Different Formats</h3>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>{{ snippets.export }}</code></pre>
            </div>
        </section>
        
        {% if table_info.partition_columns %}
        <section>
            <h2>Partitioning</h2>
            <p>This table is partitioned by:</p>
            <ul>
                {% for column in table_info.partition_columns %}
                <li><code>{{ column }}</code></li>
                {% endfor %}
            </ul>
        </section>
        {% endif %}
    </div>
    
    <footer>
        <div class="container">
            <p><a href="../index.html">← Back to Catalog</a> • 
               <a href="../api-reference.html">API Reference</a> • 
               Powered by Neuralake</p>
        </div>
    </footer>
    
    <script src="../static/app.js"></script>
</body>
</html>
"""
        
        template = Template(template_content)
        html_content = template.render(
            table_name=table_name,
            table_info=table_info,
            snippets=snippets
        )
        
        with open(tables_dir / f"{table_name}.html", "w") as f:
            f.write(html_content)
            
    def _generate_code_snippets(self, table_name: str, table_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate Python code snippets for a table."""
        
        basic_snippet = f"""# Import the catalog
from neuralake.src.catalog_core import default_catalog

# Get the table as a Polars LazyFrame
{table_name}_df = default_catalog.table("{table_name}")

# Execute the query and get results
data = {table_name}_df.collect()
print(f"Shape: {{data.shape}}")
print(data.head())"""

        advanced_snippet = f"""# Advanced querying with Polars
import polars as pl
from neuralake.src.catalog_core import default_catalog

# Get table and perform operations
{table_name}_df = (
    default_catalog.table("{table_name}")
    .filter(pl.col("your_column") > 0)  # Add your filter conditions
    .select([  # Select specific columns
        pl.col("*")  # or specify columns: pl.col("col1"), pl.col("col2")
    ])
    .limit(1000)  # Limit results if needed
)

# Execute and collect results
result = {table_name}_df.collect()"""

        export_snippet = f"""# Export to different formats
from neuralake.src.catalog_core import default_catalog

# Get the data
{table_name}_df = default_catalog.table("{table_name}")
data = {table_name}_df.collect()

# Export to CSV
data.write_csv("output.csv")

# Export to Parquet
data.write_parquet("output.parquet")

# Convert to Pandas if needed
pandas_df = data.to_pandas()

# Convert to PyArrow Table
arrow_table = data.to_arrow()"""

        snippets = {
            "basic": basic_snippet,
            "advanced": advanced_snippet,
            "export": export_snippet
        }
        
        # Add function-specific snippet if it's a function table
        if table_info.get('table_type') == 'function':
            direct_snippet = f"""# Direct function call (for function tables)
from {table_info.get('source_module', 'your_module')} import {table_info.get('source_function', table_name)}

# Call the function directly
{table_name}_df = {table_info.get('source_function', table_name)}()
data = {table_name}_df.collect()"""
            
            snippets["direct"] = direct_snippet
            
        return snippets
        
    def _generate_search_index(self, tables: Dict[str, Any]) -> None:
        """Generate JSON search index for client-side search."""
        search_index = []
        
        for table_name, table_info in tables.items():
            search_index.append({
                "name": table_name,
                "description": table_info.get("description", ""),
                "table_type": table_info.get("table_type", ""),
                "tags": table_info.get("tags", []),
                "schema": table_info.get("schema", {}),
                "owner": table_info.get("owner", ""),
                "url": f"./tables/{table_name}.html"
            })
            
        with open(self.output_dir / "search-index.json", "w") as f:
            json.dump(search_index, f, indent=2)
            
    def _generate_api_reference(self, catalog_metadata: Dict[str, Any], 
                              project_name: str) -> None:
        """Generate API reference documentation."""
        
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Reference - {{ project_name }}</title>
    <link rel="stylesheet" href="./static/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div>
                    <h1>API Reference</h1>
                    <div class="subtitle">Neuralake Catalog Python API</div>
                </div>
                <div>
                    <a href="./index.html" style="color: white; text-decoration: none;">← Back to Catalog</a>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <section>
            <h2>Core Catalog API</h2>
            
            <h3>default_catalog.table(name, **kwargs)</h3>
            <p>Get a table as a Polars LazyFrame.</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>from neuralake.src.catalog_core import default_catalog

# Get a table
df = default_catalog.table("your_table_name")
data = df.collect()  # Execute the lazy query</code></pre>
            </div>
            
            <h3>default_catalog.list_tables(table_type=None)</h3>
            <p>List all available tables, optionally filtered by type.</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code># List all tables
all_tables = default_catalog.list_tables()

# List only function tables
from neuralake.src.catalog_core import TableType
function_tables = default_catalog.list_tables(TableType.FUNCTION)</code></pre>
            </div>
            
            <h3>default_catalog.describe_table(name)</h3>
            <p>Get detailed metadata about a table.</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code># Get table metadata
metadata = default_catalog.describe_table("your_table_name")
print(f"Columns: {metadata['column_count']}")
print(f"Schema: {metadata['inferred_schema']}")
print(f"Description: {metadata['metadata']['description']}")</code></pre>
            </div>
        </section>
        
        <section>
            <h2>Table Registration</h2>
            
            <h3>@table Decorator</h3>
            <p>Register a function as a table in the catalog.</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>from neuralake.src.catalog_core import table
import polars as pl

@table(description="Sample user data", tags=["users", "demo"])
def users_table():
    \"\"\"User data from the API.\"\"\"
    return pl.LazyFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "email": ["alice@example.com", "bob@example.com", "charlie@example.com"]
    })</code></pre>
            </div>
            
            <h3>register_static_table()</h3>
            <p>Register existing table objects (Delta, Parquet).</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code>from neuralake.src.catalog_core import register_static_table
from neuralake.src.delta_tables import NeuralakeDeltaTable

# Register a Delta table
delta_table = NeuralakeDeltaTable("user_events")
register_static_table(
    delta_table, 
    "user_events",
    description="User interaction events",
    tags=["events", "analytics"]
)</code></pre>
            </div>
        </section>
        
        <section>
            <h2>Data Export</h2>
            <p>All tables return Polars LazyFrames, which can be exported to various formats:</p>
            <div class="code-snippet">
                <button class="copy-button">Copy</button>
                <pre><code># Get table data
df = default_catalog.table("your_table_name").collect()

# Export options
df.write_csv("data.csv")
df.write_parquet("data.parquet")
df.write_json("data.json")

# Convert to other formats
pandas_df = df.to_pandas()
arrow_table = df.to_arrow()
numpy_array = df.to_numpy()</code></pre>
            </div>
        </section>
    </div>
    
    <footer>
        <div class="container">
            <p><a href="./index.html">← Back to Catalog</a> • Powered by Neuralake</p>
        </div>
    </footer>
    
    <script src="./static/app.js"></script>
</body>
</html>
"""
        
        template = Template(template_content)
        html_content = template.render(project_name=project_name)
        
        with open(self.output_dir / "api-reference.html", "w") as f:
            f.write(html_content)
            
    def _format_datetime(self, date_str: str) -> str:
        """Format datetime string for display."""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return date_str
            
    def _format_schema(self, schema: Dict[str, str]) -> str:
        """Format schema dictionary for display."""
        if not schema:
            return "No schema information"
        return ", ".join(f"{col}: {dtype}" for col, dtype in schema.items())


def generate_catalog_site(output_dir: str = "catalog-site", 
                         project_name: str = "Neuralake Data Catalog") -> None:
    """
    Convenience function to generate catalog site.
    
    Args:
        output_dir: Directory to output the static site
        project_name: Name to display in site header
    """
    from .catalog_core import default_catalog
    
    # Export catalog metadata
    catalog_metadata = default_catalog.export_catalog_metadata()
    
    # Generate site
    generator = CatalogSiteGenerator(Path(output_dir))
    generator.generate_site(catalog_metadata, project_name)
    
    return Path(output_dir).absolute() 