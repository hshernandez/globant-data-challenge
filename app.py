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

    if "File" not in request.files:
        return "This method needs a csv file to operate. Please select a file", 400

    # assuming the files are uploaded as 'File' in the request form data.
    # And there's only one file
    csv_files = request.files.getlist("File")[0]

    return insert_data.upload_csv(table_name, csv_files)


@app.route("/hired_quarter/<year>")
def hired_year_quarter(year):
    return query_data.get_hired_quarter(year)


@app.route("/most_hired_department/<year>")
def most_hired_year(year):
    return query_data.get_most_hired_departments(year)


if __name__ == "__main__":
    load_dotenv()
    app.run()
