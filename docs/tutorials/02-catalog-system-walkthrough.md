# Tutorial: Building Your First Catalog Table

## 🎯 **Learning Goals**

By the end of this tutorial, you will:
- **Define your first function table** using the `@table` decorator
- **Register and query a Delta table** for production-scale data
- **Generate documentation** using the SSG system
- **Understand when to use each table type** through hands-on experience

## 📋 **Prerequisites** 

Before starting this tutorial:
- ✅ Complete [`01-foundations-lakehouse-ingestion.md`](./01-foundations-lakehouse-ingestion.md)
- ✅ Read [`../explanation/concepts/catalog-architecture-fundamentals.md`](../explanation/concepts/catalog-architecture-fundamentals.md)
- ✅ Have local MinIO running (`./setup_minio.sh`)
- ✅ Python environment set up with Poetry

## 🚀 **Part 1: Your First Function Table**

Function tables are perfect for getting started because they require zero infrastructure. Let's create a table for analyzing team productivity.

### **Step 1: Create Your Module**

```bash
cd neuralake/src
touch team_analytics.py
```

### **Step 2: Define the Function Table**

Open `team_analytics.py` and add:

```python
import polars as pl
from catalog_core import table
from datetime import datetime, timedelta

@table(
    description="Daily team productivity metrics for engineering teams",
    tags=["team", "productivity", "engineering"],
    owner="your-name",
    schema={
        "date": "Date",
        "team": "Utf8", 
        "commits": "Int64",
        "pull_requests": "Int64",
        "lines_added": "Int64",
        "lines_removed": "Int64",
        "tests_added": "Int64"
    }
)
def team_productivity():
    """
    Engineering team productivity metrics collected daily.
    
    This simulates data you might collect from GitHub API, Jira, etc.
    In production, this would fetch real data from your engineering tools.
    """
    # Generate 30 days of mock data for 3 teams
    dates = [datetime.now().date() - timedelta(days=i) for i in range(30)]
    teams = ["backend", "frontend", "data"]
    
    data = []
    for date in dates:
        for team in teams:
            # Simulate realistic team productivity patterns
            base_commits = {"backend": 8, "frontend": 12, "data": 6}[team]
            base_prs = {"backend": 3, "frontend": 4, "data": 2}[team]
            
            data.append({
                "date": date,
                "team": team,
                "commits": base_commits + (date.day % 5),  # Some variation
                "pull_requests": base_prs + (date.day % 3),
                "lines_added": (base_commits * 50) + (date.day * 20),
                "lines_removed": (base_commits * 20) + (date.day * 8),
                "tests_added": base_prs * 2
            })
    
    return pl.LazyFrame(data)

# Optional: Add a derived table for weekly summaries
@table(
    description="Weekly team productivity summaries with trends",
    tags=["team", "productivity", "weekly", "summary"],
    owner="your-name"
)
def weekly_team_summary():
    """Weekly aggregated team productivity with week-over-week trends."""
    daily_data = team_productivity()
    
    return (
        daily_data
        .with_columns([
            pl.col("date").dt.week().alias("week"),
            pl.col("date").dt.year().alias("year")
        ])
        .group_by(["year", "week", "team"])
        .agg([
            pl.col("commits").sum().alias("total_commits"),
            pl.col("pull_requests").sum().alias("total_prs"),
            pl.col("lines_added").sum().alias("total_lines_added"),
            pl.col("lines_removed").sum().alias("total_lines_removed"),
            pl.col("tests_added").sum().alias("total_tests"),
            pl.col("date").min().alias("week_start")
        ])
        .sort(["year", "week", "team"])
    )
```

### **Step 3: Test Your Function Table**

Create a test script:

```bash
touch ../scripts/test_team_analytics.py
```

Add this content:

