import requests

API_URL = "https://www.geoboundaries.org/api/current/gbOpen/ITA/ADM2/"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

metadata = response.json()

print("Response type:", type(metadata))
print("Available keys:", list(metadata.keys()))

print("Administrative units:", metadata["admUnitCount"])
print("GeoJSON URL:", metadata["gjDownloadURL"])


geojson_url = metadata["gjDownloadURL"]

geojson_response = requests.get(
    geojson_url,
    timeout=60
)

geojson_response.raise_for_status()

from pathlib import Path

output_path = Path("data") / "italy_regions.geojson"
output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_bytes(geojson_response.content)

print("File size:", output_path.stat().st_size, "bytes")

import json

with output_path.open("r", encoding="utf-8") as f:
    geojson_data = json.load(f)

print("Number of features:", len(geojson_data["features"]))
region_names = [
    feature["properties"]["shapeName"]
    for feature in geojson_data["features"]
]
print("Region names:", sorted(region_names))

from collections import Counter

geometry_types = Counter(
    feature["geometry"]["type"]
    for feature in geojson_data["features"]
    if feature["geometry"] is not None
)

missing_geometries = sum(
    feature["geometry"] is None
    for feature in geojson_data["features"]
)

print("Geometry types:", geometry_types)
print("Missing geometries:", missing_geometries)
