import my_tables

from neuralake.core import Catalog, ModuleDatabase

# Create a catalog
dbs = {"demo_db": ModuleDatabase(my_tables)}
DemoCatalog = Catalog(dbs)
