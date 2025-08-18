import pandas as pd
import re
import unicodedata
import subprocess

df = pd.read_csv("https://raw.githubusercontent.com/ia-lozano/mir4_data/refs/heads/master/raw/nft_list_2025-06-22.csv",
                 parse_dates=["date"])

# Removiendo caracteres que no sean ASCII
def normalize_name(name:str) -> str:
    # Normalizando catacteris a ASCII
    name = unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore').decode('ASCII')
    
    # Removiendo caracteres no alfanuméricos o espacios
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)

    # Removiendo espacios en blanco
    return name.strip() if name else 'name'


df['name'] = df['name'].apply(normalize_name)

# Convert score to integer, invalid -> NaN
df['power'] = pd.to_numeric(df['power'], errors='coerce')

# Convert date to datetime, invalid -> NaT
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert price to integer, invalid -> NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Convert level to integer, invalid -> NaN
df['level'] = pd.to_numeric(df['level'], errors='coerce')

# Check for any invalid rows
invalid_rows = df[df['power'].isna() | df['date'].isna()]
print("invalid rows: ", invalid_rows)

print(df.head())
print(df.dtypes)

df.to_csv("processed/data.csv", index=False)

commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", "updating"],
    ["git", "push", "-u", "origin", "master"]
]

for cmd in commands:
    subprocess.run(cmd)