SELECT
    r.region_name,
    COUNT(o.gbif_id) AS n_observations,
    COUNT(DISTINCT o.species_key) AS n_species
FROM italy_regions AS r
LEFT JOIN gbif_observations_10k AS o
    ON ST_Intersects(o.geom, r.geom)
GROUP BY
    r.region_id,
    r.region_name
ORDER BY n_species DESC;