import pandas as pd
import numpy as np
# sudo /usr/bin/python3 -m pip install PyGithub
import subprocess

url = "https://raw.githubusercontent.com/ia-lozano/mir4_data/refs/heads/master/testing/nft_list_2025-06-22.csv"
df = pd.read_csv(url)

print(df.head())

df_clean = df[["power", "price"]]

print(df_clean.head())

df_clean.to_csv

commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", "updating"],
    ["git", "push", "-u", "origin", "master"]
]

for cmd in commands:
    subprocess.run(cmd)




