import psycopg2

# server
dbname = "sample_iot"
username = "sample_iotuser"
password = "sample_iotpwd"
host = "localhost"
port = "5432"

# function that returns the database connections


def databaseconn():
    conn = psycopg2.connect(dbname=dbname, user=username,
                            password=password, host=host, port=port)
    return conn
