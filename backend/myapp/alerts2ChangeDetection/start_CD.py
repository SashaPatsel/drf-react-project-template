import json
import ee
import db
import utils
from google.cloud import storage
import os
import requests
from datetime import date
import analyze
# import cd_ndvi
# import cd_mad
# import cd_test
# import cd_ndvi_test
#import rys_ndvi
from datetime import datetime,timedelta
import time
#import image_diff
import config


# uncomment to see debugging
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

storage_client = storage.Client()

feature_sum = 0

def test_EE():
    # Initialize the Earth Engine object, using the authentication credentials.
    #ee.Initialize()
    # service_account = config.EE_ACCOUNT
    # credentials = ee.ServiceAccountCredentials(service_account, config.EE_PRIVATE_KEY_FILE)
    # ee.Initialize(credentials)
    # Just to make sure the API works:
    # Print the information for an image asset.
    image = ee.Image('srtm90_v4')
    # print(image.getInfo())

def display_rows(rows):
    rowNum=0
    for row in rows:
        rowNum += 1
        # request_id = row[0]
        # start_date = str(row[1])
        # aoi_descr = row[3]
        # geo_json = row[4]
        # email = row[5]
        # request_status = row[6]
        # last_image_id = row[7]
        # last_image_date = row[8]
        # cd_code = row[9]
        # cvz = row[10]
        # rcvz = row[11]
        # ndviz = row[12]
        # ndwiz = row[13]
        # ndsiz = row[14]
        # nbrz = row[15]
        # size = row[16]
        # intercept = row[17]
        # lda = row[18]
        # pval = row[19]
        # cloud_percent = row[20]
        # cd_id = row[21]
        # print (cd_id, " requestid:" + str(request_id) + " startdate:" + str(start_date), \
        #        " aoi_descr:" + aoi_descr, " changeDectionType:" + cd_code, " lda:" + str(lda), " intercept:" + str(intercept))
        # This is DoW test geometry.
        # geo_json = '{"type":"Polygon","coordinates":[[[-103.106689453125,32.05697250541851],[-103.08197021484375,31.966143862120095],' \
        #     '[-102.952880859375,32.00574690121464],[-102.9803466796875,32.07326555104239],[-103.106689453125,32.05697250541851]' \
        #     ']]}'

        #var forest = ee.Dictionary({
        #   'int': 0,//-1.2,
        #   'cvz': 0.0146716,//0.086286,
        #   'rcvz': -0.1817549,//-0.812,
        #   'ndviz': 0.3393854,//-0.307,
        #   'ndsiz':  0.1291063,//0.12125,
        #   'ndwiz':  -0.0334060,//0.0893477,
        #   'nbrz': 0.2112095,//0.2058,
        #   'thresh': 5
        # });

        # From Mike email on Mar 23
        # cv_z      0.009574808
        #
        # nbr_z    -0.024011919
        #
        # ndsi_z   -0.636140757
        #
        # ndvi_z    0.746331633
        #
        # ndwi_z    0.291122435
        #
        # rcvmax_z  0.945162260
        #
        # intercept         0.77898
        #
        # lda                  -1.88*
        id = row[0]
        geo_json = row[1]
        # print('geo_json:', geo_json)
        geo_js = json.loads(geo_json)
        # print('geo_json:', geo_js['coordinates'])
        aoi  = ee.Geometry.Polygon(geo_js['coordinates'])
        # print('aoi:', aoi)
        start_date = '2019-01-28'
        #SELECT sub.id, ST_AsGeoJSON(sub.geom), master.cvz, master.rcvz,
        # master.ndviz, master.ndwiz, master.ndsiz, master.nbrz,
        # master.int, master.thresh, master.cd_name FROM img_cdrequest req
        # JOIN "RSSEmailSubscription" sub on req.subscription_id = sub.id
        # JOIN img_cdmaster master on req.cd_id_id=master.cd_id
        # WHERE req.status='active'

        # 'int': 0,
        # 'cvz': 0.0146716,
        # 'rcvz': -0.1817549,
        # 'ndviz': 0.3393854,
        # 'ndsiz': 0.1291063,
        # 'ndwiz': -0.0334060,
        # 'nbrz': 0.2112095,
        # 'thresh': 5

        cvz = row[2] #0.0146716
        rcvz = row[3] #-0.1817549
        ndviz = row[4] #0.3393854
        ndwiz = row[5] #-0.0334060
        ndsiz = row[6] #0.1291063
        nbrz = row[7] #0.2112095
        size = 3 #1
        intercept = row[8] #None # is this the same as 'int' ? Not needed in analyze.py, so possibly delete
        thresh = row[9] #.1 #-1.88 #5
        geojson_file=id + '_' + str(datetime.now())[:16]
        geojson_file = geojson_file.replace(' ','_')
        print('geojson_file:', geojson_file)
        #ndwiz = 1.5
        #intercept = 1
        #lda = 4
        # if(cd_code == 'rys_ndvi'):0
        #     return_values = rys_ndvi.ndviChangeDetection(aoi, start_date, ndviz, size, cd_id)
        # if(cd_code == 'ndvi_test'):
        #     return_values = cd_ndvi_test.runIW(aoi, start_date, cvz, rcvz, ndviz, ndsiz, nbrz, size, cd_id)
        # if(cd_code == 'ndvi'):
        #     return_values = cd_ndvi.runIW(aoi, start_date, cvz, rcvz, ndviz, ndsiz, nbrz, size, cd_id)
        # if (cd_code == 'iw'):
        #def analyze(aoi, doi, cvz, nbrz, ndsiz, ndviz, ndwiz, rcvz, intercept, size, lda, cd_id):
        return_values = analyze.analyze(aoi, start_date, cvz, rcvz, ndviz, ndwiz, ndsiz, nbrz, size, intercept, thresh,
                                        geojson_file)
        # if(cd_code == 'mad'):
        #     #return_values = cd_mad_copy.my_function() #aoi, '2017-07-01', pval, size, cd_id)
        #     return_values = cd_mad.runMAD(aoi, start_date, pval, size, cd_id)
        #num_change_detected = return_values[0]
        #print (cd_id, ' num_change_detected:' + str(num_change_detected))
        if return_values[0] == "OK":
            print('past_date:', return_values[1])
            print('recent_date:', return_values[2])
            #save_fc(return_values[3], geojson_file)
            cd_descr = return_values[4]
            mouse_over = return_values[5]
            subscription_id = id
            post_cd(geojson_file, cd_descr, subscription_id, mouse_over)
            #print(make_GeoJSON((return_values[2])))
            # if (num_change_detected > 0):
            #     #print cd_id, ' return_values:' + str(return_values)
            #     feature_collection = return_values[5]
            #     #features = make_GeoJSON(feature_collection)
            #     #features = json.dumps(feature_collection)
            #     return_image1 = return_values[1]
            #     img_date = return_values[3]
            #     image_name = 'req' + str(request_id) + '__' + img_date
            #     save_image(return_image1, img_date, request_id, '', image_name)
            #     compare1_image = image_name
            #     print (cd_id, ' image_name1: ' + image_name)
            #     return_image2 = return_values[2]
            #     img_date = return_values[4]
            #     image_name = 'req' + str(request_id) + '__' + img_date
            #     compare2_image = image_name
            #     current_timestamp = time.time()
            #     datetime_ts = datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            #     geojson_file = compare1_image + "___" + compare2_image + "___" + cd_code + "___" + datetime_ts.replace(' ','_') # + '.geojson'
            #     print (cd_id, ' geojson_file: ' + geojson_file)
            #     save_fc(feature_collection, geojson_file)
            #     geojson_file += 'ee_export.geojson'
            #     save_image(return_image2, img_date, request_id, geojson_file, image_name)
            #     num_vectors = 0
            #     db.save_createdcd(request_id, geojson_file, compare1_image, compare2_image, num_vectors, cd_code, cvz, rcvz,
            #                       ndviz, ndwiz, ndsiz, nbrz, size, intercept, lda, pval)
            #     print cd_id, ' image_name2: ' + image_name
            #     save_images = True
            #     #image_diff.diff_image(compare1_image, compare2_image, save_images)
            #     #
            #     # don't use save_geo_json
            #     #save_geo_json(feature_collection, image_name); use save_fc instead.
            #     #
            #     if (image_name != 'not a valid image'):
            #         db.update_request(request_id, 'change detected')
            # else:
            #     db.update_request(request_id, 'checked')
            # print cd_id, " Finished requestid:" + str(request_id) + " aoi_descr:" + aoi_descr + " changeDectionType:" + cd_code
            # Comment break out to test with just the first returned row
            #break

