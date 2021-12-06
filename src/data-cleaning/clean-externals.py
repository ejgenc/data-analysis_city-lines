from pathlib import Path 
import pandas as pd

targets = [Path("data/externals/transport-modes.csv"),
           Path("data/externals/mobile-phone-usage.csv"),
           Path("data/externals/world-happiness-report.csv")]
           
datasets = [pd.read_csv(target, encoding="utf-8") for target in targets]