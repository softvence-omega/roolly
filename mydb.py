""" 
Install MySql on your Computer
- pip install mysql
- pip install mysql-connector
- pip install mysql-connector-python

"""

import mysql.connector

database = mysql.connector.connect(
    database='crm',  
    host='localhost',
    user='root',
    password='password123',
)

# prepare a cursor object
cursorObject = database.cursor() 

# create a database (this should be done only once, remove if already created)
cursorObject.execute("CREATE DATABASE IF NOT EXISTS crm")

print("All Done!")
