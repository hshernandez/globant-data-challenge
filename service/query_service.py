from client.client_azure import hired_quarter
from client.client_azure import most_hired_departments

def get_hired_quarter(year):
    
    try:
        clear_year = int(year)
        return [__mapper_hired_quarter(x) for x in hired_quarter(clear_year)]
    except ValueError:
        return 'The parameter year must a valid number'
    except Exception as e:
        return e

def get_most_hired_departments(year):
    try:
        clear_year = int(year)
        return [__mapper_most_hired_departments(x) for x in most_hired_departments(clear_year)]
    except ValueError:
        return 'The parameter year must a valid number'
    except Exception as e:
        return e


def __mapper_hired_quarter(tuple):
    return {
        'department':tuple[0],
        'job':tuple[1],
        'Q1': tuple[2],
        'Q2': tuple[3],
        'Q3': tuple[4],
        'Q4': tuple[5],
    }

def __mapper_most_hired_departments(tuple):
    return {
        'id':tuple[0],
        'name':tuple[1],
        'hired': tuple[2]
    }
    
    