# globant-data-challenge

This project is written in Python using Flask.
The Database is mounted in Azure Cloud as a Basic SQL Database.

# Pre-requisites per end-point

## localhost:5000/ {GET Request}

Welcome page!! This end-point is ment to check if the app is up.
Doesn't have any requisites

Example CURL: curl --location 'http://127.0.0.1:5000'

## localhost:5000/upload/<table_name>  {POST Request}

- With this end-point, the user would be able to upload a CSV file to the database. 
- It's very important to indicate the table name as a query param.
- The order of the columns in the CSV MUST BE the same as the in the database.
- The CSV MUST NOT include a header
- This request is SYNC, so the user has to wait for the server's response

Example CURL: curl --location 'http://127.0.0.1:5000/upload/employees' 
--form 'File=@"HERE_PLACE_THE_URL_OF_YOUR_LOCAL_EMPLOYEE_FILE"'

## localhost:5000/hired_quarter/<year>  {POST Request}

- With this end-point, the user would be able to consult the amount of hired people per department per job in each quarter of the specfic year
- It's very important to indicate the year as a query param.
- The specified year must be a number.
- The result in given as a JSON.

  Example CURL: curl --location 'http://127.0.0.1:5000/hired_quarter/2021'

## localhost:5000/most_hired_department/<year>  {POST Request}

- With this end-point, the user would be able to consult the list of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in the given year for all the departments, ordered by the number of employees hired (descending).
- It's very important to indicate the year as a query param.
- The specified year must be a number.
- The result in given as a JSON.

  Example CURL: curl --location 'http://127.0.0.1:5000/most_hired_department/2021'
  