def post_cd(geojson_file, cd_descr, subscription_id, mouse_over):
    print('here geojson_file:', geojson_file)
    post_fields = {'geojson_file': geojson_file,
                   'cd_descr': cd_descr,
                   'subscription_id': subscription_id,
                   'mouse_over': mouse_over}
    #url = 'https://skytruth-alerts2.appspot.com/api/insert_cd/'
    url = 'https://skytruth-alerts2.appspot.com/api/post_cd/'
    response = requests.post(url, data=post_fields)
    print(response.content)

def get_feature_sum(feat):
  return ee.Feature(feat).get('sum')

def save_fc(feature_collection, geojson_file):
    print('geojson_file:', geojson_file)
    print('feature_collection:', type(feature_collection))
    #print(feature_collection.toList(1000).map(get_feature_sum).getInfo())

    # path = 'downloads/' + geojson_file
    # # Download the URL image
    # if os.path.exists(path):
    #     os.remove(path)
    # #result = requests.get(URL)
    # f = open(path, 'wb')
    # #for chunk in result.iter_content(chunk_size=512 * 1024):
    # ##    # filter out keep-alive new chunks
    # #    if chunk:
    # f.write(feature_collection)
    # f.close()
    # #download(URL, path)
    # # and upload to thumbnails in alerts-storage
    # #__upload_file_to_storage_bucket("alerts-storage", path, "geojson", geojson_file)

    task_keyed = ee.batch.Export.table.toCloudStorage(
        collection=feature_collection,
        description=geojson_file,
        fileFormat= 'GeoJSON',
        bucket='alerts-storage',
        path='geojson/' + geojson_file
    )
    task_keyed.start()

