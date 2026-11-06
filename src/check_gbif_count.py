import requests

url = "https://api.gbif.org/v1/occurrence/search"

params = {
    "country": "IT",
    "hasCoordinate": "true",
    "taxonRank": "SPECIES",
    "limit": 0
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

print("Response type:", type(data))
print("Available keys:", data.keys())

total_records = data["count"]

print(f"Total GBIF records: {total_records:,}")