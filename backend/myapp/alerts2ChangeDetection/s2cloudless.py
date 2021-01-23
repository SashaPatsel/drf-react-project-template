# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:07:34 2019

@author: MEvans
"""

import s2cloudless
import numpy as np
import ee

# ee.Initialize()


S2 = ee.ImageCollection("COPERNICUS/S2")

#Define the Gadsden SC AOI
aoi = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Polygon(
                    [[[-80.81991758407679, 33.88836406786576],
                      [-80.82417447706393, 33.81222611807673],
                      [-80.71508881286002, 33.80919082945717],
                      [-80.72153527034902, 33.881822895147785]]]
                    ),
            {
              "system:index": "0"
            })])

projdate = ee.Date('2017-08-20')
today = projdate.advance(3, 'month')

collection = S2.filterBounds(aoi).filterDate(projdate, today)

test_img = collection.first()

# for this to work, need to convert a GEE image to an nparray
cloud_detector = S2PixelCloudDetector(threshold=0.4, average_over=4, dilation_size=2)
cloud_probs = cloud_detector.get_cloud_probability_maps(np.array(test_img))
cloud_masks = cloud_detector.get_cloud_masks(np.array(test_img))