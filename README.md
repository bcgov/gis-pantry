# BC elevation stats

Report on max, min and average elevation for features (points, lines, polygons) in BC. Supports features extending as far south as 48°S.

## Requirements

A local copy of the BC 25m DEM, in an open format (ie, not file geodatabase raster).


## Setup

Clone the script repo:

    git bcelev.git
    cd bcelev

For easy setup in an isolated environment, use `conda`:

    conda env create
    conda activate elev-env

Alternatively, manually install all requirements noted in `environment.yml` to your environment via `pip` and `npm`.


## Usage

1. Create a trans-boundary DEM. If necessary, edit the script to point to the path of the BC 25m DEM on your system:

        ./create_dem.sh


2. Overlay input features with DEM using a command something like this (replacing station with your unique identifier):

        fio cat data/Kootenay_Elevation.gdb --layer 1:Watersheds_Elevation_TBD | \
          parallel \
            --pipe \
            "rio zonalstats \
              -r dem.tif \
              --prefix 'elevation_'" | \
          jq '.features[].properties | {STATION: .station, Z_MAX: .elevation_max, Z_MIN: .elevation_min, Z_AVG: .elevation_mean}' | \
          jq --slurp . | \
          in2csv -f json > elevationstats.csv



## Credits

jq usage plagiarized from [here](https://gist.github.com/david-murr/9d17e4b7267ab3290833)
