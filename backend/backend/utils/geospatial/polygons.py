import json
import os
import shutil
import subprocess
import zipfile
from django.conf import settings
from rrm.utils import break_multis
from urllib.request import urlopen
from io import BytesIO
from .files import kml_to_geojson_features
from shapely.geometry import shape
import shapely.ops

def break_geom_collection(geojson):
    """
    given geojson containing a geometrycollection, this method returns the geojsononly containing only polygons
    """    
    new_geoms = []
    for i in geojson["geometries"]:
        if i["type"] == "Polygon":
            new_geoms.append(i)
    geojson["geometries"] = new_geoms
    return geojson

def convert_to_shp(obj):
    """
    Given geojson, this method returns that geoJSON converted into a shapely object. Shapely offers a number of useful geometric operations.
    """
    if type(obj) == str:
        obj = json.loads(obj)
    # Shapely is innacurate in reporting geom types
    geom_type = "Polygon"
    if "geometry" in obj:
        try:
            if obj["geometry"]["type"] == "Point" or obj["geometry"]["type"] == "LineString":
                shp_geom = shape(obj["geometry"]).buffer(0)
            else:
                shp_geom = shape(obj["geometry"]).buffer(0)
            geom_type = obj["geometry"]["type"]
        except:
            try:
                shp_geom = shape(obj["geometry"]).buffer(0)
            except: 
                shp_geom = shape(obj["geometry"]).buffer(0)
            geom_type = obj["geometry"]["type"]
    elif "geometries" in obj:
        obj = break_geom_collection(obj)
        shp_geom = shape(obj["geometries"][0]).buffer(0)
    else:
        try:
            if obj["type"] == "Point" or obj["type"] == "LineString":
                shp_geom = shape(obj).buffer(0)
            else:
                shp_geom = shape(obj).buffer(0)
            geom_type = obj["type"]
        except:
            # print("OBJ109", obj, "\n\n")
            shp_geom = shape(obj).buffer(0)
            geom_type = obj["type"]
    return shp_geom, geom_type

def online_shapefile_to_geojson(file_path, dataset):
  """ Given a url to an online shapefile this method returns all the geometries therein in GeoJSON format. """
  # define temporary folder
  extract_folder = settings.MEDIA_ROOT + "/temp"
  gj_path = extract_folder + "/temp.json"
  with urlopen(file_path) as fp:
    with BytesIO(fp.read()) as b, zipfile.ZipFile(b, 'r') as zip_ref:
      zip_ref.extractall(extract_folder)
  shp_file = ""
  for fn in os.listdir(extract_folder):
      if fn.endswith(".shp"):
          shp_file = extract_folder + "/" + fn

  gj_file = gj_path.replace(".zip", ".json")
  input_shp = shp_file
  output_geoJson = gj_file
  cmd = "ogr2ogr -f GeoJSON -t_srs crs:84 "  + output_geoJson +" " + input_shp
  subprocess.call(cmd , shell=True)     
  geojson = []
  with open(output_geoJson) as g_file:
      gj = json.loads(g_file.read())
      for i in gj["features"]:                    
          features = break_multis(i)
          for j in features:
              j["dataset"] = dataset
              geojson.append(j)            
      g_file.close()
  os.remove(output_geoJson)
  shutil.rmtree(extract_folder)
  return geojson

def online_kml_to_geojson(file_path):
  """ Given a url to an online shapefile this method returns all the geometries therein in GeoJSON format. """
#   NOT FINISHED
  # define temporary folder
  extract_folder = settings.MEDIA_ROOT + "/temp"
  gj_path = extract_folder + "/temp.json"
  features = {}
  with urlopen(file_path) as fp:
    with BytesIO(fp.read()) as b:
      features = kml_to_geojson_features(b)
      print("features", features)
  return features
  gj_file = gj_path.replace(".zip", ".json")
  input_shp = file_path
#   input_shp = shp_file
  output_geoJson = gj_file
  cmd = "ogr2ogr -f GeoJSON -t_srs crs:84 "  + output_geoJson +" " + input_shp
  subprocess.call(cmd , shell=True)     
  geojson = []
  with open(output_geoJson) as g_file:
      gj = json.loads(g_file.read())
      for i in gj["features"]:                    
          features = break_multis(i)
          for j in features:
              geojson.append(j)            
      g_file.close()
  os.remove(output_geoJson)
  shutil.rmtree(extract_folder)
  return geojson  


def break_multis(geojson):
    """
    Given GeoJSON, this method returns a list of all the individual geometries therein.
    """
    features = []
    try1 = False
    try2 = False
    try3 = False
    try:
        if geojson["geometry"]["type"] == "MultiPolygon":
            try1 = True
            for i in geojson["geometry"]["coordinates"]:
                new_json = {"type": "Polygon", "coordinates": []}
                new_json["coordinates"] = i
                features.append(new_json)
    except:
        try:
            if geojson["type"] == "FeatureCollection":
                try1 = True
                for i in geojson["features"]:
                    features.append(i)
        except: 
            if geojson["geometry"]["type"] == "FeatureCollection":
                try1 = True
                for i in geojson["features"]:
                    features.append(i)
    try:
        if geojson["type"] == "Feature" and not try1:
            try2 = True
            features.append(geojson)
    except:
        pass
    try:
        if geojson["type"] == "MultiPolygon" and not try1 and not try2:
            try3 = True
            for i in geojson["geometry"]:
                new_json = {"type": "Polygon", "coordinates": []}
                new_json["coordinates"] = i
                features.append(new_json)
    except:
        if geojson["type"] == "MultiPolygon" and not try1 and not try2:
            try3 = True
            for i in geojson["coordinates"]:
                new_json = {"type": "Polygon", "coordinates": []}
                new_json["coordinates"] = i
                features.append(new_json)

    try:
        if geojson["type"] == "Polygon" and not try1 and not try2 and not try3:
            features.append(geojson)

    except:
        pass    
    return features

def buffer_polygons(geojson, buff_val):
    """ Expands the size of a given polygon by the provided size. """
    shp_poly = convert_to_shp(geojson)[0]
    buffered_shp = shp_poly.buffer(buff_val)
    buffered_geojson = shapely.geometry.mapping(buffered_shp)
    return buffered_geojson