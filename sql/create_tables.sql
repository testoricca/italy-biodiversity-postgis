CREATE TABLE IF NOT EXISTS gbif_observations(
    gbif_id	                    BIGINT PRIMARY KEY,
    species_key	                BIGINT NOT NULL,
    scientific_name	            TEXT,
    latitude	                DOUBLE PRECISION NOT NULL,
    longitude	                DOUBLE PRECISION NOT NULL,
    coordinate_uncertainty_m	DOUBLE PRECISION,
    geom	                    geometry(Point, 4326)
);

CREATE TABLE IF NOT EXISTS italy_regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL UNIQUE,
    geom geometry(Geometry, 4326) NOT NULL
);