def read_feature(feature):
    print (feature.get("geometry"))
    print (feature.serialize())
    #print (feature.geometry.coordinates)

def make_GeoJSON(feature_collection):
    new_GeoJSON = '{"type": "FeatureCollection", "features": ['
    #feature_collection.map(read_feature)
    #print (feature_collection.serialize())
    #feature_collection.iterate(read_feature)

    def addToList(feature, features):
        return ee.List(features).add(ee.Dictionary({
            "geometry": feature.geometry()}))

    #features = feature_collection.iterate(addToList, [])
    # print feature_collection.getInfo()
    #print(feature_collection.getInfo().length())
    #returnit = (feature_collection.toDictionary().serialize())
    #returnit = feature_collection.serialize() #new_GeoJSON #(feature_collection.getInfo())
    returnit = feature_collection.getInfo()
    return json.dumps(returnit)

def save_image(image, img_date, request_id, geo_json, image_name):
    img_date = img_date.replace("-","_")
    # bandNames = image.bandNames()
    # print('Band names: ' + str(bandNames.size()))
    js = image.getInfo()
    print('js:' + str(js['properties']['system:footprint']))
    # print ('')
    #print ('getMap:' + str(image.getMap()))
    #image_name = 'not a valid image'
    #try:
    #    image_name = js['id']
    #except:
        #print ('not a valid image')
        #image_name = 'req' + str(request_id) + '__' + img_date
    #return image_name
    if (image_name != 'not a valid image'):
        count = db.read_saved_count(image_name)
        print "  image count:" + str(count)
        if count < 1:
            try:
                cloud_cover = js['properties']['CLOUD_COVERAGE_ASSESSMENT']
            except:
                cloud_cover = '0'
            my_geom = utils.__convert_json_to_text(str(js['properties']['system:footprint']['coordinates']))
            #my_geom = ''
            dt = img_date #image_name[14:22]
            image_id = db.__add_image_to_db("EE", image_name, dt, my_geom, cloud_cover, "COPERNICUS/S2",
                                            "type", "new", geo_json)
            id = db.__add_image_to_requestimages(image_id, request_id)
            tileset = image_name #[14:]
            # Export the tiff image to Cloud Storage.
            # Comment this out if you need to keep tiff file
            # task_config = dict(image=image, description='TIFFimage', bucket='alerts-storage',
            #                fileNamePrefix=image_name)
            # task = ee.batch.Export.image.toCloudStorage(image=task_config['image'], description=task_config['description'],
            #                                         bucket=task_config['bucket'],
            #                                         fileNamePrefix=task_config['fileNamePrefix'],
            #                                         maxPixels=150000000)
            # task.start()

            # Create the thumbnail.
            # Start by creating a visualization

            visual_image = image.visualize(min=0, max=3000, bands='B2,B3,B4', gamma=1.0) #, format='png')
            # for now, don't create the thumbnail...
            '''
            # Get the png file URL. -- You can change dimensions on thits if needed.
            URL = visual_image.getThumbUrl()
            path = 'downloads/' + image_name + '.png'
            # Download the URL image
            download(URL, path)
            # and upload to thumbnails in alerts-storage
            __upload_file_to_storage_bucket("alerts-storage", path,
                                            "thumbnails", image_name + '.png')
            '''

            # Export a tileset
            config = dict(
                image=visual_image,
                bucket='alerts-storage',
                maxZoom=14,
                description=tileset,
                region=js['properties']['system:footprint']['coordinates'],
                maxPixels=200000000,
                fileFormat='png',
                path='tileset/' + tileset)
            task_keyed = ee.batch.Export.map.toCloudStorage(
                image=config['image'],
                bucket=config['bucket'],
                path=config['path'],
                description=config['description'], fileFormat=config['fileFormat'],
                maxZoom=config['maxZoom'], region=config['region'],
                maxPixels=config['maxPixels'])
            task_keyed.start()
    return image_name

