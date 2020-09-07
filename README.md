# Problem:

Find geographical neighbours of districts in India as adjacency list.

## Data:

https://wiki.openstreetmap.org/wiki/India
https://wiki.openstreetmap.org/wiki/India/Boundaries
https://wiki.openstreetmap.org/wiki/Districts_in_India

GeoJSON can be downloaded by running an appropriate query on overpass.
A sample query is given in,
`./overpass_query.txt`

**Note**: Different countries may use different administrative levels and terminology.

## Overpass
http://overpass-turbo.eu/
http://overpass-turbo.eu/s/ynJ

## GeoJSON
https://geojson.org/
https://en.wikipedia.org/wiki/GeoJSON
https://medium.com/@sumit.arora/what-is-geojson-geojson-basics-visualize-geojson-open-geojson-using-qgis-open-geojson-3432039e336d

## Shapely

`Shapely` has been used to deal with geographical boundaries

`pip3 install shapely`

https://shapely.readthedocs.io/en/stable/manual.html
https://pypi.org/project/Shapely/

# Usage
Put GeoJSON data file in `data/data.geojson`. 
To test, you may extract the data file from `sample_data/`

Run,

`python find_neighbours.py`

# Input
## GeoJSON data acquired from overpass-turbo
`./data/data.geojson`

**Note**: Erroneous 'wikidata keys' of two districts have been manually corrected, and are mentioned in `errors.txt`. This file is not automatically processed. By default, the program is only going to work with data file

# Output
## wikidata keys, osm relations, names etc mapping of districts
`./output/details.csv`

## polygons and other features
`./output/geometry/{key}_polygon.geojson`

`./output/geometry/{key}_features.json`

## neighbour lists
`./output/neighbours.json       # GeoJSON Keys`

`./output/neighbour_names.json  # Names`

# Extra

The program can filter based on administrative level.
Districts (Administrative Level 5) from India have been considered as the data.
However, the program can be applied to any other such GeoJSON.

Pitfalls can be if certain 'properties' are missing from the GeoJSON objects.
Refer to `extract_geometry()` function for more details.
