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

# Create the DB
sql_query = """
CREATE DATABASE IF NOT EXISTS city_lines;
"""
cursor.execute(sql_query)

cursor.close()
conn.close()
