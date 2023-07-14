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
        cursor.execute(insert_query)
        conn.commit()


def hired_quarter(year):
    with __get_connection() as conn:
        cursor = conn.cursor()
        
        query_result = f"""
            SELECT  
                    department 
                    ,job
                    ,[1] AS Q1, [2] AS Q2, [3] AS Q3, [4] AS Q4
                FROM (
                    SELECT
                        DE.name as department
                        ,JB.title as job
                        ,DATEPART(QUARTER, date_time) as quarter
                    FROM [dbo].[employees] EM
                    INNER JOIN [dbo].[departments] DE 
                        ON EM.department_id = DE.id
                    INNER JOIN [dbo].[jobs] JB
                        ON EM.job_id = JB.id
                    WHERE YEAR(date_time) = ?
                ) AS HIRED

                PIVOT
                (
                COUNT(quarter)
                FOR quarter IN ([1], [2], [3], [4])
                ) AS PivotTable
                ORDER BY department, job
            """
        
        cursor.execute(query_result,year)
        return cursor.fetchall() 
        
def most_hired_departments(year):
    with __get_connection() as conn:
        cursor = conn.cursor()
        query_result = f"""
            SELECT
                    de.id
                    ,de.name
                    ,count(*) as hired
                FROM [dbo].[employees] EM
                INNER JOIN [dbo].[departments] DE 
                    ON EM.department_id = DE.id
                    AND YEAR(EM.date_time) = ?
                GROUP BY de.id,de.name
                HAVING count(*) > (SELECT AVG(count.count_per_department) 
                                FROM (
                                        SELECT COUNT(*) as count_per_department
                                            FROM [dbo].[employees] EM
                                            INNER JOIN [dbo].[departments] DE 
                                                ON EM.department_id = DE.id
                                                AND YEAR(EM.date_time) = 2021
                                            GROUP BY de.id,de.name) AS count)
                ORDER BY hired DESC
            """
        
        cursor.execute(query_result,year)
        return cursor.fetchall() 

