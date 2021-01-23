# Import the Earth Engine Python Package
import ee
from datetime import datetime
from datetime import timedelta
import stats

# Initialize Earth Engine
# ee.Initialize()

# Import the Sentinel-2 image collection
S2 = ee.ImageCollection("COPERNICUS/S2")
CDL = ee.ImageCollection("USDA/NASS/CDL/2017")
DEM = ee.ImageCollection("USGS/SRTMGL1_003")
# Function to calculate normalized difference metrics and add bands to collections
# param img: multispectral image
# param NIR: band name corresponding to near-infrared spectrum reflectance
# param R: band name corresponding to red spectrum reflectance
# param G: band name corresponding to green spectrum reflectance
# param SWIR1: band name corresponding to shortwave infared 1
# param SWIR2: band name corresponding to shortwave infrared 2
# Return: image with bands ['ndvi', 'nbr', 'ndsi']
def ND(img, NIR, R, G, SWIR1, SWIR2):
    NBR = img.normalizedDifference([NIR, SWIR2]).rename(["nbr"])
    NDSI = img.normalizedDifference([G, SWIR1]).divide(img.select([NIR])).rename(["ndsi"])
    NDWI = img.normalizedDifference([G, NIR]).rename(["ndwi"])
    NDVI = img.normalizedDifference([NIR, R]).rename(["ndvi"])
    return img.addBands(NDVI).addBands(NDSI).addBands(NBR).addBands(NDWI)

