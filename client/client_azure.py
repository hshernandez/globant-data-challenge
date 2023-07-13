import os
import pyodbc


def __get_connection():
    return pyodbc.connect(os.getenv("STRING_CONNECTION"))


def get_columns_tables(table_name):
    with __get_connection() as conn:
        cursor = conn.cursor()
        columns_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?"
        cursor.execute(columns_query,table_name)
        row = cursor.fetchone()
        columns = []
        while row: 
            columns.append(row)
            row = cursor.fetchone()
        conn.commit()
    return ','.join([x[0] for x in columns])

def insert_data(table_name, data):
    with __get_connection() as conn:
        cursor = conn.cursor()
        columns_query = get_columns_tables(table_name)
        values = "'"+data.replace("'",' ').replace('\r','').replace(',',"','")+"'"
        
        insert_query = f"INSERT INTO {table_name} ({columns_query}) VALUES ({values})"
        print(insert_query)
        cursor.execute(insert_query)
        conn.commit()
