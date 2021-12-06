import mysql.connector as connector

credentials = {
    "username": "root",
    "password": ""
}

# Establish a connection with the DBMS
conn = connector.connect(user=credentials["username"],
                         passwd=credentials["password"],
                         host="localhost")
cursor = conn.cursor(buffered=True)
sql_queries = []

# Create the DB
sql_queries.append("CREATE DATABASE IF NOT EXISTS city_lines;")

for query in sql_queries:
  cursor.execute(query)
  conn.commit()

# Close connection
cursor.close()
conn.close()
