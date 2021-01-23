import shutil
import json
import os
from os.path import join
from django.conf import settings
from osgeo import ogr, gdal
import zipfile
from .polygons import break_multis
from django.db import models
from pages.models import Tempfile
import subprocess


def kml_to_geojson_features(file_path):
    """ Given the path to an uploaded KML/KMZ file, this function returns the geometries within expressed as GeoJSON """
    # Save a temporary file locally
    tempfile = Tempfile(uploaded=file_path)
    tempfile.save()
    local_file_path = tempfile.uploaded.url
    tailURL = local_file_path.replace("/media", "") 
    absolute_path = settings.MEDIA_ROOT + tailURL

    # Define a path to store a json file containing the converted contents of the kml
    json_file_path = absolute_path[:-3]
    json_file_path += "json"

    # Fail when can't open
    gdal.UseExceptions()  

    # Open the kml file with GDAL
    srcDS = gdal.OpenEx(absolute_path)

    # Run the kml --> geojson conversion
    ds = gdal.VectorTranslate(json_file_path, srcDS, format='GeoJSON')

    # Remove the kml file from storage
    os.remove(tempfile.uploaded.path)

    # Delete GDAL object from memory
    del ds

    # Open the geojson file and store each individual feature in a list
    feature_list = []
    with open(json_file_path, "r+") as json_file:
        json_read = json_file.read()
        togeojson = json.loads(json_read)
        for i in togeojson["features"]:
            features = break_multis(i)
            for j in features:
                feature = json.dumps(j)
                feature_list.append(j)    
        json_file.close()
    
    # Remove all un-needed files and DB instances
    os.remove(json_file_path)
    tempfile.delete()

    return feature_list

def shapefile_to_geojson_features(file_path):
    """ Given the path to an uploaded shapefile, this function returns the geometries within expressed as GeoJSON  """
    # Save a temporary file locally
    tempfile = Tempfile(uploaded=file_path)
    tempfile.save()

    # Define all filepaths to be used
    local_file_path = tempfile.uploaded.url
    tailURL = local_file_path.replace("/media", "") 
    absolute_path = settings.MEDIA_ROOT + tailURL
    extract_folder = local_file_path.split(".zip")
    extract_folder = extract_folder[0]

    # Extract the contents of the compressed folder so we can process the contents of the shapefile.
    with zipfile.ZipFile(absolute_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
        zip_ref.close()
    
    # Obtain the shapefile containing the geometries we want
    shp_file = ""
    for fn in os.listdir(extract_folder):
        if fn.endswith(".shp"):
            shp_file = extract_folder + "/" + fn

    # Defined file paths where we can store the converted JSON file
    json_file_path = absolute_path.replace(".zip", ".json")
    input_shp = shp_file
    output_geoJson = json_file_path

    # Convert the shapefile to a JSON file.
    cmd = "ogr2ogr -f GeoJSON -t_srs crs:84 "  + output_geoJson +" " + input_shp
    subprocess.call(cmd , shell=True)    

    # Extract all the geometries from the JSON file and store them in a list
    feature_list = []
    with open(output_geoJson) as g_file:
        gj = json.loads(g_file.read())
        for i in gj["features"]:                    
            features = break_multis(i)
            for j in features:
                feature_list.append(j)            
        g_file.close()

    #  Delete all the un-needed files and DB instances
    tempfile.delete()
    os.remove(output_geoJson)
    os.remove(absolute_path)
    shutil.rmtree(extract_folder)

    return feature_list
    

def geojson_file_to_geojson_features(file_path):
    """ Given the path to an uploaded GeoJSON file, this function returns the geometries within expressed as GeoJSON  """
    # Save a temporary file locally
    tempfile = Tempfile(uploaded=file_path)
    tempfile.save()
    local_file_path = tempfile.uploaded.url
    tailURL = local_file_path.replace("/media", "") 
    absolute_path = settings.MEDIA_ROOT + tailURL

    # Extract all the geometries from the JSON file and store them in a list
    feature_list = []
    with open(absolute_path) as g_file:
        gj = json.loads(g_file.read())
        gj = break_multis(gj)
        try:
            gj = gj["features"]
        except:
            pass
        for i in gj:                    
            features = break_multis(i)
            for j in features:
                feature_list.append(j)                   
        g_file.close()

    #  Delete all the un-needed files and DB instances
    tempfile.delete()
    os.remove(absolute_path)

    return feature_list



def file_to_geojson_features(file_path):
    """ Given a file (accepted file types are: KML/KMZs, GeoJSON, and Shapefiles), this method returns the geometries contained within as GeoJSON """
    filename = file_path.name
    geojson = {}
    if filename.endswith("kmz") or filename.endswith("kml"):
        geojson = kml_to_geojson_features(file_path)
    elif filename.endswith("zip"):
        geojson = shapefile_to_geojson_features(file_path)
    elif filename.endswith("json"):
        geojson = geojson_file_to_geojson_features(file_path)
    return geojson