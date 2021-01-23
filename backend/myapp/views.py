from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .alerts2ChangeDetection import dictionaries
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import numpy
import requests
import ee
import json
from .alerts2ChangeDetection.analyze import *
from .utils import *
from backend.utils.API.ecos import get_species_range, get_critical_habitat_species_list, get_species_critical_habitat, get_species_names
from backend.utils.geospatial.polygons import break_multis, online_shapefile_to_geojson, online_kml_to_geojson, buffer_polygons
from backend.utils.geospatial.files import file_to_geojson_features
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser



class Analysis(APIView):
  permission_classes = (permissions.AllowAny,)

  def post(self, req, format=None):
    # Initialize data POSTed in the request
    start_date = req.data["startDate"]
    end_date = req.data["endDate"]
    coordinates = req.data["coords"]
    tries = int(req.data["tries"])
    geoj = json.loads(coordinates)
    
    # This is the problem. EE cant render this for some reason...
    small = buffer_polygons(geoj, -1.105)
    # small = buffer_polygons(geoj, -.001)
    # We should buffer to max based on centroid
    # return Response({"poly": small})
    # geoj = small
    # Convert GeoJSON to ee object 
    if geoj["type"] == "FeatureCollection":
      aoi = ee.FeatureCollection(geoj)
      aoi = aoi.map(lambda x: x.geometry().bounds())
      print("ee1")
    else:
      try:
        coordinates = geoj["geometry"]["coordinates"]
        aoi = ee.Geometry.Polygon(coordinates).bounds()
        print("ee2")
      except:
        aoi = ee.FeatureCollection({"type": "FeatureCollection", "features": [geoj]})
        aoi = aoi.map(lambda x: x.geometry().bounds())
        print("ee3")
        # coordinates = geoj["coordinates"]
        # aoi = ee.Geometry.Polygon(coordinates)
      # aoi = ee.Geometry.Polygon(coordinates).bounds()

    # If a tiny AOI is submitted, buffer it into a larger one for a more accurate analysis.
    # print("AOI", aoi)
    size_check = buffer_to_min(geoj)
    buff_val = size_check[0]
    meets_min = size_check[1]
    area = size_check[2]

    if not meets_min:
      try:
        aoi = aoi.buffer(buff_val)
      except:
        pass

    # aoi = aoi.buffer(-3)

    # Determine what the max allowable area is (the largest value that will render tiles). 
    # If FC area excceds max area, AND is an FC, run the analysis one by one on each polygon...

    # Initialize the dates from the request
    projdate = ee.Date(start_date)
    projdate_end = ee.Date(end_date)

    # Run the change detection algorithm and store the output in a variable
    output = analyze(aoi, projdate, projdate_end, 1, area, tries)

    # Retreieve a url for a tile to display for the aoi at the later date
    afterImg = output[2]
    afterImg = ee.data.getTileUrl(afterImg.getMapId({"bands": ["B4", "B3", "B2"], "min": 250, "max": 2500}), 8014,4817, 37)

    afterImg = afterImg[:-12] + "{z}/{x}/{y}"

    # Retreieve a url for a tile to display for the aoi at the earlier date
    beforeImg = output[1]
    beforeImgID = beforeImg.getMapId({"bands": ["B4", "B3", "B2"], "min": 250, "max": 2500})
    beforeImg = ee.data.getTileUrl(beforeImgID, 8014,4817, 37)
    beforeImg = beforeImg[:-12] + "{z}/{x}/{y}"

    # Retreieve a url for a tile to display the change polygons
    gee_geom = output[0]
    # This line seems to be responsible for the failures. In other words, requesting a mapID for an ee.featurecollection
    geom_map_id = gee_geom.getMapId({'palette':['purple'], 'min':1, 'max':1})
    changeImg = ee.data.getTileUrl(geom_map_id, 8014,4817, 37)
    changeImg = changeImg[:-12] + "{z}/{x}/{y}"
    # changeImg = beforeImg
    change_occured = output[3]
    print("\n\narea", area)
    print("tries", output[5])
    print("original_scale", output[6])
    print("scale", output[4], "\n\n")
    return JsonResponse({
        "changeImg": changeImg,
        "afterImg": afterImg,
        "beforeImg": beforeImg,
        "change_occured": change_occured,
        "poly": geoj
    })

class AOI(APIView):
  permission_classes = (permissions.AllowAny,)
  parser_classes = (FormParser, MultiPartParser)
  
  def get(self, req, format=None):
    species = req.query_params["species"]
    q_type = req.query_params["type"]
    if q_type == "species_range":
      data = get_species_range(species)
      data = data["data"]
      res = { "geometries": [], "speciesID": data[0][18]}
      for i in data:
          try:
              shp_file_path = i[15]["url"]
          except:
              shp_file_path = False
          if shp_file_path:
              polygons = online_shapefile_to_geojson(shp_file_path, species)
              res["geometries"].append(polygons)
    elif q_type == "critical_habitat":
      # returns feature collection containing multipolygon... Leaflet can't ingest multipolygons...
      res = get_species_critical_habitat(species)
      res = break_multis(res)
      try:
        res = break_multis(res[0])
      except:
        pass
      res = {"type": "FeatureCollection", "features": res}
    return Response(res)    

  def post(self, req, format=None):
    uploaded = req.data["file"]
    file_name = uploaded.name
    geojson = file_to_geojson_features(uploaded)
    return Response(geojson)

  def put(self, req, format=None):
    res = get_critical_habitat_species_list()
    return Response(res)

''