# Drop DB if it already exists

import mysql.connector as connector

credentials = {
    "username": "root",
    "password": ""
}

# Establish a connection with the DBMS
conn = connector.connect(user=credentials["username"],
                         passwd=credentials["password"],
                         host="localhost")
cursor = conn.cursor()

# Drop the database
sql_query = """
DROP DATABASE IF EXISTS city_lines
"""
cursor.execute(sql_query)

cursor.close()
conn.close()
