import json
from pathlib import Path

input_path = Path("data") / "italy_regions.geojson"

with input_path.open("r", encoding="utf-8") as f:
    geojson_data = json.load(f)

region_records = []

for region_id, feature in enumerate(geojson_data["features"], start=1):
    region_name = feature["properties"]["shapeName"]
    geometry_json = json.dumps(feature["geometry"])

    region_records.append(
        (region_id, region_name, geometry_json)
    )

print("Regions prepared:", len(region_records))
print("First region ID:", region_records[0][0])
print("First region name:", region_records[0][1])
print("Geometry JSON type:", type(region_records[0][2]))

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

connection_params = {
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}

insert_sql = """
   INSERT INTO italy_regions (
    region_id,
    region_name,
    geom
)
VALUES (
    %s,
    %s,
    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
)
ON CONFLICT (region_id) DO NOTHING;
"""

with psycopg.connect(**connection_params) as conn:
    with conn.cursor() as cur:
        cur.executemany(insert_sql, region_records)

print("Regions imported successfully.")