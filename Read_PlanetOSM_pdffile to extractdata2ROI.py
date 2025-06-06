# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 11:26:54 2025

@author: Acer
"""

import geopandas as gpd
from pyrosm import OSM
from shapely.geometry import box

# --- INPUT FILES ---
#pbf_file = "your_file.osm.pbf"  # Large PBF file
shapefile = "D:/FireData_27May2025/AdminBoundary/UK_State4326.shp"  # Shapefile to define bounding box
#output_gpkg = "extracted_data.gpkg"

pbf_file = "D:/FireData_27May2025/PY_Syntax/planet_osm_pbf/india-latest.osm.pbf"  # Replace with your .pbf file path
output_gpkg = "D:/FireData_27May2025/Outputfolder/Planet_OSM.gpkgoutput_data.gpkg"  # Output GeoPackage filename

# --- Load region boundary & compute bounding box ---
region = gpd.read_file(shapefile).to_crs("EPSG:4326")  # PBF is usually in EPSG:4326
minx, miny, maxx, maxy = region.total_bounds
bbox = [minx, miny, maxx, maxy]

# --- Load OSM data with bounding box ---
osm = OSM(pbf_file, bounding_box=bbox)

# --- Extract and export layer-wise to reduce memory pressure ---
def extract_and_save(getter, layer_name):
    try:
        gdf = getter()
        if gdf is not None and not gdf.empty:
            gdf.to_file(output_gpkg, layer=layer_name, driver="GPKG")
            print(f" {layer_name} exported.")
        else:
            print(f" {layer_name} is empty.")
    except Exception as e:
        print(f" Failed to export {layer_name}: {e}")

# Extract common layers one-by-one
extract_and_save(osm.get_network, "roads")
#extract_and_save(osm.get_buildings, "buildings")
extract_and_save(osm.get_pois, "pois")
#extract_and_save(osm.get_landuse, "landuse")
#extract_and_save(osm.get_transport, "transport")

print(" All layers processed RD and pois.")
