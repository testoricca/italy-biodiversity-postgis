# Italy Biodiversity Analysis with PostGIS

## Project overview

This project investigates the geographic distribution of biodiversity observations across Italian administrative regions.

The analysis combines public biodiversity occurrence records, administrative boundaries, PostgreSQL/PostGIS, Python, pandas, and GeoPandas.

## Research question

How many distinct species are represented in biodiversity occurrence records across Italian regions?

## Data sources

- GBIF — Global Biodiversity Information Facility
- geoBoundaries — Administrative boundaries

## Project workflow

1. Retrieve and validate public biodiversity data.
2. Import observations and administrative boundaries into PostGIS.
3. Perform spatial joins and aggregate observations by region.
4. Validate the results using Python.
5. Produce a map and document the findings.

## Important limitations

Observed species counts depend on sampling effort, geographic coverage, and data quality. They should not be interpreted as unbiased estimates of true regional species richness.

## Status

Work in progress — Week 6.5 portfolio project.