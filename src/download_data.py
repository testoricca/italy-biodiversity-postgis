import requests
import pandas as pd

API_URL = "https://api.gbif.org/v1/occurrence/search"

params = {
    "country": "IT",
    "hasCoordinate": "true",
    "limit": 20,
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