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
                         database="city_lines",
                         autocommit=True)
cursor = conn.cursor(buffered=True)
cursor.execute("USE city_lines")
cursor.execute('SET GLOBAL max_allowed_packet=67108864')

# Populate the DB using the pre-existing city-lines SQL dump
input_fp = Path("data/raw/city-lines.sql")
with open(input_fp, encoding="utf-8") as file:
    sql_query = file.read()

cursor.execute(sql_query, multi=True)

# Close connection
cursor.close()
conn.close()
