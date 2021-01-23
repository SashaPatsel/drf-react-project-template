
import ee

from datetime import datetime
from . import clouds
from . import iw
from . import MAD_mc
from . import stats
from . import terrain
from . import dictionaries
from backend.utils.math import round_to_nearest_ten
import sys
import os
import requests
import json
from pprint import pprint
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
counter = 0 

# Initialize Earth Engine

CDL = ee.Image("USDA/NASS/CDL/2017")
S2 = ee.ImageCollection("COPERNICUS/S2")
SR = ee.ImageCollection("COPERNICUS/S2_SR") 
DEM = ee.Image("USGS/SRTMGL1_003")

def mask(img):
    scored = clouds.basicQA(img)
    scored = clouds.sentinelCloudScore(scored)
    waterMask = clouds.waterScore(img).select('waterScore').lte(0.5)
    shadowMask = img.select('B11').gt(900)
    return scored.updateMask(scored.select('cloudScore').lte(15).And(shadowMask).And(waterMask))

def sz(ft):
    area = ft.area(5)
    return ft.set({'area': area})

def displaySize(size):
    print('size:', size)

def analyze_iw(aoi, doi, dictionary, size, aoiId):
    """
    Function that pre-processes sentinel-2 imagery and runs the LCC change detection algorithm
    
    Parameters:
        aoi(ee.Feature): area of interest with property 'landcover'
        doi(ee.Date): date of interest
        dictionary (ee.Dictionary):
        size (float): minimum size (ac) of changes to output
        aoiId (str): unique identifier for the area of interest
        
    Returns:
        tuple: ee.FeatureCollection with properties 'id', and 'landcover',
        ee.Image with bands
    """
    # cast dictionary to ee.Dictionary for use in subsequent GEE ops
    dictionary = ee.Dictionary(dictionary)
    # grab the landcover property from aoi and then cast to geometry
    lc = ee.Feature(aoi).get('landcover')
    aoi = aoi.geometry()
    
    # function to add unique id and landcover type to output feature properties
    
    def add_props(ft):
        global counter
        try:
            ftId = aoiId + '_' + ft.id().getInfo() 
            print("ftId", ftId)
        except:
            print("fttype", type(ft.id()))
            # ftId = aoiId + '_' + ft.id()
            str_counter = str(counter)
            print("counta", str_counter)
            ftId = aoiId + '_' + str_counter
            counter += 1
        return ft.set('id', ftId, 'landcover', lc)

    try:
        sq_meters = ee.Number(size).multiply(4047)
        projdate = ee.Date(doi);
        today = projdate.advance(3, 'month');
    
        proj_dt = str(datetime.fromtimestamp(int(projdate.getInfo()['value']) / 1e3))[:10]
        print('proj_dt:', proj_dt)
        prior = ee.Date.fromYMD(projdate.get('year').subtract(1), projdate.get('month'), projdate.get('day'))
        prior_dt = str(datetime.fromtimestamp(int(prior.getInfo()['value']) / 1e3))[:10]
        print('prior_dt:', prior_dt)

        rgbn = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']

        masked = S2.filterDate(prior, today).filterBounds(aoi).map(mask)
        corrected = terrain.c_correct(masked, rgbn, aoi, DEM)

        after = corrected.filterDate(projdate, today)
        count = after.size()
        #print('after size:', count.getInfo())
        reference = after.sort('system:time_start', False)
        time0 = ee.Image(reference.first()).get('system:time_start')
        recent_date = str(datetime.fromtimestamp(int(time0.getInfo()) / 1e3))[:10]

        before = corrected.filterDate(prior, projdate)
        count = before.size()
        print('before size:', count.getInfo())
        reference = before.sort('system:time_start', False)
        time0 = reference.first().get('system:time_start')
        past_date = str(datetime.fromtimestamp(int(time0.getInfo()) / 1e3))[:10]
 
        # run the IW algorithm between the before and after collections within the user defined AOI.
        # by default, ag fields are masked by 'yes'
        print('running the iw algorithm')
        iwout = iw.runIW(before, after, aoi, 'yes').clip(aoi)

        # calculate LDA score to discriminate change/no-change pixels in iwout.  Requires thresholds from habitat dictionary        
        scored = stats.ldaScore(
                iwout,
                ['cv_z', 'rcvmax_z', 'ndvi_z', 'ndsi_z', 'ndwi_z', 'nbr_z'],
                dictionary)
        
