from pathlib import Path
import mysql.connector as connector
import pandas as pd

# Load the cleaned .csv files
# paths = [Path("data/external/transport-modes.csv"),
#          Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
#          Path("data/cleaned/world-happiness-report-cleaned.csv")]

# datasets = [pd.read_csv(path, encoding="utf-8") for path in paths]

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
conn.set_charset_collation("utf8", "utf8_general_ci")
sql_queries.append("USE city_lines;")
sql_queries.append("SET GLOBAL max_allowed_packet=67108864;")

# Prepare new tables for data insertion
# Create tables
sql_queries.append("""
CREATE TABLE IF NOT EXISTS city_country_region (
  PRIMARY KEY (city),
  city VARCHAR(100) COLLATE utf8_general_ci,
  country VARCHAR(100) COLLATE utf8_general_ci,
  region VARCHAR(100) COLLATE utf8_general_ci,
  INDEX (country),
  INDEX (region)
);
"""
)

sql_queries.append("""
CREATE TABLE IF NOT EXISTS transport_modes (
  PRIMARY KEY (id),
  id TINYINT,
  name TEXT NOT NULL COLLATE utf8_general_ci
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS mobile_phone_usage (
  PRIMARY KEY (country),
  FOREIGN KEY (country) REFERENCES city_country_region (country),
  country VARCHAR(100) COLLATE utf8_general_ci,
  num_user INT UNSIGNED,
  lines_per_hundred DECIMAL(5, 2) UNSIGNED,
  INDEX (country)
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS world_happiness_report (
  PRIMARY KEY (country),
  FOREIGN KEY (country) REFERENCES city_country_region (country),
  FOREIGN KEY (region) REFERENCES city_country_region (region),
  country VARCHAR(100) COLLATE utf8_general_ci,
  region VARCHAR(100) COLLATE utf8_general_ci,
  ladder_score DECIMAL(5,4)
);
""")

# Establish foreign key links to recently created tables
sql_queries.append("SET FOREIGN_KEY_CHECKS=0;")
sql_queries.append("""
ALTER TABLE cities
ADD FOREIGN KEY (name) REFERENCES city_country_region (city),
ADD FOREIGN KEY (country) REFERENCES city_country_region (country);
""")

sql_queries.append("""
ALTER TABLE lines
ADD FOREIGN KEY (transport_mode_id) REFERENCES transport_modes (id);
""")
sql_queries.append("SET FOREIGN_KEY_CHECKS=1;")

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