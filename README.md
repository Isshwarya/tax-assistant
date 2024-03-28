# About

A simple tax assistant web application that helps you to store and track your expenses and revenue for the purpose of filing tax.

# Solution

NOTE: To run all the commands in this documentation, please ensure to be in the workspace directory (Kindly unzip the zip file and set the current directory to the top level directory which contains api, deployment folders.)

## Context

- The application will likely to expand in the future, so a "all-batteries-included" framework like Django would help with faster development.

- The web server is containerized and deployment is supported through docker for ease-of-use of users trying out this solution.

- The order of the columns in the csv file is fixed as below:

  ```
  date,type,amount,memo
  ```

  - date takes any date format as supported by DateTime
  - type takes either Expense or Income
  - amount takes floating point number
  - memo takes text content and contains expense category or job address

  All four fields are mandatory.

- All transactions given in the csv file are stored under 'Transaction' model. Each record represents one line of data in csv file.

- Transaction model additionally uses created_at field to track when was the record added.

- For sake of simplicity and in the interest of time, transactions (expense and revenue details) are not associated with the user who added those. So the report API considers all transactions in the database irrespective of which user added those.

- SQLite DB is just used for demonstration of solution which also means requests cannot be served concurrently. This also gives persistence of data (even if it may not be needed as stated in the challenge) and allows us to smoothly transition to other RDBMs like MYSQL or PostgreSQL without having to change the views.

- csv file parsing was originally done using Python's standard csv module but that didn't support regexp based delimiters, hence moved to pandas for easier parsing.

- Versioning scheme is defined for APIs but version need not be specified in the HTTP request as there exists only one version at this moment.

## How to deploy the web server

Either of the below approaches can be used

### Using Docker image

- First, build the docker image. Set your current directory to the workspace directory (the directory that house api, deployment folders) and then run:

```console
>>>docker build -t tax_assistant_app -f deployment/Dockerfile .
```

Alternatively, the image can be readily downloaded from Dockerhub using

```console
>>> docker pull isshwarya/tax_assistant_app:latest
```

- Second, deploy the containers by running the command:

```console
docker-compose -f deployment/docker-compose.yml up -d
```

Now the web server is ready to serve the requests.

### Starting local development server

Please run the below commands:

```console
>>>cd tax_assistant
>>>source ./venv/bin/activate
>>>pip install -r requirements.txt
>>>python manage.py makemigrations; python manage.py migrate
>>>python manage.py runserver 0.0.0.0:8020
```

The tar.gz file comes preinstalled with virtualenv setup and Python 3.8.9 in it. so just activating the setup alone is enough.

## Supported APIs

- Post transactions of expenses and revenue tracked in a csv file

```
  curl -i -X POST http://0.0.0.0:8020/transactions/  -F "data=@summer-break/data.csv"
```

If the request is successful, HTTP status code 200 will be returned with no output.

If there are any issues with data format in CSV file, an error response of the below format will be
returned with HTTP status code 400.

```
{"detail":"Failed while parsing csv file. Please ensure the format is as given in the documentation"}
```

- Get the report.

```
curl -i -X GET http://0.0.0.0:8020/report/
```

This returns a JSON response with the tally of gross revenue, expenses, and net revenue (gross - expenses) as follows:

```
{
    "gross-revenue": <amount>,
    "expenses": <amount>,
    "net-revenue": <amount>
}
```

- Delete all transactions that are stored in database.

```
curl -i -X DELETE http://0.0.0.0:8020/transactions/
```

If successful, returns a response with HTTP status code 200.

## How to run the tests

The unit test cases can be executed as:

```console
python manage.py test
```

The test script that came along with the challenge bundle (summer-break/test.sh) can be executed as:

```console
isshwarya@Isshwaryas-MBP tax_assistant % bash summer-break/test.sh
{"gross-revenue":225.0,"expenses":72.93,"net-revenue":152.07}%                                                                                                                                        isshwarya@Isshwaryas-MBP tax_assistant %
```

# Shortcomings

- Lack of DB concurrency

# Future work

- Swagger support for industry standard API documentation

- Adding multi user support and defining user model. This would pave way for tracking transactions on individual user basis.

- Adding AuthN and AuthZ support

- Add Admin panel support if needed or custom frontends can be developed to achieve UI based CRUD operations.

- Ability to perform CRUD on transaction model beyond the current csv file based approach. Since Django Rest Framework is used, viewsets can be used to readily implement this.

- Ability to filter on the transactions added - Filter by date range, type (expense or income)

- Pagination support for list type queries

- Ability to delete all the transactions associated with a user, similar to how the user can add all transactions using a csv file through a single POST request. This helps with data privacy for users. Also define how long the data will be retained in DB unless explicitly deleted by the user.

- Move from SQLITE DB to other production grade databases such as PostgreSQL for better performance.
