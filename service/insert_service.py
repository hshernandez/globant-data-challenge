from client.client_azure import insert_data


def upload_csv(table_name, csv_file):
    csv_file = csv_file.read().decode('ascii')
    if csv_file == '':
        return 'CSV file is empty'

    data = csv_file.split('\n')
    
    for x in data:
        if x == '':
            continue
        insert_data(table_name, x)
   
    #Return message
    return 'CSV files uploaded successfully!'
