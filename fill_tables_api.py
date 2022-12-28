import pymysql
import random
import table
from config_tables import *
from procedures_db import *



def add_ingredients(connection, name=None, cost_price=None, measuring_unit=None, count=10):
    with connection.cursor() as cursor:

        for i in range(1, count + 1):
            name = f"\'ingredient{i}\'"
            cost_price = i
            measuring_unit = "\'gram\'"
            fields = g_table_dict[ingredients_table_name].get_fields_to_string()
            insert_query = f"INSERT INTO `{ingredients_table_name}` ({fields}) " \
                           f"VALUES ({name}, {cost_price}, {measuring_unit});"
            cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[ingredients_table_name].increase_count_of_rows(count)


def add_dishes(connection, count=10):
    with connection.cursor() as cursor:
        for i in range(1, count + 1):
            name = f"\'dish{i}\'"
            group_id = i
            markup = i * 100
            cost_price = 0
            price = cost_price + markup
            fields = g_table_dict[dishes_table_name].get_fields_to_string()
            insert_query = f"INSERT INTO `{dishes_table_name}` ({fields}) " \
                           f"VALUES ({name}, {group_id}, {cost_price}, {price}, {markup});"
            cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[dishes_table_name].increase_count_of_rows(count)


def add_groups(connection, count=10):
        with connection.cursor() as cursor:
            for i in range(1, count + 1):
                name = f"\'group{i}\'"
                fields = g_table_dict[groups_table_name].get_fields_to_string()
                insert_query = f"INSERT INTO `{groups_table_name}` ({fields}) " \
                               f"VALUES ({name});"
                cursor.execute(insert_query)
            try:
                connection.commit()
            except Exception as ex:
                print("connection is failed", ex)
            g_table_dict[groups_table_name].increase_count_of_rows(count)


def add_dishes_composition(connection, quantity=10, count_of_dishes=10, count_of_ingredients=10):
        with connection.cursor() as cursor:
            for i in range(1, count_of_dishes + 1):
                dish_id = i
                for j in range(1, count_of_ingredients + 1):
                    ingredient_id = j
                    cost_price = calculate_dishes_composition_cost_price(cursor, ingredient_id) * quantity
                    fields = g_table_dict[dishes_composition_table_name].get_fields_to_string()
                    insert_query = f"INSERT INTO `{dishes_composition_table_name}` ({fields}) " \
                                   f"VALUES ({dish_id}, {ingredient_id}, {quantity}, {cost_price});"
                    cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[dishes_composition_table_name].increase_count_of_rows(count_of_dishes * count_of_ingredients)


def add_waiters(connection, count=10):
        with connection.cursor() as cursor:
            for i in range(1, count + 1):
                name = f"\'waiter{i}\'"
                fields = g_table_dict[waiters_table_name].get_fields_to_string()
                insert_query = f"INSERT INTO `{waiters_table_name}` ({fields}) " \
                               f"VALUES ({name});"
                cursor.execute(insert_query)
            try:
                connection.commit()
            except Exception as ex:
                print("connection is failed", ex)
            g_table_dict[waiters_table_name].increase_count_of_rows(count)


def add_discounts(connection, name=None, discount_percentage=None, count=10):
    with connection.cursor() as cursor:
        for i in range(1, count + 1):
            name = f"\'discount{i}\'"
            discount_percentage = i
            fields = g_table_dict[discounts_table_name].get_fields_to_string()
            insert_query = f"INSERT INTO `{discounts_table_name}` ({fields}) " \
                           f"VALUES ({name}, {discount_percentage});"
            cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[discounts_table_name].increase_count_of_rows(count)

def add_orders(connection, count=10):
    with connection.cursor() as cursor:
        for i in range(1, count + 1):
            waiter_id = i
            discount_id = i
            cost_price = 0
            amount = 0
            total_amount = 0
            fields = g_table_dict[orders_table_name].get_fields_to_string()
            insert_query = f"INSERT INTO `{orders_table_name}` ({fields}) " \
                           f"VALUES ({waiter_id}, {discount_id}, {cost_price}, {amount}, {total_amount});"
            cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[orders_table_name].increase_count_of_rows(count)

def add_order_units(connection, quantity=2, count=10):
    with connection.cursor() as cursor:
        for i in range(1, count + 1):
            order_id = i
            dish_id = i
            if dish_id == 7:
                dish_id = 8
            cost_price = calculate_orders_unit_cost_price(cursor, dish_id) * quantity
            amount = calculate_orders_unit_price(cursor, dish_id) * quantity
            fields = g_table_dict[order_units_table_name].get_fields_to_string()
            insert_query = f"INSERT INTO `{order_units_table_name}` ({fields}) " \
                           f"VALUES ({order_id}, {dish_id}, {cost_price}, {quantity}, {amount});"
            cursor.execute(insert_query)
        try:
            connection.commit()
        except Exception as ex:
            print("connection is failed", ex)
        g_table_dict[order_units_table_name].increase_count_of_rows(count)
