# ----------------
# Create a 25m trans-border DEM
# (upsampling mapzen data from 30m to 25m)
# ----------------

# Batch download 1 degree Mapzen terrain tiles along 49th parallel
# (with slight overlap into Canada to cover any gaps)
# https://registry.opendata.aws/terrain-tiles/
# ----------------
python get_terraintiles.py

# merge downloaded tiles
# ----------------
gdalbuildvrt tmp/mapzen.vrt tmp/*tif

gdalwarp \
  tmp/mapzen.vrt \
  tmp/mapzen.tif \
  -t_srs EPSG:3005 \
  -r cubic \
  -tr 25 25 \
  -dstnodata -9999 \
  -wo NUM_THREADS=ALL_CPUS \
  -ot Int16 \
  -co COMPRESS=DEFLATE \
  -co TILED=YES \
  -co ZLEVEL=9 \
  -co PREDICTOR=2


# Copy BC DEM to local folder, setting 0 to NODATA
# (We don't want to do this to the source file because there are valid 0 cells
# that would require some tidying to identify)
# ----------------
cp $1 tmp/bc_dem_0null.tif
gdal_edit.py \
  tmp/bc_dem_0null.tif \
  -a_nodata 0

# Finally, combine the two data sources into output dem.tif
# ----------------
gdalbuildvrt \
  tmp/transborder.vrt \
  tmp/mapzen.tif \
  tmp/bc_dem_0null.tif

gdal_translate \
  tmp/transborder.vrt \
  dem.tif \
  -ot Int16 \
  -co COMPRESS=DEFLATE \
  -co TILED=YES \
  -co ZLEVEL=9 \
  -co PREDICTOR=2


echo 'output dem.tif created, consider deleting intermediate files in tmp'