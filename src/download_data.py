import requests
import pandas as pd
from pathlib import Path

API_URL = "https://api.gbif.org/v1/occurrence/search"

params = {
    "country": "IT",
    "hasCoordinate": "true",
    "taxonRank": "SPECIES",
    "limit": 1000,
}

response = requests.get(
    API_URL,
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()
df = pd.DataFrame(data["results"])

print("HTTP status:", response.status_code)
print("Records downloaded:", len(df))
print("Total matching records:", data.get("count"))
print("Columns:", df.columns.tolist())

columns_to_check = [
    "speciesKey",
    "scientificName",
    "decimalLatitude",
    "decimalLongitude",
    "coordinateUncertaintyInMeters",
]

print("\nAvailable columns:")
print([col for col in columns_to_check if col in df.columns])

print("\nFirst five records:")
print(df[[col for col in columns_to_check if col in df.columns]].head())

print("\nDataset shape:", df.shape)

print("\nMissing values:")
print(
    df[
        [
            "speciesKey",
            "decimalLatitude",
            "decimalLongitude",
        ]
    ].isna().sum()
)

df_clean = (
    df[(df["speciesKey"].notna())
        & (df["decimalLatitude"] >= -90) & (df["decimalLatitude"] <= 90) # df["decimalLatitude"].between(-90, 90)
        & (df["decimalLongitude"] >= -180) & (df["decimalLongitude"] <= 180)
    ]
)

print("Original records:", len(df))
print("Clean records:", len(df_clean))
print("Excluded records:", len(df) - len(df_clean))

columns_to_keep = [
    "gbifID",
    "speciesKey",
    "scientificName",
    "decimalLatitude",
    "decimalLongitude",
    "coordinateUncertaintyInMeters",
]

df_export = df_clean.reindex(columns=columns_to_keep).copy()

print("\nExport dataset shape:", df_export.shape)
print("\nUnique species keys:", df_export["speciesKey"].nunique())
print("\nMissing uncertainty values:",
      df_export["coordinateUncertaintyInMeters"].isna().sum())

output_path = Path("data") / "gbif_italy_sample.csv"

df_export.to_csv(
    output_path,
    index=False,
)

print(f"Dataset saved to: {output_path}")