# Function calculating 'change vector'
# param b: before image
# param a: after image
# param bnds: list of band names (typically R, G, B, NIR, SWIR1, SWIR2)
# Return: image with ['cv'] band
# b.select(bnds)
#                   .subtract(a
#                             .select(bnds))
#                   .pow(2)
# .reduce(ee.Reducer.sum())
# .rename(['cv'])
# );
# }
def CV(b, a, bnds, aoi):
    diff = b.select(bnds).subtract(a.select(bnds))
    diff_sd = diff.reduceRegion(
        reducer = ee.Reducer.stdDev(),
        geometry = aoi,
        scale = 30,
        maxPixels = 1e13).toImage(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    diff_mn = diff.reduceRegion(
        reducer= ee.Reducer.mean(),
        geometry= aoi,
        scale= 30,
        maxPixels= 1e13).toImage(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    return (diff.subtract(diff_mn).divide(diff_sd).pow(2).reduce(ee.Reducer.sum()).rename(['cv']))

# Function calculating 'relative change vector maximum'
# param b: before image
# param a: after image
# param bnds: list of band names (typically R, G, B, NIR, SWIR1, SWIR2)
# Return: image with ['rcvmax'] band
def rcvmax(b, a, bnds, aoi):
    diff = b.select(bnds).subtract(a.select(bnds))
    maxab = b.select(bnds).max(a.select(bnds)).pow(2)
    stat = diff.divide(maxab)
    diff_sd = diff.reduceRegion(
        reducer= ee.Reducer.stdDev(),
        geometry= aoi,
        scale= 30,
        maxPixels= 1e13).toImage(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']).divide(maxab)
    diff_mn = diff.reduceRegion(
        reducer= ee.Reducer.mean(),
        geometry= aoi,
        scale= 30,
        maxPixels= 1e13).toImage(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']).divide(maxab)
    return (stat.subtract(diff_mn).divide(diff_sd).reduce(ee.Reducer.sum()).rename(['rcvmax']))

# Function calculating changes in common band values between two images
# param b: before image
# param a: after image
# param bnds: list of band names to calculate differences between before and after
# Return: image with bands equal to common bands in b and a
def d(b, a, bnds):
    return b.select(bnds).subtract(a.select(bnds))

# Function(s) to rename bands.
# param string: the existing band name
# param descriptor: the additional text for the band names
# return: the newly renamed bands
def rnm_u(instring):
    newstring = ee.String(instring).cat('_mean')
    return(newstring)

def rnm_s(instring):
    newstring = ee.String(instring).cat('_sd')
    return(newstring)

def rnm_z(instring):
    newstring = ee.String(instring).cat('_z')
    return(newstring)

def rnm_p(instring):
    newstring = ee.String(instring).cat('_p')
    return(newstring)

# Function calculating z-score and p-value for all bands in a change image.
# param change: multiband image representing change in pixels values btwn time a and b
# param aoi: geometry restricting analysis
# param scl: numeric scale at which to sample image to calculate global mean/sd
# Return: image with 2(n) bands of original image storing z-scores and p-values
def calc_zp(change, aoi, scl):
    norm = change.select(['ndvi', 'ndsi', 'nbr', 'ndwi', 'rcvmax'])
    chi = change.select(['cv']).rename(['cv_z'])
    norm_bands = norm.bandNames()
    chi_bands = ['cv']
    bands = change.bandNames()
    # list = bands.getInfo()
    # print('begin calc_zp bands:', list)
    cat_mean = norm_bands.map(rnm_u)
    cat_sd = norm_bands.map(rnm_s)
    cat_p = norm_bands.map(rnm_p)
    cat_z = norm_bands.map(rnm_z)

    mean = change.select(norm_bands).reduceRegion(
        reducer=ee.Reducer.mode(),
        geometry=aoi,
        scale=scl,
        maxPixels=1e13).rename(norm_bands, cat_mean)

    sd = change.select(norm_bands).reduceRegion(
        reducer=ee.Reducer.stdDev(),
        geometry=aoi,
        scale=scl,
        maxPixels=1e13).rename(norm_bands, cat_sd)

    mystats = mean.combine(sd)
    img_z = norm.subtract(mystats.toImage(cat_mean)).divide(mystats.toImage(cat_sd)).rename(cat_z)
    np = stats.norm_p(img_z.abs()).multiply(2).rename(cat_p)
    #np = ee.Image.constant(1).subtract(img_z.abs().multiply(-1.65451).exp().add(1).pow(-1)).multiply(2).rename(ee.String().cat('_p'))



    cp = stats.chi_p(chi, 6).multiply(-1).add(1).rename(['cv_p'])
    return chi.addBands(img_z).addBands(np).addBands(cp)

# Function to iteratively reweight pixels of a chane image as per Nielsen 2007.
# Currently takes a number of iterations as argument, but want to
# update to use a single response metric threshold (e.g. total change in p)
# param change: multiband image representing change in pixels values btwn time a and b
# param aoi: geometry restricting analysis
# param niter: number of iterations to perform
# Return: image with 2(n) original image bands storing z-score and p-values from the final iteration.
def iw(change, aoi, niter):
    bands = change.bandNames()
    cat_p = bands.map(rnm_p)
    net = 1
    zs = calc_zp(change, aoi, 30)
    while net <= niter:
        dp = zs.select(cat_p).multiply(change).rename(bands)
        zs = calc_zp(dp, aoi, 30)
        net += 1
    return zs

# Function to run complete iteratively reweighted national landcover change analysis.
# param aoi: geometry restricting analysis
def runIW(before, after, aoi, ag):
    CDL = ee.Image("USDA/NASS/CDL/2017")
    DEM = ee.Image("USGS/SRTMGL1_003")

    demMask = DEM.select(['elevation']).lte(3500)
    agMask = CDL.select(['cultivated']).eq(1)
    rgbn = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']

    recent = after.median().clip(aoi)

    recent = ee.Image(
        ee.Algorithms.If(ag == 'yes', recent.updateMask(agMask.And(demMask)), recent.updateMask(demMask)))

    past = before.median().clip(aoi)

    past = ee.Image(
        ee.Algorithms.If(ag == 'yes', past.updateMask(agMask.And(demMask)), past.updateMask(demMask)))

    now = ND(recent, 'B8', 'B4', 'B3', 'B11', 'B12')  # 'B4', 'B3', 'B2', 'B8', 'B11') #
    old = ND(past, 'B8', 'B4', 'B3', 'B11', 'B12')  # 'B4', 'B3', 'B2', 'B8', 'B11') #

    # CREATE IMAGE WITH BANDS FOR CHANGE METRICS CV, RCV, NDVI, NBR, NDSI
    # Calculate cv from before and after images
    cv = CV(old, now, rgbn, aoi)

    # Calculate rcv from before and after images
    rcv = rcvmax(old, now, rgbn, aoi)

    # Calculate combined normalized difference metrics from before and after images
    diff = d(old, now, ['ndvi', 'ndsi', 'ndwi', 'nbr'])

    # Combine cv, rcv, and normalized difference images into single image
    change = cv.addBands(rcv).addBands(diff)

    # zchange not used, but still need to call zp
    zchange = calc_zp(change, aoi, 30)

    iwchange = iw(change, aoi, 10)

    return iwchange
