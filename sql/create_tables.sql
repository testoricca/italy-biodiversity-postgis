CREATE TABLE gbif_observations(
    gbif_id	                    BIGINT PRIMARY KEY,
    species_key	                BIGINT NOT NULL,
    scientific_name	            TEXT,
    latitude	                DOUBLE PRECISION NOT NULL,
    longitude	                DOUBLE PRECISION NOT NULL,
    coordinate_uncertainty_m	DOUBLE PRECISION,
    geom	                    geometry(Point, 4326)
);