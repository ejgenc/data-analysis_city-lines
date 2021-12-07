from pathlib import Path 
import pandas as pd

targets = [Path("data/external/mobile-phone-usage.csv"),
           Path("data/external/world-happiness-report.csv")]
           
datasets = [pd.read_csv(target, encoding="utf-8") for target in targets]

# Clean 'mobile-phone-usage.csv'
datasets[0] = (datasets[0]
               .drop(["pop2021"], axis=1)
               .rename({"numUsers": "num_users",
                        "linesPer100": "lines_per_hundred"}, axis=1))

# Clean 'world-happiness-report.csv'
datasets[1] = (datasets[1]
               .drop([column for column in list(datasets[1].columns) if
                      column not in
                      ["Country name", "Regional indicator", "Ladder score"]],
                      axis=1)
               .rename({"Country name": "country",
                        "Regional indicator": "regional_indicator",
                        "Ladder score": "ladder_score"}, axis=1))

# Export data 
paths = [Path("data/cleaned/mobile-phone-usage-cleaned.csv"),
         Path("data/cleaned/world-happiness-report-cleaned.csv")]

for dataset, path in zip(datasets, paths):
       dataset.to_csv(path, encoding="utf-8", index=False)
