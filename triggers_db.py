from config_tables import *

def add_triggers(connection):
    with connection.cursor() as cursor:
        for trigger in triggers:
            try:
                cursor.execute(trigger)
                print("Table created successfully")
            except Exception as ex:
                print("connection is failed", ex)


dishes_insert_prices_trigger = rf"""
    CREATE TRIGGER `insert_dish_prices` AFTER INSERT ON {dishes_composition_table_name}
    FOR EACH ROW BEGIN
        UPDATE {dishes_table_name} SET {dishes_table_name}.cost_price = {dishes_table_name}.cost_price + NEW.cost_price
        WHERE {dishes_table_name}.id = NEW.dish_id;
        UPDATE {dishes_table_name} SET {dishes_table_name}.price = {dishes_table_name}.price + NEW.cost_price
        WHERE {dishes_table_name}.id = NEW.dish_id;
    END;
"""

dishes_update_prices_trigger = rf"""
    CREATE TRIGGER `update_dish_prices` AFTER UPDATE ON {dishes_composition_table_name}
    FOR EACH ROW BEGIN
        UPDATE {dishes_table_name} SET {dishes_table_name}.cost_price = {dishes_table_name}.cost_price - OLD.cost_price + NEW.cost_price
        WHERE {dishes_table_name}.id = NEW.dish_id;
        UPDATE {dishes_table_name} SET {dishes_table_name}.price = {dishes_table_name}.price - OLD.cost_price + NEW.cost_price
        WHERE {dishes_table_name}.id = NEW.dish_id;
    END;
"""

dishes_composition_update_trigger = rf"""
    CREATE TRIGGER `update_dishes_composition_cost_price` AFTER UPDATE ON {ingredients_table_name}
    FOR EACH ROW BEGIN
        UPDATE {dishes_composition_table_name} SET {dishes_composition_table_name}.cost_price = NEW.cost_price * {dishes_composition_table_name}.quantity
        WHERE {dishes_composition_table_name}.ingredient_id = NEW.id;
    END;
"""

orders_insert_prices_trigger = rf"""
    CREATE TRIGGER `insert_order_prices` AFTER INSERT ON {order_units_table_name}
    FOR EACH ROW BEGIN
        SET @discount_id := (SELECT discount_id FROM `{orders_table_name}`
        WHERE id = NEW.order_id);
        SET @discount := (SELECT discount_percentage FROM `{discounts_table_name}`
        WHERE id = @discount_id);
        UPDATE {orders_table_name} SET {orders_table_name}.cost_price = {orders_table_name}.cost_price + NEW.cost_price
        WHERE {orders_table_name}.id = NEW.order_id;
        UPDATE {orders_table_name} SET {orders_table_name}.amount = {orders_table_name}.amount + NEW.amount
        WHERE {orders_table_name}.id = NEW.order_id;
        UPDATE {orders_table_name} SET {orders_table_name}.total_amount = {orders_table_name}.total_amount + NEW.amount * (1 - @discount / 100)
        WHERE {orders_table_name}.id = NEW.order_id;
    END;
"""

triggers = [dishes_update_prices_trigger, dishes_insert_prices_trigger, dishes_composition_update_trigger,
            orders_insert_prices_trigger]