from neuralake.core import Catalog, ModuleDatabase
import my_tables

# Create a catalog
dbs = {"demo_db": ModuleDatabase(my_tables)}
DemoCatalog = Catalog(dbs) 