```python
#!/usr/bin/env python3
"""Test our new team analytics tables."""

import sys
sys.path.append('src')

from catalog_core import Catalog
import team_analytics  # This triggers registration

def main():
    catalog = Catalog()
    
    print("🔍 Testing team_productivity table...")
    productivity = catalog.table("team_productivity")
    
    # Show basic stats
    print(f"📊 Total rows: {productivity.select(pl.count()).collect().item()}")
    print(f"📅 Date range: {productivity.select([pl.col('date').min(), pl.col('date').max()]).collect()}")
    print(f"👥 Teams: {productivity.select(pl.col('team').unique()).collect()}")
    
    # Show sample data
    print("\n📋 Sample data:")
    print(productivity.head(5).collect())
    
    # Test weekly summary
    print("\n🔍 Testing weekly_team_summary table...")
    weekly = catalog.table("weekly_team_summary")
    print(f"📊 Weekly summary rows: {weekly.select(pl.count()).collect().item()}")
    print("\n📋 Weekly summary sample:")
    print(weekly.head(3).collect())
    
    # Example analysis: most productive team last week
    print("\n🏆 Most productive team analysis:")
    top_team = (
        weekly
        .sort("week_start", descending=True)
        .head(3)  # Last week's data
        .group_by("team")
        .agg(pl.col("total_commits").sum().alias("commits"))
        .sort("commits", descending=True)
        .head(1)
        .collect()
    )
    print(top_team)

if __name__ == "__main__":
    main()
```

Run the test:

```bash
cd neuralake
python scripts/test_team_analytics.py
```

You should see your data being generated and queried!

### **Step 4: Generate Documentation**

Let's see how your tables automatically appear in documentation:

```bash
python scripts/generate_demo_catalog_site.py
```

Open `demo-catalog-site/index.html` in your browser and search for "team" to find your new tables.

## 🚀 **Part 2: Working with Delta Tables**

Now let's create a Delta table for handling larger, production-scale data with ACID properties.

### **Step 5: Create a Delta Table for Events**

Add this to your `team_analytics.py`:

```python
from delta_tables import NeuralakeDeltaTable, register_static_table
from delta_config import get_delta_config

# Create Delta table for event tracking
def setup_team_events_delta_table():
    """Set up a Delta table for tracking detailed team events."""
    
    # This would be called once to set up the table
    delta_table = NeuralakeDeltaTable("team_events")
    
    register_static_table(
        delta_table,
        "team_events",
        description="Detailed engineering team events with full audit trail",
        tags=["team", "events", "audit", "delta"],
        owner="your-name",
        schema={
            "timestamp": "Datetime",
            "team": "Utf8",
            "event_type": "Utf8",  # commit, pr_opened, pr_merged, etc.
            "user": "Utf8",
            "details": "Utf8",
            "metadata": "Utf8"  # JSON string
        }
    )
    
    return delta_table

# Call this to set up the table (run once)
# delta_table = setup_team_events_delta_table()
```

### **Step 6: Write Data to Delta Table**

Create a script to populate your Delta table:

```bash
touch ../scripts/populate_team_events.py
```

```python
#!/usr/bin/env python3
"""Populate the team events Delta table with sample data."""

import sys
sys.path.append('src')

import polars as pl
from datetime import datetime, timedelta
import json
import random

from team_analytics import setup_team_events_delta_table
from catalog_core import Catalog

def generate_team_events(days=7):
    """Generate realistic team events for the last N days."""
    
    events = []
    teams = ["backend", "frontend", "data"]
    users = {
        "backend": ["alice", "bob", "charlie"],
        "frontend": ["diana", "eve", "frank"], 
        "data": ["grace", "henry", "iris"]
    }
    
    event_types = ["commit", "pr_opened", "pr_merged", "deployment", "bug_report"]
    
    start_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        for team in teams:
            # Each team generates 10-30 events per day
            num_events = random.randint(10, 30)
            
            for _ in range(num_events):
                event_time = current_date + timedelta(
                    hours=random.randint(8, 18),  # Business hours
                    minutes=random.randint(0, 59)
                )
                
                event_type = random.choice(event_types)
                user = random.choice(users[team])
                
                # Generate realistic event details
                details = {
                    "commit": f"Fixed bug in {team} module",
                    "pr_opened": f"Add new feature to {team} service",
                    "pr_merged": f"Merge feature branch into main",
                    "deployment": f"Deploy {team} service v1.{random.randint(1,9)}",
                    "bug_report": f"Critical bug in {team} reported"
                }[event_type]
                
                metadata = json.dumps({
                    "files_changed": random.randint(1, 15),
                    "lines_added": random.randint(10, 500),
                    "impact": random.choice(["low", "medium", "high"])
                })
                
                events.append({
                    "timestamp": event_time,
                    "team": team,
                    "event_type": event_type,
                    "user": user,
                    "details": details,
                    "metadata": metadata
                })
    
    return pl.DataFrame(events)

def main():
    print("🚀 Setting up team events Delta table...")
    
    # Set up the Delta table
    delta_table = setup_team_events_delta_table()
    
    print("📝 Generating sample events...")
    events_df = generate_team_events(days=14)  # 2 weeks of data
    
    print(f"💾 Writing {len(events_df)} events to Delta table...")
    
    # Write to Delta table (this handles ACID transactions)
    delta_table.write_data(events_df)
    
    print("✅ Data written successfully!")
    
    # Test reading the data back
    print("\n🔍 Testing Delta table read...")
    catalog = Catalog()
    events = catalog.table("team_events")
    
    print(f"📊 Total events in Delta table: {events.select(pl.count()).collect().item()}")
    print("\n📋 Sample events:")
    print(events.head(3).collect())
    
    # Test Delta-specific features
    print("\n⏰ Events by type and team:")
    summary = (
        events
        .group_by(["team", "event_type"])
        .agg(pl.count().alias("count"))
        .sort(["team", "count"], descending=[False, True])
        .collect()
    )
    print(summary)

if __name__ == "__main__":
    main()
```

