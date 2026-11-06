import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
import pandas as pd

BASE_URL = "https://api.gbif.org/v1/occurrence/search"

TARGET_RECORDS = 10_000
PAGE_SIZE = 300

all_records = []

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)

for offset in range(0, TARGET_RECORDS, PAGE_SIZE):

    remaining = TARGET_RECORDS - offset
    current_limit = min(PAGE_SIZE, remaining)

    params = {
        "country": "IT",
        "hasCoordinate": "true",
        "taxonRank": "SPECIES",
        "limit": current_limit,
        "offset": offset
    }

    response = session.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    page_records = data["results"]

    if len(page_records) != current_limit:
        raise ValueError(
            f"Incomplete page at offset {offset}: "
            f"expected {current_limit}, "
            f"received {len(page_records)}"
    )

    if len(page_records) == 0:
        print("No more records available.")
        break

    all_records.extend(page_records)

    print(
        f"Offset: {offset} | "
        f"Page records: {len(page_records)} | "
        f"Total downloaded: {len(all_records)}"
    )

print(f"\nFinal total: {len(all_records)}")

gbif_ids = [record["gbifID"] for record in all_records]

unique_ids = set(gbif_ids)

print("Downloaded records:", len(all_records))
print("Unique GBIF IDs:", len(unique_ids))
print("Duplicate records:", len(all_records) - len(unique_ids))

actual_records = len(all_records)

if actual_records != TARGET_RECORDS:
    raise ValueError(
        f"Expected {TARGET_RECORDS} records, "
        f"but downloaded {actual_records}"
    )

if len(unique_ids) != actual_records:
    raise ValueError("Duplicate GBIF IDs detected")

print("Download validation passed.")

columns = [
    "gbifID",
    "speciesKey",
    "scientificName",
    "decimalLatitude",
    "decimalLongitude",
    "coordinateUncertaintyInMeters",
]

df = pd.DataFrame(all_records)

df = df[columns].copy()

# Escludiamo le osservazioni senza identificativo tassonomico
df = df.dropna(subset=["speciesKey"])

# Creiamo il percorso di output
output_path = Path("data/gbif_italy_10000.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Salviamo senza aggiungere l'indice pandas
df.to_csv(output_path, index=False)

print("Rows saved:", len(df))
print("Unique species:", df["speciesKey"].nunique())
print("Missing coordinate uncertainty:",
      df["coordinateUncertaintyInMeters"].isna().sum())
print("Saved to:", output_path)