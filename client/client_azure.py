import os
import pyodbc


def __get_connection():
    """
    Retrieves a connection object to the database.

    Returns:
        pyodbc.Connection: A connection object to the database.


    Notes:
        - This function retrieves a connection object to the database using the connection string obtained from the environment variable 'STRING_CONNECTION'.
        - The connection string should be stored in the 'STRING_CONNECTION' environment variable.
        - The function utilizes the pyodbc library to establish the database connection.

    Example:
        conn = __get_connection()
        This will retrieve a connection object to the database and store it in the 'conn' variable for further use.

    """
    return pyodbc.connect(os.getenv("STRING_CONNECTION"))


def get_columns_tables(table_name):
    """
    Retrieves the column names of the specified table and returns them as a comma-separated string.

    Args:
        table_name (str): The name of the table for which the column names will be retrieved.

    Returns:
        str: A comma-separated string containing the column names of the specified table.


    Notes:
        - This function queries the database to fetch the column names of the specified table.
        - It utilizes the __get_connection function to establish a connection to the database.
        - The column names are retrieved from the INFORMATION_SCHEMA.COLUMNS table using the specified table name.
        - The column names are returned as a comma-separated string.

    Example:
        columns = get_columns_tables("employees")
        This will retrieve the column names of the "employees" table and store them in the 'columns' variable as a comma-separated string.

    """
    with __get_connection() as conn:
        cursor = conn.cursor()
        columns_query = (
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?"
        )
        cursor.execute(columns_query, table_name)
        row = cursor.fetchone()
        columns = []
        while row:
            columns.append(row)
            row = cursor.fetchone()
        conn.commit()
    return [x[0] for x in columns]


def insert_data(table_name, data):
    """
    Inserts the provided data into the specified table in the database.

    Args:
        table_name (str): The name of the table to which the data will be inserted.
        data (str): The data to be inserted into the specified table.

    Returns:
        None


    Notes:
        - This function inserts the provided data into the specified table in the database.
        - It utilizes the __get_connection function to establish a connection to the database.
        - The column names of the specified table are retrieved using the get_columns_tables function.
        - The data is inserted into the table using an INSERT query constructed dynamically based on the table name, column names, and provided data.
        - The data should be provided as a comma-separated string with each value enclosed in single quotes.

    """
    with __get_connection() as conn:
        cursor = conn.cursor()
        columns_query = get_columns_tables(table_name)

        insert_query = f"INSERT INTO {table_name} ({','.join(columns_query)}) VALUES ({','.join(['?' for _ in columns_query])})"
        cursor.executemany(insert_query, data)
        conn.commit()


def hired_quarter(year):
    """
    Retrieves the hired data for each department and job during each quarter of the specified year.

    Args:
        year (int): The year for which the hired data will be retrieved.

    Returns:
        list: A list of tuples containing the hired data for each department and job during each quarter of the specified year.


    Notes:
        - This function queries the database to fetch the hired data for each department and job during each quarter of the specified year.
        - It utilizes the __get_connection function to establish a connection to the database.
        - The hired data includes the department name, job title, and the number of hires in each quarter.
        - The result is returned as a list of tuples, where each tuple represents the hired data for a specific department and job.
        - Each tuple contains the department name, job title, and the number of hires in each of the four quarters.

    Example:
        hired_data = hired_quarter(2022)
        This will retrieve the hired data for each department and job during each quarter of the year 2022 and store it in the 'hired_data' variable as a list of tuples.

    """
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

        cursor.execute(query_result, year)
        return cursor.fetchall()


def most_hired_departments(year):
    """
    Retrieves the departments that have hired more employees than the average for the specified year.

    Args:
        year (int): The year for which the most hired departments will be retrieved.

    Returns:
        list: A list of tuples containing the departments that have hired more employees than the average for the specified year.


    Notes:
        - This function queries the database to fetch the departments that have hired more employees than the average for the specified year.
        - It utilizes the __get_connection function to establish a connection to the database.
        - The result includes the department ID, department name, and the count of hires for each department.
        - The result is returned as a list of tuples, where each tuple represents a department that has hired more employees than the average.
        - Each tuple contains the department ID, department name, and the count of hires for that department.

    Example:
        hired_departments = most_hired_departments(2022)
        This will retrieve the departments that have hired more employees than the average for the year 2022 and store them in the 'hired_departments' variable as a list of tuples.

    """
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

        cursor.execute(query_result, year)
        return cursor.fetchall()