Run it:

```bash
python scripts/populate_team_events.py
```

### **Step 7: Join Function Tables with Delta Tables**

Now let's demonstrate the power of the unified interface - joining data across different table types:

```bash
touch ../scripts/analyze_team_performance.py
```

```python
#!/usr/bin/env python3
"""Analyze team performance by combining function tables and Delta tables."""

import sys
sys.path.append('src')

import polars as pl
from catalog_core import Catalog
import team_analytics  # Register our tables

def main():
    catalog = Catalog()
    
    print("🔗 Joining Function Tables with Delta Tables...")
    
    # Get data from both table types
    daily_productivity = catalog.table("team_productivity")
    team_events = catalog.table("team_events")
    
    # Create a comprehensive team analysis
    print("📊 Computing comprehensive team metrics...")
    
    # First, aggregate events by day and team
    daily_events = (
        team_events
        .with_columns(pl.col("timestamp").dt.date().alias("date"))
        .group_by(["date", "team"])
        .agg([
            pl.count().alias("total_events"),
            pl.col("event_type").filter(pl.col("event_type") == "commit").count().alias("commit_events"),
            pl.col("event_type").filter(pl.col("event_type") == "pr_merged").count().alias("pr_merged_events"),
            pl.col("event_type").filter(pl.col("event_type") == "deployment").count().alias("deployments")
        ])
    )
    
    # Join with daily productivity metrics
    comprehensive_metrics = (
        daily_productivity
        .join(daily_events, on=["date", "team"], how="left")
        .with_columns([
            # Calculate derived metrics
            (pl.col("lines_added") / pl.col("commits")).alias("avg_lines_per_commit"),
            (pl.col("tests_added") / pl.col("pull_requests")).alias("tests_per_pr"),
            (pl.col("total_events").fill_null(0) / 8).alias("events_per_hour")  # 8 hour workday
        ])
        .sort(["date", "team"])
    )
    
    print("📋 Sample comprehensive metrics:")
    print(comprehensive_metrics.head(5).collect())
    
    # Team efficiency analysis
    print("\n🏆 Team Efficiency Analysis (last 7 days):")
    recent_efficiency = (
        comprehensive_metrics
        .filter(pl.col("date") >= pl.col("date").max() - pl.duration(days=7))
        .group_by("team")
        .agg([
            pl.col("avg_lines_per_commit").mean().round(1).alias("avg_lines_per_commit"),
            pl.col("tests_per_pr").mean().round(1).alias("avg_tests_per_pr"),
            pl.col("events_per_hour").mean().round(2).alias("avg_events_per_hour"),
            pl.col("deployments").sum().alias("total_deployments"),
            pl.col("commits").sum().alias("total_commits")
        ])
        .with_columns([
            # Efficiency score (higher is better)
            (pl.col("avg_tests_per_pr") * 2 + 
             pl.col("total_deployments") * 5 +
             pl.col("avg_events_per_hour") * 10).alias("efficiency_score")
        ])
        .sort("efficiency_score", descending=True)
    )
    
    print(recent_efficiency.collect())
    
    print("\n✨ Key Insights:")
    top_team = recent_efficiency.head(1).collect()
    if len(top_team) > 0:
        team_name = top_team[0, "team"]
        score = top_team[0, "efficiency_score"]
        print(f"🥇 Most efficient team: {team_name} (score: {score:.1f})")
    
    print("\n💡 This analysis combines:")
    print("   • Function table data (daily productivity metrics)")
    print("   • Delta table data (detailed events with audit trail)")
    print("   • Unified Polars LazyFrame interface")
    print("   • ACID guarantees from Delta Lake")

if __name__ == "__main__":
    main()
```

