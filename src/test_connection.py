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

with psycopg.connect(**connection_params) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT current_database(), current_user, PostGIS_Version();"
        )
        result = cur.fetchone()

print("Connection successful!")
print("Database:", result[0])
print("User:", result[1])
print("PostGIS:", result[2])