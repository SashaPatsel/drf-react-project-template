from accounts.models import Account
import os
from django.conf import settings
from osgeo import ogr, gdal, osr
from pyproj import Proj, transform
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from django.contrib.gis.gdal import GDALRaster
import numpy
import subprocess

def reproject_to_web_mercator(raster_path, reprojected_raster_path):
  """ Given a path to an exitsting tif file, and the path to a non-existent 'warped' file, this method reprojects a raster from any CRS to EPSG 3857 (web mercator), and returns the path to that reprojected image. """
  # Instantiate information to convert the Raster from EPSG 4326 to EPSG 3857
  src = rasterio.open(raster_path)
  # Desired CRS
  dst_crs = "EPSG:3857"    
  # Get new values to replaifce existing Raster profile
  src_crs = src.crs
  # If the image is already projected for web mercator 
  if src_crs == dst_crs:
      reprojected_raster_path = raster_path
  else:
      # Get reprojected data to make up profile of output image
      transformed, width, height = calculate_default_transform(src_crs, dst_crs, src.width, src.height, *src.bounds)
      kwargs = src.meta.copy()
      kwargs.update({
          'crs': dst_crs,
          'transform': transformed,
          'width': width,
          'height': height
       })
      # Create a new file with the raster projected to EPSG 3857
      with rasterio.open(reprojected_raster_path, 'w', **kwargs) as dst:
          for i in range(1, src.count + 1):
              reproject(
                  source=rasterio.band(src, i),
                  destination=rasterio.band(dst, i),
                  src_transform=src.transform,
                  src_crs=src.crs,
                  dst_transform=transform,
                  dst_crs=dst_crs,
                  resampling=Resampling.nearest)
      src.close()
  return reprojected_raster_path

def get_raster_min_max_nodata(raster_path):
  """ Given a path to a tif image, this method returns its minimum and maximum values unstreteched by nodata values. Additionally, it returns the nodata value itself """
  # Open for ratser info
  rasterio_image = rasterio.open(raster_path, mode="r+")
  # Retrieve value representing pixels meant to be rendered as transparent   
  nodata = rasterio_image.nodata
  # Gets an copy of the raster array, but with only binary options for data or nodata
  try:
      null_val = numpy.array(nodata, dtype=rasterio_image.profile["dtype"])
  except:
      null_val = numpy.array(nodata)
  # The actual dataset
  matrix = rasterio_image.read()
  # Instantiate original dataset in numpy array
  numpy_matrix = numpy.array(matrix)
  # Set all null values to equal False
  numpy_matrix[numpy_matrix == null_val] = False
  # Obtain the min value with null val excluded (to avoid unintended stretching)
  rast_min = str(numpy.nanmin(numpy_matrix).item())
  # Obtain the max value with null val excluded (to avoid unintended stretching) 
  rast_max = str(numpy.nanmax(numpy_matrix).item())
  rasterio_image.close()
  return rast_min, rast_max, str(nodata)

def tif_to_png(nodata, rast_min, rast_max, tif_path, png_path):
  """ Given the path to a tif file, this method uses that file to create a new PNG. All PNGs are forced to UInt16 datatype, and have their colors appropriately scaled. """
  # Convert the warped raster to a PNG
  subprocess.call(["gdal_translate", "-ot", "UInt16", "-a_nodata", nodata, "-of", "PNG", "-scale", rast_min, rast_max, "0", "65535", tif_path, png_path])

def get_raster_bounds(raster_path):
  """ Given a path to a raster file, this method returns its bounds for a web mercator map. """
  # Open the warped raster in order to get its boundbox
  raster = GDALRaster(raster_path)
  # Define 4326 as the crs we want our bounds in (even though leaflet projects images to EPSG 3857, it takes in bounds from EPSG 4326)  
  inProj = Proj(init='epsg:3857')
  outProj = Proj(init='epsg:4326')
  # Get bounding box coordinates 
  x1 = raster.extent[0]
  y1 = raster.extent[1]
  x2 = raster.extent[2]
  y2 = raster.extent[3]
  # Convert the boundbox to EPSG 4326 for Leaflet projection
  coords1 = transform(inProj, outProj, x1, y1)
  coords2 = transform(inProj, outProj, x2, y2)
  # Store coordinates as a string separated by a space so they can be easily stored in a database   
  coords1 += coords2
  coordinates = ""
  for i in coords1:
      coordinates += repr(i) + " "
  return coordinates


def process_raster(file_path, path_tail, rm_extra_files=False):
  """ Given a database instance and a path to a tif file, this method reprojects, recolors, and returns the bounds of that file as well as its new path. Additionally, a PNG to be projected to a Leaflet map. """
  raster_filename = file_path
  raster_filename = raster_filename.split(".tif")
  raster_filename = raster_filename[0]
  path_tail = path_tail.replace("/media", "") 
  image_in = settings.MEDIA_ROOT + path_tail
  # Create paths/names for reprojection file, recoloring file, and png file
  if file_path.endswith("tiff"):
      # PNG
      image_out = image_in[:-4]
      # Image to be warped to new projection
      image_warped = image_out[:-1] + "warped."
      image_out += "png"
      image_warped += "tiff"
  elif file_path.endswith("tif"):
      image_out = image_in[:-3]
      image_warped = image_out[:-1] + "warped."
      image_out += "png"
      image_warped += "tif"

  image_warped = reproject_to_web_mercator(image_in, image_warped)

  rast_min, rast_max, nodata = get_raster_min_max_nodata(image_warped)

  tif_to_png(nodata, rast_min, rast_max, image_warped, image_out)

  coordinates = get_raster_bounds(image_warped)

  # Remove the old files
  if rm_extra_files:
    raster = None
    xml_file = image_out + ".aux.xml"
    os.remove(image_in)
    os.remove(image_warped)
    try:
        os.remove(xml_file)
    except:
        pass
  return coordinates, raster_filename
