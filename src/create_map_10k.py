from pathlib import Path
import geopandas as gpd

geojson_path = Path("data/italy_regions.geojson")

regions = gpd.read_file(geojson_path)

print("Number of regions:", len(regions))
print("CRS:", regions.crs)
print(regions[["shapeName", "geometry"]].head())

import pandas as pd
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

sql_path = Path("sql/regional_species_10k.sql")
query = sql_path.read_text(encoding="utf-8")

connection_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

with psycopg.connect(**connection_params) as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()
        column_names = [col.name for col in cur.description]

species_counts = pd.DataFrame(
    records,
    columns = column_names
)

print(species_counts.head())
print("Rows:", len(species_counts))

map_data = regions.merge(
    species_counts,
    left_on="shapeName",
    right_on="region_name",
    how="left",
    validate="one_to_one"
)

print("Regions after merge:", len(map_data))
print("Missing species counts:", map_data["n_species"].isna().sum())
print(map_data[["shapeName", "n_observations", "n_species"]].tail())

correlation = map_data["n_observations"].corr(
    map_data["n_species"],
    method="pearson"
)

print(f"Pearson correlation: {correlation:.3f}")

import matplotlib.pyplot as plt

output_path = Path("outputs/species_by_region_10k.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 11))

map_data.plot(
    column="n_species",
    cmap="viridis",
    legend=True,
    edgecolor="white",
    linewidth=0.5,
    ax=ax
)

ax.set_title(
    "Specie distinte osservate per regione\n"
    "Campione GBIF Italia (9.959 osservazioni)",
    fontsize=14
)

ax.set_axis_off()
fig.tight_layout()
fig.savefig(output_path, dpi=200, bbox_inches="tight")
plt.close(fig)

print("Map saved:", output_path)