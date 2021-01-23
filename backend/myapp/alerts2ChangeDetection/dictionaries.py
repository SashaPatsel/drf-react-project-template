# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 09:21:46 2019

@author: MEvans
"""
#we probably don't need to import ee here, could create these as python dictionaries...?
import ee

#Collection of dictionaries storing parameter values for various habitat types
forest = ee.Dictionary({
  'int': 0,
  'cv_z': 0.01968614,#0.020213447,
  'rcvmax_z': -0.01005500,#,-0.241673763,
  'ndvi_z': 0.23793789,#0.171443325,
  'ndsi_z': 0.09507422,#,0.242237481,
  'ndwi_z': 0.09902060,#-0.021797543,
  'nbr_z': 0.10534742,#-0.004327796,
  'lda': 1.5,
  'chi':  1.680617e-02,
  'V1':  -1.465696e-03,
  'V2':1.723482e-04,
  'V3': 2.299032e-04,
  'V4': -3.903381e-05,
  'V5': 3.061286e-04,
  'V6':  -7.319635e-04,
  'mad': 1
})


scrub = ee.Dictionary({
  'int': 0,
  'cv_z': 0.001523492,#-0.004616377,
  'rcvmax_z': -0.228383542,#-0.756532635,
  'ndvi_z': 0.374194520,#-0.034184409,
  'ndsi_z': -0.177040740,#-0.005930105,
  'ndwi_z': -0.135408066,#-0.208912147,
  'nbr_z': -0.241886898,#-0.065727911,
  'lda': 1.5,
  'chi':  0.0112356429,
  'V1': -0.0019951636,
  'V2':  0.0002209054,
  'V3':   0.0004750912,
  'V4': -0.0015628258,
  'V5':  -0.0017628213,
  'V6':  0.0005914612,
  'mad': 1.5
})

desert = ee.Dictionary({
  'int': 0,
  'cv_z': 0.05781507,#0.03535703,
  'rcvmax_z': -0.07196164,#0.37298094,
  'ndvi_z': 0.22448341,#0.81159062,
  'ndsi_z': -0.04054897,#0.31934502,
  'ndwi_z': -0.08732940,#-0.04074573,
  'nbr_z': -0.10015228,#0.03053187,
  'lda': 1.5,
  'chi': 4.053633e-02,
  'V1': -1.668553e-04,
  'V2': -9.212610e-04,
  'V3': -7.455153e-05,
  'V4': -1.387260e-03,
  'V5': 2.851671e-04,
  'V6': -3.688913e-04,
  'mad': 2  
})
    
wetland = ee.Dictionary({
  'int': 0,
  'cv_z': 0.02608609,#0.01539318,
  'rcvmax_z': -0.11168147,#,-0.53627410,
  'ndvi_z': 0.09873193,#-0.05276547,
  'ndsi_z': 0.09082271,#0.04784782,
  'ndwi_z': -0.12424875,#-0.21047313,
  'nbr_z': 0.15379691,#0.28553036,
  'lda': 1,
  'chi':  3.183977e-02,
  'V1':  -5.495463e-04,
  'V2':  -1.935902e-05,
  'V3':  -5.771866e-05,
  'V4':   3.543529e-04,
  'V5':   8.904052e-04,
  'V6':  -2.347725e-03,
  'mad': 1.1
})

grassland = ee.Dictionary({
  'int': 0,
  'cv_z': 0.01501676,#0.003335746,
  'nbr_z': 0.09690559,#0.200660811,
  'ndsi_z': -0.08688555,#-0.048249043,
  'ndvi_z': -0.14835658,#0.199691164,
  'ndwi_z': -0.19044280,#0.012553511,
  'rcvmax_z': -0.20351300,#-0.473307836,
  'lda': 1.5,
  'chi':  0.0195215749,
  'V1':   0.0001151189,
  'V2':  -0.0006378971,
  'V3': -0.0004738995,
  'V4': -0.0007036161,
  'V5':   0.0004734193,
  'V6':  -0.0011570211,
  'mad': 1
})