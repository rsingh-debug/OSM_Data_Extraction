# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 17:56:21 2025

@author: Acer
"""

import os
import requests
from pyrosm import get_data, OSM
import geopandas as gpd
import zipfile

def download_pbf(region_name, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pbf_path = get_data(region_name, directory=output_folder)
    return pbf_path

def extract_and_save_layer(pbf_file, region_shapefile, layer, zip_filename):
    region_gdf = gpd.read_file(region_shapefile).to_crs("EPSG:4326")
    bbox = region_gdf.total_bounds.tolist()
    osm = OSM(pbf_file, bounding_box=bbox)

    if layer == "places":
        # ✅ Correct way to extract place-type POIs
        custom_filter = {"place": ["village", "town", "hamlet", "suburb", "locality"]}
        gdf = osm.get_pois(custom_filter=custom_filter)
    elif layer == "roads":
        gdf = osm.get_network(network_type="all")
    else:
        raise ValueError("Unsupported layer requested.")

    if gdf is None or gdf.empty:
        print(f"⚠️ No data found for {layer}")
        return

    gdf = gdf.to_crs(region_gdf.crs)
    gdf = gdf[gdf.geometry.intersects(region_gdf.unary_union)]

    output_dir = f"osm_{layer}_shp"
    os.makedirs(output_dir, exist_ok=True)
    shapefile_name = f"osm_{layer}"
    shapefile_path = os.path.join(output_dir, shapefile_name + ".shp")
    gdf.to_file(shapefile_path)

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
            file = os.path.join(output_dir, shapefile_name + ext)
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))

    print(f"✅ {layer.capitalize()} saved to {zip_filename}")
    
def download_planet_osm_data(region_name, region_shapefile):
    print("⏬ Downloading PBF for:", region_name)
    pbf_file = download_pbf(region_name, "planet_osm_pbf")

    extract_and_save_layer(pbf_file, region_shapefile, "places", "planet_osm_places.zip")
    extract_and_save_layer(pbf_file, region_shapefile, "roads", "planet_osm_roads.zip")

# Example usage
download_planet_osm_data("india", "D:/FireData_27May2025/AdminBoundary/UK_State4326.shp")
