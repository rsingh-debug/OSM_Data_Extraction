# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 12:26:45 2025

@author: Acer
"""

import geopandas as gpd
from pyrosm import OSM
import shapely
import os

# Paths
#pbf_file = "your_file.osm.pbf"  # Large PBF file


region_path = "D:/FireData_27May2025/AdminBoundary/UK_State4326.shp"  # Shapefile to define bounding box
pbf_path = "D:/FireData_27May2025/PY_Syntax/planet_osm_pbf/india-latest.osm.pbf"  # Replace with your .pbf file path
output_gpkg = "D:/FireData_27May2025/Outputfolder/Planet_OSM.gpkg"  # Output GeoPackage filename

# Step 1: Read region and get bounding box
region = gpd.read_file(region_path).to_crs("EPSG:4326")
minx, miny, maxx, maxy = region.total_bounds
bbox = [minx, miny, maxx, maxy]

# Step 2: Initialize OSM reader with bounding box
osm = OSM(pbf_path, bounding_box=bbox)

# Step 3: Define features to extract one-by-one to avoid memory issues
layers = {
    "roads": osm.get_network,
    #"buildings": osm.get_buildings,
    #"landuse": osm.get_landuse,
    #"pois": osm.get_pois,
}

# Step 4: Loop through layers and export safely
for name, func in layers.items():
    try:
        print(f"📦 Processing: {name}")
        gdf = func()
        
        # Skip empty results
        if gdf is None or gdf.empty:
            print(f"⚠️ No data found for {name}. Skipping...")
            continue

        # Clip to exact region boundary to reduce size further
        gdf_clipped = gpd.clip(gdf, region)

        # Write to geopackage
        gdf_clipped.to_file(output_gpkg, layer=name, driver="GPKG")
        print(f"✅ Saved: {name} ({len(gdf_clipped)} features)")
        
        # Clean memory
        del gdf, gdf_clipped

    except Exception as e:
        print(f"❌ Error processing {name}: {e}")