#        scored = stats.ldaScore(iwout, 0 ['cv_z', 'rcvmax_z', 'ndvi_z', 'ndsi_z', 'ndwi_z', 'nbr_z'],
#                                [cvz, rcvz, ndviz, ndsiz, ndwiz, nbrz]).clip(aoi)

        # create a binary [0, 1] image representing change and no-change pixels.  Erode and dilate changed areas
        selected = scored.gte(dictionary.get('lda').getInfo())\
        .focal_min(1, 'square', 'pixels')\
        .focal_max(1, 'square', 'pixels')

        # mask image to retain only pixels equal to '1'
        selected = selected.updateMask(selected)
        #maskSelected = selected.updateMask(selected.eq(0))
        # mask out no-change areas (i.e. selected = 0) here.  Creates fewer polygons which should save memory
        # selected = selected.updateMask(selected.eq(1))
        #print('selected is a ', type(selected))

        scale = 10
        tileScale = 6
        
        # convert binary image to polygons.  Note: this creates polygons for both contiguous change and contiguous no-change areas
        polys = selected.reduceToVectors(
            geometry=aoi,
            scale=scale,
            tileScale=tileScale,
            eightConnected=True,
            bestEffort=True,
            maxPixels=1e13)

        print('polys is a ', type(polys))
        try: 
            print("len", len(polys))
        except:
            print("no len")
        count = polys.size()
        #print('polys size:', count.getInfo(displaySize))

        # return only polygons corresponding to change pixels
        polys = polys.map(sz).map(add_props)
        # ft.id().getInfo() 
        # filter out change polygons smaller than the user defined minimum area
        polys = polys.filter(ee.Filter.gte('area', sq_meters))
        print("polt", type(polys))
        # indicator = True

        return "OK", past_date, recent_date, polys, iwout.select([
                'cv_z', 'nbr_z', 'ndsi_z', 'ndwi_z', 'ndvi_z', 'rcvmax_z'])
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print ("")
        print ("*******************************")
        print ("Unexpected error in analyze.py")
        print (exc_type, fname, exc_tb.tb_lineno)
        #print("sys.exc_info:", sys.exc_info()[0])
        print ("Error:", error)
        print ("*******************************")
        print ("")
        return "error"


# HABITAT PATROL
def analyze(aoi, prior_date, end_date, size, area, tries):
    """
    Function that pre-processes sentinel-2 imagery and runs the LCC change detection algorithm
    
    Parameters:
        aoi(ee.Feature): area of interest with property 'landcover'
        doi(ee.Date): date of interest
        dictionary (ee.Dictionary): appropriate dictionary of lda coefficients
        size (float): minimum size (ac) of changes to output
        aoiId (str): unique identifier for the area of interest
        
    Returns:
        tuple: ee.FeatureCollection with properties 'id', and 'landcover',
        ee.Image with bands
    """
    lc = ee.Feature(aoi).get('mode')
    def add_props(ft):
        ftId = str(0) + '_' + '1'
        return ft.set({'id': ftId, 'landcover': lc})

    try:
        sq_meters = ee.Number(size).multiply(4047)
        # projdate = ee.Date(doi);
        projdate = prior_date
        today = end_date
        # 
        today_dt = str(datetime.fromtimestamp(int(today.getInfo()['value'])/1e3))[:10]
        # 
        proj_dt = str(datetime.fromtimestamp(int(projdate.getInfo()['value']) / 1e3))[:10]
        prior = ee.Date.fromYMD(projdate.get('year').subtract(1), projdate.get('month'), projdate.get('day'))
        prior_dt = str(datetime.fromtimestamp(int(prior.getInfo()['value']) / 1e3))[:10]

        rgbn = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']
        
        filtered = S2.filterDate(prior, today).filterBounds(aoi)

        end_date_year = projdate.get('year').getInfo()


        if(prior.get('year').getInfo() >= 2019):
            masked = SR.filterDate(prior, today).filterBounds(aoi).map(clouds.maskSR)
        elif(today.get('year').getInfo() >= 2019):

            s2 = S2.filterDate(prior, '2018-12-25').filterBounds(aoi).map(clouds.maskTOA)
            sr = SR.filterDate('2018-12-26', today).filterBounds(aoi).map(clouds.maskSR)
            masked = s2.select(rgbn).merge(sr.select(rgbn))
        else:
            masked = S2.filterDate(prior, today).filterBounds(aoi).map(clouds.maskTOA)


        corrected = terrain.c_correct(masked, rgbn, aoi, DEM)

        after = corrected.filterDate(projdate, today)
        count = after.size()
        reference = after.sort('system:time_start', False)
        time0 = ee.Image(reference.first()).get('system:time_start')
        before = corrected.filterDate(prior, projdate)
        count = before.size()

        reference = before.sort('system:time_start', False)
        time0 = reference.first().get('system:time_start')
 
        # Scaling scale
        max_sampling = 1000000

        scale = round_to_nearest_ten(area / max_sampling)
        original_scale = scale
        if scale < 1:
            scale = 10

        if tries is 2:
            # scale = 10
            scale = area / 18256 

        elif tries is 3:
            scale = area / 7180

        elif tries is 4:
            # scale += 200
            scale = scale * 250
            
        elif tries is 5:
            # scale += 200
            scale = scale * 500
            
        elif tries is 6:
            # scale += 200
            # 190000.0 worked!
            scale = scale * 1000
        elif tries is 7:
            # scale += 200
            # 190000.0 worked!
            scale = scale * 5000    
        elif tries is 8:
            # scale += 200
            # 190000.0 worked!
            scale = scale * 10000 
        elif tries is 9:
            # scale += 200
            # 190000.0 worked!
            scale = scale * 20000 
        elif tries is 10:
            # scale += 200
            # 190000.0 worked!
            scale = scale * 100000


        # run the IW algorithm between the before and after collections within the user defined AOI.
        iwout = iw.runIW(before, after, aoi, scale, 'yes').clip(aoi)

        # Use the AOI to determine the most common occuring landscape.
        nlcd = ee.Image("USGS/NLCD/NLCD2016").clip(aoi)
        landcover = nlcd.select("landcover")
        mask = landcover.gt(24).And(landcover.neq(82)).And(landcover.neq(81))
        lc = landcover.updateMask(mask)
        beforeImg = before.median()
        afterImg = after.median()

        scrubScore = stats.ldaScore(iwout, ['cv_z', 'nbr_z', 'ndsi_z', 'ndvi_z', 'ndwi_z', 'rcvmax_z'], dictionaries.scrub)

        forScore = stats.ldaScore(iwout, ['cv_z', 'nbr_z', 'ndsi_z', 'ndvi_z', 'ndwi_z', 'rcvmax_z'], dictionaries.forest)

        grassScore = stats.ldaScore(iwout, ['cv_z', 'nbr_z', 'ndsi_z', 'ndvi_z', 'ndwi_z', 'rcvmax_z'], dictionaries.grassland)

        desScore = stats.ldaScore(iwout, ['cv_z', 'nbr_z', 'ndsi_z', 'ndvi_z', 'ndwi_z', 'rcvmax_z'], dictionaries.desert)

        wetScore = stats.ldaScore(iwout, ['cv_z', 'nbr_z', 'ndsi_z', 'ndvi_z', 'ndwi_z', 'rcvmax_z'], dictionaries.wetland)
        
        scored = forScore.where(landcover.eq(52), scrubScore).where(landcover.eq(71), grassScore).where(landcover.eq(31), desScore).where(landcover.eq(90).Or(landcover.eq(95)), wetScore)

        # selected = scored.gte(2)
        selected = scored.gte(3)

        selected = selected.updateMask(selected)

        change_occured = True
        polys = selected

        return polys, beforeImg, afterImg, change_occured, scale, tries, original_scale


    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print ("")
        print ("*******************************")
        print ("Unexpected error in analyze.py")
        print (exc_type, fname, exc_tb.tb_lineno)
        #print("sys.exc_info:", sys.exc_info()[0])
        print ("Error:", error)
        print ("*******************************")
        print ("")
        return "error"

