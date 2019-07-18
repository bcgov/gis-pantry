# BC elevation stats

Report on max, min and average elevation for features (points, lines, polygons) in BC. For areas in BC, the script uses the (non-public) BC 25m DEM. For features spanning the BC border, (currently supported for as far south as 48°S), the script uses [Mapzen Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) hosted on AWS. See [tilezen documentation](https://github.com/tilezen/joerd/tree/master/docs) for more info about these tiles.

## Requirements

A local copy of the BC 25m DEM, in an open format (ie, not file geodatabase raster).


## Setup

Clone the script repo:

    git bcelev.git
    cd bcelev

For easy setup in an isolated environment, use `conda`:

    conda env create
    conda activate elev-env

Alternatively, manually manage your environment by installing all requirements noted in [`environment.yml`](environment.yml) via `pip` and `npm` (and `brew` or similar for `parallel`)


## Usage

1. Create a trans-boundary DEM. If necessary, edit the script to point to the path of the BC 25m DEM on your system:

        ./create_dem.sh


2. Overlay input features with the DEM using a command something like this (replacing `station` with your unique identifier):

        fio cat ~/Dropbox/temp/Watershed_Median_Elevation.gdb --layer 1:Basins | \
          parallel \
            --pipe \
            "rio zonalstats \
              -r dem.tif \
              --prefix 'elevation_'" | \
          jq '.features[].properties | {STATION: .station, Z_MAX: .elevation_max, Z_MIN: .elevation_min, Z_AVG: .elevation_mean, Z_MEDIAN: .elevation_median}' | \
          jq --slurp . | \
          in2csv -f json > elevationstats.csv

See the [`rasterstats` documentation](https://pythonhosted.org/rasterstats/cli.html) for more info on stats that can be extracted. For point features, you may want to use `rio pointquery` rather than `rio zonalstats`.

## Credits

jq usage plagiarized from [here](https://gist.github.com/david-murr/9d17e4b7267ab3290833)