Run the analysis:

```bash
python scripts/analyze_team_performance.py
```

## 🚀 **Part 3: Documentation and Discovery**

### **Step 8: Generate Updated Documentation**

Your new tables should automatically appear in the documentation:

```bash
python scripts/generate_demo_catalog_site.py
```

Browse to `demo-catalog-site/index.html` and explore:
- Search for "team" to find your tables
- Click on table cards to see schemas and examples
- Notice how function tables and Delta tables are presented differently
- Check the API reference for copy-paste code examples

### **Step 9: Understanding the Generated Code**

Look at what the SSG generated for your tables:

```bash
ls demo-catalog-site/tables/
```

Open one of your table HTML files to see:
- Rich metadata display
- Schema information
- Executable code examples
- Owner and tag information

## 🎯 **Part 4: When to Use Each Table Type**

Based on what you've built, here's the decision matrix:

### **Function Tables** (`team_productivity`, `weekly_team_summary`)
✅ **Perfect for:**
- Development and prototyping
- Small datasets (< 10M rows)
- Data from APIs or computed results
- Rapidly changing business logic

⚠️ **Consider alternatives when:**
- Data size exceeds memory
- Multiple writers need concurrent access
- You need audit trails or time travel

### **Delta Tables** (`team_events`)
✅ **Perfect for:**
- Production data with multiple writers
- Large datasets (10M+ rows)
- Audit requirements
- Need for ACID transactions
- Time travel queries

⚠️ **Consider alternatives when:**
- Simple reference data that rarely changes
- Single writer, read-heavy workloads
- Infrastructure overhead is a concern

### **Parquet Tables** (not covered, but good for reference data)
✅ **Perfect for:**
- Reference data (countries, categories, etc.)
- External data sources
- Maximum read performance
- Simple file-based storage

## 🎉 **Congratulations!**

You've successfully:
- ✅ Created function tables with the `@table` decorator
- ✅ Set up and populated a Delta table with ACID properties  
- ✅ Joined data across different table types using unified interface
- ✅ Generated automatic documentation using SSG
- ✅ Understood when to use each table type

## 🔄 **Next Steps**

1. **Explore production deployment**: Check out [`../how-to/upgrade_dev_to_prod.md`](../how-to/upgrade_dev_to_prod.md)

2. **Study the case studies**: Read [`../explanation/case-studies/01-debugging-neuralake-v0.0.5.md`](../explanation/case-studies/01-debugging-neuralake-v0.0.5.md) to understand architectural decisions

3. **Add your own tables**: Create tables for your team's actual data sources

4. **Set up CI/CD**: Configure automatic documentation generation in your deployment pipeline

5. **Explore advanced features**: Time travel queries, schema evolution, and data quality validation

## 🤔 **Common Questions**

**Q: My function table is slow. Should I convert to Delta?**
A: If you're processing > 1M rows or the computation takes > 10 seconds, consider Delta. Otherwise, optimize the function first.

**Q: Can I use both approaches for the same dataset?**
A: Yes! You can have a Delta table for raw data and function tables for derived/aggregated views.

**Q: How do I add authentication/permissions?**
A: The current system is designed for internal use. For production, add authentication layers in your query service.

**Q: What happens if I change a function table schema?**
A: Update the `schema` parameter in `@table()`. The SSG will regenerate documentation automatically.

---

**Related Documentation:**
- [`../explanation/concepts/catalog-architecture-fundamentals.md`](../explanation/concepts/catalog-architecture-fundamentals.md) - Deep dive into architecture
- [`01-foundations-lakehouse-ingestion.md`](./01-foundations-lakehouse-ingestion.md) - Environment setup
- [`../explanation/concepts/code-as-catalog-ssg.md`](../explanation/concepts/code-as-catalog-ssg.md) - SSG philosophy and implementation 