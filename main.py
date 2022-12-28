import pymysql
from config_tables import g_tables
from config_db import *
from config_tables import fill_table_fields
from connection_api import *
from fill_tables_api import *
from procedures_db import add_procedures
from triggers_db import add_triggers
from gui import *

if __name__ != "__main__":
    print("Incorrect use of main file")

#
connection = connect_db()
create_tables(connection, g_tables)
# add_triggers(connection)
fill_table_fields()
# add_ingredients(connection)
# add_groups(connection)
# add_dishes(connection)
# add_dishes_composition(connection)
# add_waiters(connection)
# add_discounts(connection)
# add_orders(connection)
# add_order_units(connection)
# add_procedures(connection)
create_gui(connection)
