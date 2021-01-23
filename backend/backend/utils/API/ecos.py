import json
import requests

def get_species_range(species_scientific_name):
  """ Given a species' scientific name, this function returns a response from the ECOs API containing a path to shapefile which holds that species range. """
  data = requests.get(f"https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species/export?columns=%2Fspecies&filter=%2Fspecies%40sn%20%3D%20%27{species_scientific_name}%27")
  res = data.json()
  return res

def get_critical_habitat_species_list():
  """ This function returns a list of species who's critical habitat is searchable. """
  data = requests.get("https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species/export?format=json&columns=%2Fspecies%40cn%2Csn%2Cstatus%2Cdesc%2Clisting_date&sort=%2Fspecies%40cn%20asc%3B%2Fspecies%40sn%20asc&filter=%2Fspecies%2Fcrithab_docs%40crithab_status%20%3D%20'Final'")
  res = data.json()
  return res  

def get_species_critical_habitat(species_scientific_name):
  """ Given a species' scientific name, this function returns a response from the Arc GIS API containing a a species critical expressed in GeoJSON. """
  data = requests.get(f"https://services.arcgis.com/QVENGdaPbd4LUkLV/ArcGIS/rest/services/USFWS_Critical_Habitat/FeatureServer/1/query?where=sciname+%3D+%27{species_scientific_name}%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=")
  res = data.json()
  return res

def get_species_names():
  """ Get a lits of species scientific and common names from the ecos database. """
  data = requests.get(f"https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species/export")
  res = data.json()
  return res