def download(URL, path_out):
    if os.path.exists(path_out):
        os.remove(path_out)
    result = requests.get(URL)
    f = open(path_out, 'wb')
    for chunk in result.iter_content(chunk_size=512 * 1024):
        # filter out keep-alive new chunks
        if chunk:
            f.write(chunk)
    f.close()

def __upload_file_to_storage_bucket(bucket_name, source_image_path, bucket_folder_name, file_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob_name = (bucket_folder_name + "/" + file_name).replace("//","/") #__get_filename_from_path(path=image_path)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_image_path)
    url = 'gs://' + bucket_name + '/' + blob_name
    return url

def save_geo_json(features, image_name):
    task_geo = ee.batch.Export.table.toCloudStorage(
        collection=features,
        description='GeoToStorage',
        bucket='alerts-storage',
        fileNamePrefix='GeoJSON/' + image_name,
        fileFormat='GeoJSON'
    )
    task_geo.start()

def get_features(aoi):
    dims = aoi["coordinates"]
    pt1 = dims[0][1]
    pt2 = dims[0][2]
    pt3 = dims[0][3]
    returnit = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[' \
               + str(pt1).replace(" ","") + ',' + str(pt2).replace(" ","") + ',' \
               + str(pt3).replace(" ","") + ',' + str(pt1).replace(" ","") + ']]}}]}'
    return returnit

def create_GeoJSON():
    geometry = ee.Geometry.Polygon(
        [[[-103.10365477432623, 32.01438101485287],
          [-103.042129867239, 31.902274302824058],
          [-102.98352153673954, 31.90081017201704],
          [-102.9571941679389, 31.913308768646484],
          [-102.93552070509918, 31.91024728844159],
          [-102.92742467899319, 31.915873649494397],
          [-102.92123346678125, 31.923274918095142],
          [-102.91042476773987, 31.90471429734437],
          [-102.91958234235153, 31.958271911788167],
          [-102.9570861430027, 32.00040818667322],
          [-103.00451655764022, 32.01250376789874],
          [-103.02654914768448, 32.03564779218852],
          [-103.07626752955048, 32.072521908690945]]])
    print("geometry:" + str(geometry))
    task_geo = ee.batch.Export.table.toCloudStorage(
        collection=geometry,
        description='GeoJSONExample',
        bucket='alerts-storage',
        fileNamePrefix='GeoJSON_1',
        fileFormat='GeoJSON'
    )
    task_geo.start()

def run_EE_for_cd(cd_id):
    print 'here'
    rows = db.read_requests(cd_id)
    print 'after'
    display_rows(rows)
    #test_EE()
    #create_GeoJSON()

if __name__ == '__main__':
    rows = db.read_new_requests()
    print('rows:', str(rows))
    display_rows(rows)
