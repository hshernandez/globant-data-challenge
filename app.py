from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
import service.insert_service as insert_data
import service.query_service as query_data

app = Flask(__name__)
CORS(app)


# Defualt route just to make sure API is up!!
@app.route("/")
def home():
    return "Hello, I'm Hugo Santiago Hernandez Limas :)"


@app.route("/upload/<table_name>", methods=["POST"])
def upload_csv(table_name):
    """
    Uploads a CSV file to the specified table in the database.

    Args:
        table_name (str): The name of the table in the database to which the CSV data will be uploaded.

    Returns:
        str: A message indicating the success or failure of the operation.


    Notes:
        - This endpoint expects a single CSV file to be uploaded as 'File' in the request form data.
        - The uploaded CSV file should contain the data to be inserted into the specified table.
        - The CSV file should not have a header row that defines the column names.

    Example:
        A POST request to '/upload/employees' with the CSV file uploaded as 'File' will insert the data
        from the CSV file into the 'employees' table in the database.

    """
    if "File" not in request.files:
        return "This method needs a csv file to operate. Please select a file", 400

    # assuming the files are uploaded as 'File' in the request form data.
    # And there's only one file
    csv_files = request.files.getlist("File")[0]

    return insert_data.upload_csv(table_name, csv_files)


@app.route("/hired_quarter/<year>")
def hired_year_quarter(year):
    """
    Retrieves the hired data for the specified year divided by quarteds and returns it.

    Args:
        year (int): The year for which the hired data will be retrieved.

    Returns:
        JSON: The hired data for the specified year.

    Notes:
        - This endpoint expects the year to be provided as a parameter in the URL.
        - The function queries the database to fetch the hired data for the specified year.
        - The hired data represents the number of employees hired each quarter of the specified year.
        - The data is retreive in JSON format

    Example:
        A GET request to '/hired_quarter/2022' will retrieve the hired data for the year 2022.

    """

    return query_data.get_hired_quarter(year)


@app.route("/most_hired_department/<year>")
def most_hired_year(year):
    """
    Retrieves the most hired departments for the specified year and returns the result.

    Args:
        year (int): The year for which the most hired departments will be retrieved.

    Returns:
        JSON: The most hired departments for the specified year.

    Notes:
        - This endpoint expects the year to be provided as a parameter in the URL.
        - The function queries the database to fetch the most hired departments for the specified year.
        - The result includes the department id, names and the corresponding number of hires.
        - The departments are ranked based on the number of hires, with the highest number appearing first.

    Example:
        A GET request to '/most_hired_department/2022' will retrieve the most hired departments for the year 2022.

    """
    return query_data.get_most_hired_departments(year)


if __name__ == "__main__":
    load_dotenv()
    app.run()
