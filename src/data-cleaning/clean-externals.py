from pathlib import Path 
import pandas as pd
import mysql.connector as connector

targets = [Path("data/external/mobile-phone-usage.csv"),
           Path("data/external/world-happiness-report.csv"),
           Path("data/external/freedom-of-speech.csv")]
           
datasets = [pd.read_csv(target, encoding="utf-8") for target in targets]

# Establish a connection with the DBMS
credentials = {
    "username": "root",
    "password": ""
}

conn = connector.connect(user=credentials["username"],
                         passwd=credentials["password"],
                         host="localhost",
                         database="city_lines")

# Config the connection & the cursor
conn.set_charset_collation("utf8", "utf8_general_ci")

# Get a list of countries that exist in city lines
query = """
SELECT DISTINCT country
  FROM cities
  ORDER BY country ASC;
"""
countries = pd.read_sql(query, conn)

# Clean 'mobile-phone-usage.csv'
datasets[0] = (datasets[0]
               .drop(["pop2021"], axis=1)
               .rename({"numUsers": "num_users",
                        "linesPer100": "lines_per_hundred"}, axis=1)
               .loc[datasets[0]["country"].isin(countries["country"]), :])

# Clean 'world-happiness-report.csv'
datasets[1] = (datasets[1]
               .drop([column for column in list(datasets[1].columns) if
                      column not in
                      ["Country name", "Regional indicator", "Ladder score"]],
                      axis=1)
               .rename({"Country name": "country",
                        "Regional indicator": "region",
                        "Ladder score": "ladder_score"}, axis=1))        
datasets[1] = datasets[1].loc[datasets[1]["country"].isin(countries["country"]), :]

# Clean 'freedom-of-speech.csv'
datasets[2] = (datasets[2]
               .drop([column for column in list(datasets[2].columns) if
                      column not in
                      ["Country Name", "Indicator", "2021"]], axis=1))

index_mask = datasets[2].loc[:, "Indicator"] == "Press Freedom Index"
dataset_index = (datasets[2].loc[index_mask, :]
                 .drop("Indicator", axis=1)
                 .rename({"2021": "index_score"}, axis=1))
dataset_rank = (datasets[2].loc[~index_mask, :]
                .drop("Indicator", axis=1)
                .rename({"2021": "rank"}, axis=1))
datasets[2] = ((pd.merge(dataset_index, dataset_rank,
                        how="left", on="Country Name"))
               .rename({"Country Name": "country"}, axis=1))
datasets[2] = datasets[2].loc[datasets[2]["country"].isin(countries["country"]), :]

# Export data 
paths = [Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
         Path("data/cleaned/world-happiness-report-cleaned.csv"),
         Path("data/cleaned/freedom-of-speech-cleaned.csv")]

for dataset, path in zip(datasets, paths):
       dataset.to_csv(path, encoding="utf-8", index=False)