def analyze_mad(aoi, doi, size, niters):
    iterations = niters
    # service_account = config.EE_ACCOUNT
    # credentials = ee.ServiceAccountCredentials(service_account, config.EE_PRIVATE_KEY_FILE)
    # ee.Initialize(credentials)
    sq_meters = ee.Number(size).multiply(4047)
    projdate = ee.Date(doi);
    today = projdate.advance(3, 'month');
    #projdate = ee.Date(doi)
    #today = ee.Date(datetime.now())
    #today = ee.Date('2018-11-01')
    
    prior = projdate.advance(-1, 'year')
    
    rgbn = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']
    
    nbands = len(rgbn)
    print(nbands)
    
    masked = ee.Algorithms.If(doi.gte(ee.Date('2019-01-01')),
                 S2.filterDate(prior, today).filterBounds(aoi).map(clouds.maskS2SR),
                 S2.filterDate(prior, today).filterBounds(aoi).map(clouds.mask))

    corrected = terrain.c_correct(masked, rgbn, aoi, DEM)

    after = corrected.filterDate(projdate, today)
    image2 = after.median().select(rgbn)
    
    before = corrected.filterDate(prior, projdate)
    image1 = before.median().select(rgbn)
    
    image = image1.addBands(image2).clip(aoi)
    
    npix = image.select(0).reduceRegion(
            reducer = ee.Reducer.count(),
            geometry = aoi,
            scale = 10,
            maxPixels = 1e13,
            tileScale = tileScale).get('B2')
    
    inputlist = ee.List.sequence(1, iterations)
        
    first = ee.Dictionary({
            'done':ee.Number(0),
            'image': image,
            'allrhos': [ee.List.sequence(1, nbands)],
            'chi2': ee.Image.constant(1),
            'MAD': ee.Image.constant(0),
            'size': npix})
    output = ee.Dictionary(inputlist.iterate(MAD_mc.imad, first))
    return output

