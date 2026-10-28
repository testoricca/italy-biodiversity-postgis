from pathlib import Path
import os

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

csv_path = Path("data") / "gbif_italy_sample.csv"

df = pd.read_csv(csv_path)

column_mapping = {
    "gbifID": "gbif_id",
    "speciesKey": "species_key",
    "scientificName": "scientific_name",
    "decimalLatitude": "latitude",
    "decimalLongitude": "longitude",
    "coordinateUncertaintyInMeters": "coordinate_uncertainty_m",
}

df = df.rename(columns=column_mapping)

print(df.head())
print("\nData types:")
print(df.dtypes)

records = []

for row in df.itertuples(index=False):
    gbif_id = int(row.gbif_id)
    species_key = int(row.species_key)
    if pd.isna(row.scientific_name):
            scientific_name = None
    else: scientific_name = str(row.scientific_name)
    latitude = float(row.latitude)
    longitude = float(row.longitude)
    if pd.isna(row.coordinate_uncertainty_m):
        coordinate_uncertainty_m = None
    else: coordinate_uncertainty_m = float(row.coordinate_uncertainty_m)
    record = (gbif_id, species_key, scientific_name, latitude, longitude, coordinate_uncertainty_m)
    records.append(record)

print("Records prepared:", len(records))
print("First record:", records[0])
print("Tuple length:", len(records[0]))

insert_sql = """
    INSERT INTO gbif_observations (
        gbif_id,
        species_key,
        scientific_name,
        latitude,
        longitude,
        coordinate_uncertainty_m,
        geom
    )
    VALUES (
        %s, %s, %s, %s, %s, %s,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)
    )
    ON CONFLICT (gbif_id) DO NOTHING;
"""

insert_records = []

for record in records:
     longitude = record[4]
     latitude = record[3]
     insert_record = record + (longitude, latitude)
     insert_records.append(insert_record)

print("Parameters in first record:", len(insert_records[0]))

connection_params = {
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}

with psycopg.connect(**connection_params) as conn:
    with conn.cursor() as cur:
        cur.executemany(insert_sql, insert_records)

print("Database insertion completed.")