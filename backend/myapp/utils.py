import math
import pyproj
from shapely.geometry import mapping
from shapely.ops import transform
from functools import partial
from rrm.utils import convert_to_shp

def buffer_to_min(coords):
  proj = pyproj.Proj(init='epsg:3857') 
  # print("coords", coords)
  try:
    shp = convert_to_shp(coords)[0]
    projected_area = transform(proj, shp).area
  except: 
    # Handles featurecollections
    projected_area = 0
    print(type(coords["features"]) == str, type(coords["features"]))
    for i in coords["features"]:
      shp = convert_to_shp(i)[0]
      try:
        polygon_area = transform(proj, shp).area
        projected_area += polygon_area 
      except:
        def _to_2d(x, y, z):
          return tuple(filter(None, [x, y]))

        shp = transform(_to_2d, shp)
        polygon_area = transform(proj, shp).area
        projected_area += polygon_area 
  # print("area", projected_area)
  min_area_m2 = 25000000
  diff = min_area_m2 - projected_area
  # If the user hasn't met the min size
  val = 0
  if diff > 0:
    val = math.sqrt(diff)
    val = val/2
  meets_min = True  
  if projected_area < min_area_m2:
    shp = shp.buffer(.001)
    projected_area = transform(proj, shp).area
    meets_min = False
  geoj = mapping(shp)
  return val, meets_min, projected_area



# WORKING
# {type: "Feature", properties: {…}, geometry: {…}}
# geometry: {type: "Polygon", coordinates:
# geoj {'type': 'MultiPolygon', 'coordinates': [(((-87.86692290267924, 34.76461989941619), (-87.86270245835051, 34.76809690774274), 
# AOI ee.FeatureCollection({


# NOT WORKING
# {type: "Feature", properties: {…}, geometry: {…}}
# geometry: {type: "Polygon", coordi
# geoj {'type': 'Polygon', 'coordinates': (((-115.23553916829427, 48.8433387732827), (-115.19971245534867, 48.884018778443995), (-115.19916411349827, 48.884699170521074), (-115.17772711349826, 48.91381617052107), (-115.17710368818184, 48.91477291661028), (-115.17659340389807, 48.91579449977091), (-115.16192340389807, 48.94990849977091), (-115.16163047015291, 48.95067489669164), (-115.16140135017775, 48.95146272818131), (-115.15513735017775, 48.97684172818131), (-115.15495502641906, 48.977765369149736), (-115.15486037175884, 48.97870206284932), (-115.1548


# ZOOM LEVEL WAS THE CULPRIT
# Working zoom levels:
# 2km


# SHOULD WE ONLY RUN THE PROGRAM ON THE LARGEST THREE POLYGONS IN AN AOI?