from config_tables import *


def calculate_dishes_composition_cost_price(cursor, ingredient_id):
    query = rf"""
        SELECT cost_price FROM {ingredients_table_name} WHERE id = {ingredient_id}
    """
    cursor.execute(query)
    res = cursor.fetchall()
    res = res[0].values()
    res = list(res)
    return res[0]

def get_dish_name(connection, dish_id):
    query = rf"""
        SELECT name FROM {dishes_table_name} WHERE id = {dish_id}
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        res = res[0].values()
        res = list(res)
        return res[0]


def add_waiter(connection, name):
    with connection.cursor() as cursor:
        fields = g_table_dict[waiters_table_name].get_fields_to_string()
        insert_query = f"INSERT INTO `{waiters_table_name}` ({fields}) " \
                       f"VALUES (\'{name}\');"
        print(insert_query)
        cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[waiters_table_name].increase_count_of_rows()

def add_discount(connection, name, discount_percentage):
    with connection.cursor() as cursor:
        fields = g_table_dict[discounts_table_name].get_fields_to_string()
        insert_query = f"INSERT INTO `{discounts_table_name}` ({fields}) " \
                       f"VALUES (\'{name}\', {discount_percentage});"
        print(insert_query)
        cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[discounts_table_name].increase_count_of_rows()


def calculate_orders_unit_cost_price(cursor, dish_id):
    query = rf"""
        SELECT cost_price FROM {dishes_table_name} WHERE id = {dish_id}
    """
    cursor.execute(query)
    res = cursor.fetchall()
    res = res[0].values()
    res = list(res)
    return res[0]

def calculate_orders_unit_price(cursor, dish_id):
    query = rf"""
        SELECT price FROM {dishes_table_name} WHERE id = {dish_id}
    """
    cursor.execute(query)
    res = cursor.fetchall()
    res = res[0].values()
    res = list(res)
    return res[0]

calculate_revenue_procedure_name = 'calculate_revenue'
calculate_revenue_procedure = rf"""
    CREATE PROCEDURE {calculate_revenue_procedure_name}()
    BEGIN
        SELECT SUM(`total_amount`) FROM {orders_table_name};
    END
"""

calculate_profit_procedure_name = 'calculate_profit'
calculate_profit_procedure = rf"""
    CREATE PROCEDURE {calculate_profit_procedure_name}()
    BEGIN
        SELECT SUM(total_amount) - SUM(cost_price) FROM {orders_table_name};
    END
"""

find_most_popular_dish_procedure_name = 'find_most_popular_dish'
find_most_popular_dish_procedure = rf"""
    CREATE PROCEDURE {find_most_popular_dish_procedure_name}()
    BEGIN
        SELECT name, COUNT(dish_id) FROM `{order_units_table_name}` CROSS JOIN {dishes_table_name} WHERE dish_id = id GROUP BY dish_id ORDER BY COUNT(dish_id);
    END
"""

find_most_valuable_waiter_procedure_name = "find_most_valuable_waiter"
find_most_valuable_waiter_procedure = rf"""
    CREATE PROCEDURE {find_most_valuable_waiter_procedure_name}()
    BEGIN
        SELECT bio, SUM(amount) FROM {waiters_table_name} CROSS JOIN {orders_table_name} WHERE waiter_id = {waiters_table_name}.id GROUP BY waiter_id ORDER BY SUM(amount);
    END
"""

find_most_unprofitable_discount_procedure_name = "find_most_unprofitable_discount"
find_most_unprofitable_discount_procedure = rf"""
    CREATE PROCEDURE {find_most_unprofitable_discount_procedure_name}()
    BEGIN
        SELECT name, SUM(amount) - SUM(total_amount) FROM {discounts_table_name}
        CROSS JOIN Orders WHERE discount_id = {discounts_table_name}.id GROUP BY discount_id ORDER BY SUM(amount) - SUM(total_amount);
    END
"""

find_most_popular_group_procedure_name = 'find_most_popular_group'
find_most_popular_group_procedure = rf"""
    CREATE PROCEDURE {find_most_popular_group_procedure_name}()
    BEGIN
        SELECT {groups_table_name}.name, COUNT(dish_id) FROM {groups_table_name}
        JOIN Dishes ON {groups_table_name}.id = {dishes_table_name}.group_id
        JOIN Order_units on {dishes_table_name}.id = {order_units_table_name}.dish_id
        GROUP BY (dish_id) ORDER BY COUNT(dish_id);
    END
"""

def calculate_revenue(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {calculate_revenue_procedure_name};
        """
        cursor.execute(query)
        res = cursor.fetchall()
        res = res[0].values()
        res = list(res)
        print(res[0])
        return res[0]

def calculate_profit(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {calculate_profit_procedure_name};
        """
        cursor.execute(query)
        res = cursor.fetchall()
        res = res[0].values()
        res = list(res)
        print(res[0])
        return res[0]


def find_most_popular_dish(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {find_most_popular_dish_procedure_name};
        """
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        data = list(data[-1].values())
        name = data[0]
        count_of_orders = data[1]
        print(name, count_of_orders)
        return name, count_of_orders


def find_most_valuable_waiter(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {find_most_valuable_waiter_procedure_name};
        """
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        max_data = list(data[-1].values())
        max_name = max_data[0]
        max_amount = max_data[1]
        min_data = list(data[0].values())
        min_name = min_data[0]
        min_amount = min_data[1]
        return max_name, max_amount, min_name, min_amount


def find_most_unprofitable_discount(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {find_most_unprofitable_discount_procedure_name};
        """
        cursor.execute(query)
        data = cursor.fetchall()
        max_data = list(data[-1].values())
        max_name = max_data[0]
        max_amount = max_data[1]
        min_data = list(data[0].values())
        min_name = min_data[0]
        min_amount = min_data[1]
        return max_name, max_amount, min_name, min_amount


def find_most_popular_group(connection):
    with connection.cursor() as cursor:
        query = rf"""
            CALL {find_most_popular_group_procedure_name};
        """
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        data = list(data[-1].values())
        name = data[0]
        count = data[1]
        print(name, count)
        return name, count



procedures = [calculate_revenue_procedure, find_most_popular_dish_procedure, find_most_valuable_waiter_procedure,
              find_most_unprofitable_discount_procedure, calculate_profit_procedure, find_most_popular_group_procedure]

def add_procedures(connection):
    with connection.cursor() as cursor:
        for procedure in procedures:
            try:
                cursor.execute(procedure)
                print("Table created successfully")
            except Exception as ex:
                print("connection is failed", ex)

