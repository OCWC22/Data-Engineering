from my_catalog import DemoCatalog
from neuralake.core import Filter

def main():
    """
    This script demonstrates how to use a neuralake catalog to query and join tables.
    """
    print("Querying data using the neuralake catalog...")

    # Get part and supplier information
    # We apply a filter to the 'part' table to select only specific brands
    part_data = DemoCatalog.db("demo_db").table(
        "part",
        (
            Filter('p_brand', 'in', ['Brand#1', 'Brand#2']),
        ),
    )

    # Get the full supplier table
    supplier_data = DemoCatalog.db("demo_db").table("supplier")

    # Join part and supplier data on their keys
    # and select the columns we are interested in.
    # The .collect() call executes the query.
    joined_data = part_data.join(
        supplier_data,
        left_on="p_partkey",
        right_on="s_suppkey",
    ).select(["p_name", "p_brand", "s_name"]).collect()

    print("\\nJoined data:")
    print(joined_data)


if __name__ == "__main__":
    main() 