from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
import pyodbc
import csv

app = Flask(__name__)
CORS(app)

#Defualt route just to make sure API is up!!
@app.route("/")
def home():
    print('HELLO WORLD')
    return "Hello, Flask!"

def get_columns_tables(table_name):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        columns_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
        cursor.execute(columns_query)
        row = cursor.fetchone()
        columns = []
        while row: 
            columns.append(row)
            row = cursor.fetchone()
        conn.commit()
    return ','.join([x[0] for x in columns])


# Endpoint to receive CSV files
@app.route('/upload/<table_name>', methods=['POST'])
def upload_csv(table_name):
    print(request.files)
    if 'File' not in request.files:
        return 'This method needs a csv file to operate. Please select a file', 400
    
    #validating file type
    #content_type = request.headers.get('Content-Type')
    #if (content_type != 'text/csv'):
    #    return 'Not valid file type. It must be a csv', 400
        
    # assuming the files are uploaded as 'File' in the request form data
    csv_files = request.files.getlist('File')
    csv_file = csv_files[0].read().decode('ascii')
    
    data = csv_file.split('\n')
    # TODO: Validate the data
    for x in data:
        print(x)
        insert_data(table_name, x)
   
    #Return message
    return 'CSV files uploaded successfully!'


def parse_csv(csv_file):
    data = []
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Process each row as per your requirements
        data.append(row)
    return data


conn_str = (
    "driver={ODBC Driver 17 for SQL Server};"
    "SERVER=globant-challenge.database.windows.net;"
    "DATABASE=globant-challenge;"
    "UID=admin-login;"
    "PWD=Hugosantiago98;"
)

def insert_data(table_name, data):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        columns_query = get_columns_tables(table_name)
        values = "'"+data.replace("'",' ').replace('\r','').replace(',',"','")+"'"
        
        insert_query = f"INSERT INTO {table_name} ({columns_query}) VALUES ({values})"
        print(insert_query)
        cursor.execute(insert_query)
        conn.commit()




if __name__ == '__main__':
    load_dotenv()
    app.run()