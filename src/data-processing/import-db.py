from pathlib import Path
import mysql.connector as connector

credentials = {
    "username": "root",
    "password": ""
}

# Establish a connection with the DBMS
conn = connector.connect(user=credentials["username"],
                         passwd=credentials["password"],
                         host="localhost",
                         database="city_lines")
cursor = conn.cursor(buffered=True)
sql_queries = []

# Config the connection & the cursor
sql_queries.append("USE city_lines;")
sql_queries.append("SET GLOBAL max_allowed_packet=67108864;")

# Populate the DB using the pre-existing city-lines SQL dump
input_fp = Path("data/raw/city-lines.sql")
with open(input_fp, encoding="utf-8") as file:
    dump = file.read()
for query in dump.split(";")[:-1]:
    sql_queries.append(query)


#Execute all queries
for query in sql_queries:
  cursor.execute(query)
  conn.commit()

# Close connection
cursor.close()
conn.close()
