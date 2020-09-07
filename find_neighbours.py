#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 02:15:55 2019

@author: Hrishikesh Terdalkar
"""

import os
import json
from collections import defaultdict

from shapely.geometry import shape

###############################################################################


def extract_geometry(geojson_file, admin_level='5',
                     output_dir="geometry", details_file="details.json"):
    '''
    Extract administrative boundary polygons from GeoJSON

    @params:
        admin_level: administrative level to extract (default: 5)
        output_dir: path where the polygons and features should be saved
        details_file: file in which details about nodes are stored

    @return:
        details
    '''
    details = {}
    try:
        with open(geojson_file, 'r') as f:
            data = json.load(f)
        feature_collection = data['features']
    except Exception:
        print("Error: geojson file not found.")
        feature_collection = []

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for feature in feature_collection:
        try:
            properties = feature['properties']
            geometry = feature['geometry']

            if not ((properties['admin_level'] == str(admin_level)) and
                    (properties['boundary'] == 'administrative') and
                    (properties['type'] == 'boundary')):
                continue

            if 'wikidata' in properties:
                _wikidata = properties['wikidata']
            else:
                _wikidata = None

            _id = properties['@id'].replace('/', '_')
            _name = properties['name'].lower().replace(' ', '_')
            _geo_type = feature['geometry']['type']
            _rings = len(geometry['coordinates'])

            details[_id] = [_wikidata, _name, _geo_type, _rings]
            filename = os.path.join(output_dir, f'{_id}_feature.json')
            with open(filename, 'w') as f:
                json.dump(feature, f)
            print(f"Feature written: {_name} ({_id}).")

            filename = os.path.join(output_dir, f'{_id}_geometry.geojson')
            with open(filename, 'w') as f:
                json.dump(geometry, f)
            print(f"Geometry written: {_name} ({_id}).")
        except Exception:
            pass

    with open(details_file, "w") as f:
        json.dump(details, f)

    return details


def load_geometry(details, objects_dir):
    '''
    Load GeoJSON geometrical objects using Shapely
    '''
    geo_objects = {}
    for _id in details:
        geometry_file = os.path.join(objects_dir, f'{_id}_geometry.geojson')
        with open(geometry_file, 'r') as f:
            _geometry = json.load(f)
            geo_objects[_id] = shape(_geometry)

    return geo_objects


def find_neighbours(geo_objects):
    '''
    Build an adjacency list from geometrical objects
    '''
    adjlist = defaultdict(set)
    for key1, polygon1 in geo_objects.items():
        for key2, polygon2 in geo_objects.items():
            if key1 == key2:
                continue
            if polygon1.intersects(polygon2):
                adjlist[key1].add(key2)
                adjlist[key2].add(key1)
    adjlist = {k: list(v) for k, v in adjlist.items()}
    return adjlist


def change_labels(adjlist, details, name=None):
    '''
    Generate an adjacency list with different node labels
    instead of GeoJSON feature IDs.

    @params:
        adjlist: adjacency list of neighbours
        details: dict, created by extract_geometry
        name: function to get name for a relation
    '''
    if not name:
        def name(k):
            return f'{details[k][1]}/{details[k][0]}'

    _adjlist = {}
    for _id, neighbours in adjlist.items():
        _neighbours = []
        for neighbour in neighbours:
            _neighbours.append(name(neighbour))
        _adjlist[name(_id)] = _neighbours
    return _adjlist

###############################################################################


def main():
    '''
    Find Neighbouring Districts of India
    '''

    # ----------------------------------------------------------------------- #

    # Input
    input_dir = 'data'
    geojson_file = os.path.join(input_dir, 'data.geojson')
    admin_level = 5

    # Output
    output_dir = 'output'
    geometry_dir = os.path.join(output_dir, 'geometry')

    details_file = os.path.join(output_dir, 'details.json')

    neighbours_file = os.path.join(output_dir, 'neighbours.json')
    neighbour_names_file = os.path.join(output_dir, 'neighbour_names.json')

    # ----------------------------------------------------------------------- #

    details = extract_geometry(geojson_file,
                               admin_level=admin_level,
                               output_dir=geometry_dir,
                               details_file=details_file)
    geo_objects = load_geometry(details,
                                objects_dir=geometry_dir)
    adjlist = find_neighbours(geo_objects)
    names_adjlist = change_labels(adjlist,
                                  details=details)

    with open(neighbours_file, 'w') as f:
        json.dump(adjlist, f, indent=2)

    with open(neighbour_names_file, 'w') as f:
        json.dump(names_adjlist, f, indent=2)

    return locals()

###############################################################################


if __name__ == '__main__':
    locals().update(main())

###############################################################################
