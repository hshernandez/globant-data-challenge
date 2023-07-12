from flask import Flask, request
import csv

app = Flask(__name__)

#Defualt route just to make sure API is up!!
@app.route("/")
def home():
    return "Hello, Flask!"



# Endpoint to receive CSV files
@app.route('/upload', methods=['POST'])
def upload_csv():
    csv_files = request.files.getlist('file')  # assuming the files are uploaded as 'file' in the request form data

    for csv_file in csv_files:
        # Implement CSV parsing and data extraction logic here
        data = parse_csv(csv_file)

        # TODO: Validate the data

        # TODO: Store the extracted data in memory or temporary storage

    #Return message
    return 'CSV files uploaded successfully!'

def parse_csv(csv_file):
    data = []
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Process each row as per your requirements
        data.append(row)
    return data


if __name__ == '__main__':
    app.run()