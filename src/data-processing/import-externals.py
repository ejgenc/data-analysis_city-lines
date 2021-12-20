from pathlib import Path
import mysql.connector as connector
import sqlalchemy
import pandas as pd

# Load the cleaned .csv files
paths = [Path("data/external/transport-modes.csv"),
         Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
         Path("data/cleaned/world-happiness-report-cleaned.csv"),
         Path("data/external/education-index.csv"),
         Path("data/cleaned/freedom-of-speech-cleaned.csv")]

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
conn.set_charset_collation("utf8", "utf8_general_ci")
sql_queries.append("USE city_lines;")
sql_queries.append("SET GLOBAL max_allowed_packet=67108864;")

# Prepare new tables for data insertion
# Create tables
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
  country VARCHAR(100) COLLATE utf8_general_ci,
  num_users INT UNSIGNED,
  lines_per_hundred DECIMAL(5, 2) UNSIGNED,
  INDEX (country)
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS world_happiness_report (
  PRIMARY KEY (country),
  country VARCHAR(100) COLLATE utf8_general_ci,
  region VARCHAR(100) COLLATE utf8_general_ci,
  ladder_score DECIMAL(5,4)
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS education_levels (
  PRIMARY KEY (country),
  country varchar(100) COLLATE utf8_general_ci,
  rank INT UNSIGNED DEFAULT NULL,
  education_index DECIMAL(4,2) DEFAULT NUll
);
""")

sql_queries.append("""
CREATE TABLE IF NOT EXISTS freedom_of_speech (
  PRIMARY KEY (country),
  country VARCHAR(100) COLLATE utf8_general_ci,
  index_score DECIMAL(4,2),
  rank TINYINT UNSIGNED
);
""")

# Establish foreign key links to recently created tables
sql_queries.append("SET FOREIGN_KEY_CHECKS=0;")
sql_queries.append("""
ALTER TABLE cities
ADD FOREIGN KEY (country) REFERENCES mobile_phone_usage (country),
ADD FOREIGN KEY (country) REFERENCES world_happiness_report (country),
ADD FOREIGN KEY (country) REFERENCES education_levels (country),
ADD FOREIGN KEY (country) REFERENCES freedom_of_speech (country);
""")

sql_queries.append("""
ALTER TABLE `lines`
ADD FOREIGN KEY (transport_mode_id) REFERENCES transport_modes (id);
""")
sql_queries.append("SET FOREIGN_KEY_CHECKS=1;")

#Execute all SQL queries
for query in sql_queries:
  cursor.execute(query)
  conn.commit()

# Populate the tables
write_engine = sqlalchemy.create_engine("mysql+pymysql://root:@localhost/city_lines?charset=utf8")

table_names = ["transport_modes", "mobile_phone_usage",
               "world_happiness_report", "education_levels",
               "freedom_of_speech"]
for dataset, table_name in zip(datasets, table_names):
  dataset.to_sql(name=table_name,
                 con=write_engine,
                 if_exists="append",
                 index=False,
                 method=None)

# Close connection
cursor.close()
conn.close()