import polars as pl
import os

# Create a directory for data if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Create a sample DataFrame
data = {
    "p_partkey": [1, 2, 3, 4, 5],
    "p_name": ["Part#1", "Part#2", "Part#3", "Part#4", "Part#5"],
    "p_brand": ["Brand#1", "Brand#2", "Brand#3", "Brand#1", "Brand#2"],
    "p_retailprice": [10.0, 20.0, 30.0, 40.0, 50.0],
}
df = pl.DataFrame(data)

# Write to a Parquet file
df.write_parquet("data/parts.parquet")

print("Sample data created at data/parts.parquet") 