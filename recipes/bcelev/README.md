# BC elevation stats

A recipe for quickly reporting on elevation stats (max, min, mean, median, etc) for features (points, lines, polygons) in BC and adjacent jurisdictions.

For features spanning the 49th parallel BC/USA border, (currently supported for as far south as 48°S), the script uses [Mapzen Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) hosted on AWS. See [tilezen documentation](https://github.com/tilezen/joerd/tree/master/docs) for more info about these tiles.

The supplied script currently only downloads DEM tiles along the 49th parallel but could easily be expanded to download tiles in AB/YT/AK/NWT.


## Requirements

1. bash (the scripts will not currently run on Windows)
2. A local copy of the BC 25m DEM, in an open format (ie, not file geodatabase
raster)


## Setup

For easy setup in an isolated environment, use `conda`:

    conda env create
    conda activate elev-env

Alternatively, manually manage your environment by installing all requirements noted in [`environment.yml`](environment.yml) via `pip` and `npm` (and `brew` or similar for `parallel`)


## Usage

1. Create a trans-boundary DEM, supplying the script with the path to your copy of the BC 25m DEM:

        ./create_dem.sh <path/to/bc_dem.tif>


2. Overlay input features with the DEM using a command something like this (replacing `station` with your unique identifier):

        fio cat myfile.gdb --layer 1:Basins | \
          parallel \
            --pipe \
            "rio zonalstats \
              --stats \"min max mean median\" \
              -r dem.tif \
              --prefix 'elevation_'" | \
          jq '.features[].properties | {STATION: .station, Z_MAX: .elevation_max, Z_MIN: .elevation_min, Z_AVG: .elevation_mean, Z_MEDIAN: .elevation_median}' | \
          jq --slurp . | \
          in2csv -f json > myfile_elev.csv

See the [`rasterstats` documentation](https://pythonhosted.org/rasterstats/cli.html) for more info on usage and stats that can be extracted. For point features, you may want to use `rio pointquery` rather than `rio zonalstats`.

## Credits / resources

- [gdal](https://gdal.org/)
- [fiona](https://github.com/Toblerity/Fiona)
- [rasterio](https://github.com/mapbox/rasterio)
- [rasterstats](https://github.com/perrygeo/python-rasterstats)

jq usage is plagiarized from [here](https://gist.github.com/david-murr/9d17e4b7267ab3290833)

## See also

[elevatr](https://github.com/jhollist/elevatr) and [intro to elevatr](https://cran.r-project.org/web/packages/elevatr/vignettes/introduction_to_elevatr.html)
