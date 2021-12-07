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

# Clean the 'cities' table
# Change data types
sql_queries.append("""
ALTER TABLE cities
MODIFY name VARCHAR(100),
MODIFY country VARCHAR(100);
""")

# Clean the 'lines' table
# Change data types
sql_queries.append("""
ALTER TABLE `lines`
MODIFY transport_mode_id TINYINT NULL;
""")

# Clean the 'station-lines' table
# Change data types
sql_query = """
ALTER TABLE station_lines
MODIFY created_at TIMESTAMP NULL,
MODIFY updated_at TIMESTAMP NULL;
"""
sql_queries.append(sql_query)

# Clean the 'tracks' table
# Change data types
sql_query = """
ALTER TABLE tracks
MODIFY buildstart SMALLINT UNSIGNED NULL,
MODIFY opening SMALLINT UNSIGNED NULL,
MODIFY closure SMALLINT UNSIGNED NULL;
 """
sql_queries.append(sql_query)

# Clean illogical values & fix null duplicacy
sql_query = """
UPDATE tracks
   SET buildstart = NULL
 WHERE buildstart <= 1800 OR buildstart >= 2021;

 UPDATE tracks
   SET opening = NULL
 WHERE opening <= 1800 OR opening >= 2021;

UPDATE tracks
   SET closure = NULL
 WHERE closure <= 1800 OR closure >= 2021;

 UPDATE tracks
    SET length = NULL
  WHERE length <= 0;
 """
for query in sql_query.split(";")[:-1]:
  if query != " ":
    sql_queries.append(query)

#Execute all queries
for query in sql_queries:
  cursor.execute(query)
  conn.commit()

# Commit & close connection
cursor.close()
conn.close()
