import re
from table import Table

waiters_table_name = "Waiters"
order_units_table_name = "Order_units"
discounts_table_name = "Discounts"
groups_table_name = "Groups"
ingredients_table_name = "Ingredients"
dishes_table_name = "Dishes"
dishes_composition_table_name = "Dishes_composition"
orders_table_name = "Orders"

waiters_table = rf"""
    CREATE TABLE IF NOT EXISTS {waiters_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        bio VARCHAR(512) NOT NULL
    );
"""

ingredients_table = rf"""
    CREATE TABLE IF NOT EXISTS {ingredients_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(128) NOT NULL, 
        cost_price INT NOT NULL,
        measuring_unit VARCHAR(64) NOT NULL
    );
"""

dishes_composition_table = rf"""
    CREATE TABLE IF NOT EXISTS {dishes_composition_table_name}
    (
        dish_id INT NOT NULL,
        ingredient_id INT NOT NULL,
        quantity INT NOT NULL,
        cost_price INT NOT NULL,
        FOREIGN KEY (ingredient_id)
            REFERENCES Ingredients (id),
        FOREIGN KEY (dish_id)
            REFERENCES Dishes (id)  
    );
"""

dishes_table = rf"""
    CREATE TABLE IF NOT EXISTS {dishes_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(128) NOT NULL,
        group_id INT NOT NULL,
        cost_price FLOAT NOT NULL,
        price FLOAT NOT NULL,
        markup INT NOT NULL,
        FOREIGN KEY (group_id)
            REFERENCES Groups (id)
    );
"""

groups_table = rf"""
    CREATE TABLE IF NOT EXISTS {groups_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(128) NOT NULL
    );
"""

orders_table = rf"""
    CREATE TABLE IF NOT EXISTS {orders_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        waiter_id INT NOT NULL,
        discount_id INT NOT NULL,
        cost_price FLOAT NOT NULL,
        amount FLOAT NOT NULL,
        total_amount FLOAT NOT NULL,
        FOREIGN KEY (waiter_id)
            REFERENCES Waiters (id),
        FOREIGN KEY (discount_id)
            REFERENCES Discounts (id)
    );
"""
discounts_table = rf"""
    CREATE TABLE IF NOT EXISTS {discounts_table_name}
    (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(256) NOT NULL,
        discount_percentage INT(100) NOT NULL
    );
"""

order_units_table = rf"""
    CREATE TABLE IF NOT EXISTS {order_units_table_name}
    (
        order_id INT NOT NULL,
        dish_id INT NOT NULL,
        cost_price FLOAT NOT NULL,
        quantity INT NOT NULL,
        amount FLOAT NOT NULL,
        FOREIGN KEY (order_id)
            REFERENCES Orders (id),
        FOREIGN KEY (dish_id)
            REFERENCES Dishes (id)
    );
"""

g_tables = (waiters_table, discounts_table, groups_table,
            ingredients_table, dishes_table, dishes_composition_table,  orders_table, order_units_table)
g_tables_names = (waiters_table_name, discounts_table_name, groups_table_name,
                  ingredients_table_name, dishes_table_name, dishes_composition_table_name,  orders_table_name, order_units_table_name,)
g_table_dict = {}


def fill_table_fields():
    tables_info = list(zip(g_tables_names, g_tables))
    for table_pair in tables_info:
        g_table_dict[table_pair[0]] = Table(list(re.findall("(?<= )[a-z_]+(?= )", table_pair[1])))
