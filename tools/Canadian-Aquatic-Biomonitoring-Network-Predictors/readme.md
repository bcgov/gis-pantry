# CABIN Catchment Predictors — README

Purpose
-------
This repository contains two Python scripts that together produce geomorphologic and climate predictors for catchments suitable for post-field analysis for the Canadian Aquatic Biomonitoring Network (CABIN):

- simple_pyshed_20250909.py — DEM-based catchment delineation using pysheds
- watersehd_model_predictors_20250909.py — Extracts catchment-level predictors (area, landcover fractions, slope class area, mean climate values) and writes an Excel table

These scripts are intended to be run sequentially: first delineate catchments (per pour/field points), then extract predictors for those delineated catchments.


Overview of the workflow
------------------------
1. Read DEM, pour points, and stream network.
2. Condition the DEM (fill pits, depressions, resolve flats), rasterize and optionally burn-in stream network.
3. Compute D8 flow directions and flow accumulation using pysheds.
4. Snap pour points to meaningful accumulation/stream locations (with configurable thresholds/distances).
5. Delineate catchments and export per-site catchment rasters and polygons (GeoPackage, one layer per site).
6. For each catchment polygon, compute predictors:
   - catchment area (ha)
   - percent area of landcover classes: Water, Snow/Ice (from LCC)
   - percent area of slope between 30–50%
   - mean precipitation for target months (PPT* rasters)
   - mean maximum temperature for target months (Tmax* rasters)
7. Save the predictors table to an Excel workbook for use in CABIN post-field analysis workflows.

Inputs — expected files & layers
--------------------------------
- DEM: 25m Digital Elevation Model 
- Pour points: Points representing the outflow of catchment areas (in this case field sample locations)
- Stream network: Clipped version of [WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP](https://catalogue.data.gov.bc.ca/dataset/92344413-8035-4c08-b996-65a9b3f62fca)
- Landcover: national LCC [shapefile ](https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_lcc_csc/shp_en)
- [Landcover Classifications](https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_lcc_csc//doc/GeoBase_lcc_en_Catalogue.pdf)
- Slope raster: 25m Clipped Slope raster
- [Climate rasters for precip and temp ](https://climatebc.ca/)

Outputs
-------
- Per-site raster catchments: Rasters of catchment areas
- Combined catchments GeoPackage: Polygons of all catchment areas
- Predictor table (Excel): final output of excel spreadsheet

CABIN context and notes
-----------------------
These predictors were designed to support CABIN post-field analysis by producing catchment-level covariates commonly used in modelling biological responses. Confirm the list of predictors and months (June/August/December in this code) match CABIN analysis needs and conventions and update script column names accordingly.
