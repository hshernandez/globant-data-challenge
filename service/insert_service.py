from client.client_azure import insert_data


def upload_csv(table_name, csv_file):
    """
    Uploads a CSV file to the specified table in the database.

    Args:
        table_name (str): The name of the table to which the CSV data will be uploaded.
        csv_file (werkzeug.datastructures.FileStorage): The CSV file to be uploaded.

    Returns:
        str: A message indicating the success or failure of the operation.


    Notes:
        - This function uploads the provided CSV file to the specified table in the database.
        - It expects the CSV file to be provided as a werkzeug.datastructures.FileStorage object.
        - The CSV file is read, decoded as ASCII, and split into lines.
        - The data lines are cleaned and processed using the __clean_line function.
        - The cleaned data is then inserted into the specified table using the insert_data function.
        - If the CSV file is empty, the function returns a message indicating that the file is empty.
        - Upon successful upload, the function returns a message indicating the successful upload of the CSV file.

    Example:
        message = upload_csv("employees", csv_file)
        This will upload the provided 'csv_file' to the 'employees' table and store a message indicating the success or failure of the operation in the 'message' variable.

    """
    csv_file = csv_file.read().decode("ascii")
    if csv_file == "":
        return "CSV file is empty"

    data = csv_file.split("\n")
    insert_data(table_name, [__clean_line(x) for x in data])
    # Return message
    return "CSV files uploaded successfully!"


def __clean_line(line):
    return [
        x.replace("\r", "").replace("\n", "").replace("\t", "") for x in line.split(",")
    ]
