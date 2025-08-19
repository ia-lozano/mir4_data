import pandas as pd
import numpy as np
# /usr/bin/python3 -m pip install scipy
from scipy import stats
import subprocess

url = 'https://raw.githubusercontent.com/ia-lozano/mir4_data/refs/heads/master/processed/data.csv'
dataset = pd.read_csv(url)

# Segmentando por rangos de 50k en 50k
df100 = dataset[(dataset["power"] >= 10000) & (dataset["power"] <= 150000)]
df150 = dataset[(dataset["power"] >= 150001) & (dataset["power"] <= 200000)]
df200 = dataset[(dataset["power"] >= 200001) & (dataset["power"] <= 250000)]
df250 = dataset[(dataset["power"] >= 250001) & (dataset["power"] <= 300000)]
df300 = dataset[(dataset["power"] >= 300001) & (dataset["power"] <= 350000)]
df350 = dataset[(dataset["power"] >= 350001) & (dataset["power"] <= 400000)]
df400 = dataset[(dataset["power"] >= 400001) & (dataset["power"] <= 450000)]
df450 = dataset[(dataset["power"] >= 450001) & (dataset["power"] <= 500000)]
df500 = dataset[dataset["power"] >= 500001]

print("Checkeo rapido ----------------------------")
print("df100:", df100.shape)
print("df150:", df150.shape)
print("df200:", df200.shape)
print("df250:", df250.shape)
print("df300:", df300.shape)
print("df350:", df350.shape)
print("df400:", df400.shape)
print("df450:", df450.shape)
print("df500:", df500.shape)

def remove_outliers_zscore(df, col="price", threshold=2.5):
    z = np.abs(stats.zscore(df[col]))
    return df[z < threshold]

df100_clean = remove_outliers_zscore(df100, "price", threshold=3)
df150_clean = remove_outliers_zscore(df150, "price", threshold=3)
df200_clean = remove_outliers_zscore(df200, "price", threshold=3)
df250_clean = remove_outliers_zscore(df250, "price", threshold=3)
df300_clean = remove_outliers_zscore(df300, "price", threshold=3)
df350_clean = remove_outliers_zscore(df350, "price", threshold=3)
df400_clean = remove_outliers_zscore(df400, "price", threshold=3)
df450_clean = remove_outliers_zscore(df450, "price", threshold=3)
df500_clean = remove_outliers_zscore(df500, "price", threshold=3)

print('Segundo sanity check ------------------')
print("df100:", df100.shape, "→", df100_clean.shape)
print("df150:", df150.shape, "→", df150_clean.shape)
print("df200:", df200.shape, "→", df200_clean.shape)
print("df250:", df250.shape, "→", df250_clean.shape)
print("df300:", df300.shape, "→", df300_clean.shape)
print("df350:", df350.shape, "→", df350_clean.shape)
print("df400:", df400.shape, "→", df400_clean.shape)
print("df450:", df450.shape, "→", df450_clean.shape)
print("df500:", df500.shape, "→", df500_clean.shape)

# Mergeando el dataet
cleaned_dataset = pd.concat([
    df100_clean,
    df150_clean,
    df200_clean,
    df250_clean,
    df300_clean,
    df350_clean,
    df400_clean,
    df450_clean,
    df500_clean
], ignore_index=True)

print("Final dataset shape:", cleaned_dataset.shape)

cleaned_dataset.to_csv('processed/outlier_free.csv', index=False)

# Push to Github
commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", "updating"],
    ["git", "push", "-u", "origin", "master"]
]

for cmd in commands:
    subprocess.run(cmd)