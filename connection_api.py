import pymysql
from config_db import *

def connect_db():
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected to db")
        return connection

    except Exception as ex:
        print("connection is failed", ex)


def create_tables(connection, tables):
    try:
        with connection.cursor() as cursor:
            for table in tables:
                cursor.execute(table)
                print("Table created successfully")
    except Exception as ex:
        print("connection is failed", ex)

