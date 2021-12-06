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

# Clean the 'station-lines' table
# Change data types
sql_query = """
ALTER TABLE station_lines
MODIFY created_at TIMESTAMP NULL,
MODIFY updated_at TIMESTAMP NULL;
"""
cursor.execute(sql_query)

# Clean the 'tracks' table
# Change data types
sql_query = """
ALTER TABLE tracks
MODIFY buildstart SMALLINT UNSIGNED NULL,
MODIFY opening SMALLINT UNSIGNED NULL,
MODIFY closure SMALLINT UNSIGNED NULL;
 """
cursor.execute(sql_query)

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
cursor.execute(sql_query, multi=True)

# Commit & close connection
cursor.close()
conn.close()
