from pathlib import Path
import mysql.connector as connector
import pandas as pd

# Load the cleaned .csv files
paths = [Path("data/external/transport-modes.csv"),
         Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
         Path("data/cleaned/world-happiness-report-cleaned.csv")]

datasets = [pd.read_csv(path, encoding="utf-8") for path in paths]

# Establish a connection with the DBMS
credentials = {
    "username": "root",
    "password": ""
}

conn = connector.connect(user=credentials["username"],
                         passwd=credentials["password"],
                         host="localhost",
                         database="city_lines")
cursor = conn.cursor(buffered=True)
sql_queries = []

# Config the connection & the cursor
sql_queries.append("USE city_lines;")
sql_queries.append("SET GLOBAL max_allowed_packet=67108864;")

# Prepare new tables for data insertion
# Create tables
sql_queries.append("""
CREATE TABLE IF NOT EXISTS transport_modes (
    PRIMARY KEY (id),
    id TINYINT,
    name TEXT NON-NULL
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS
""")



# Establish foreign key links to the table


#Execute all SQL queries
for query in sql_queries:
  cursor.execute(query)
  conn.commit()

# # Populate the tables
# datasets[0].to_sql(name="transport_modes",
#                    con=conn,
#                    if_exits="append",
#                    index=False,
#                    method=None)

# Close connection
cursor.close()
conn.close()