from client.client_azure import hired_quarter
from client.client_azure import most_hired_departments


def get_hired_quarter(year):
    """
    Retrieves the hired data for the specified year and returns it.

    Args:
        year (int): The year for which the hired data will be retrieved.

    Returns:
        JSON: The hired data for the specified year, represented as a list of JSON values.

    Raises:
        ValueError: If the year parameter is not a valid number.
        Exception: If an unexpected error occurs during the execution.

    Notes:
        - This function internally calls the hired_quarter function to fetch the hired data for the specified year.
        - The hired data represents the number of employees hired each quarter of the specified year.
        - The result is returned as a list of JSON, where each JSON represents the data for a quarter.

    Example:
        hired_data = get_hired_quarter(2022)
        This will retrieve the hired data for the year 2022 and store it in the 'hired_data' variable as a list of JSON.

    """
    try:
        clear_year = int(year)
        return [__mapper_hired_quarter(x) for x in hired_quarter(clear_year)]
    except ValueError:
        return "The parameter year must a valid number"
    except Exception as e:
        return e


def get_most_hired_departments(year):
    """
    Retrieves the most hired departments for the specified year and returns the result.

    Args:
        year (int): The year for which the most hired departments will be retrieved.

    Returns:
        list: The most hired departments for the specified year, represented as a JSON.

    Raises:
        ValueError: If the year parameter is not a valid number.
        Exception: If an unexpected error occurs during the execution.

    Notes:
        - This function internally calls the most_hired_departments function to fetch the most hired departments for the specified year.
        - The result includes the department names and the corresponding number of hires.
        - The departments are ranked based on the number of hires, with the highest number appearing first.
        - The result is returned as a JSON, where each dictionary represents a department and its hire count.
        - Each dictionary contains the 'department' and 'hires' keys, representing the department name and the number of hires respectively.

    Example:
        most_hired = get_most_hired_departments(2022)
        This will retrieve the most hired departments for the year 2022 and store the result in the 'most_hired' variable as a JSON.

    """
    try:
        clear_year = int(year)
        return [
            __mapper_most_hired_departments(x)
            for x in most_hired_departments(clear_year)
        ]
    except ValueError:
        return "The parameter year must a valid number"
    except Exception as e:
        return e


def __mapper_hired_quarter(tuple):
    return {
        "department": tuple[0],
        "job": tuple[1],
        "Q1": tuple[2],
        "Q2": tuple[3],
        "Q3": tuple[4],
        "Q4": tuple[5],
    }


def __mapper_most_hired_departments(tuple):
    return {"id": tuple[0], "name": tuple[1], "hired": tuple[2]}
