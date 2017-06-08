import numpy as np
from featureParsing import *
from sklearn.decomposition import PCA , KernelPCA

#feature parsing

[imageId , imageFiles , features , groundTruth] = dirFeatureParsing(\
"../features/features.smart_crop.no_enhancement",\
[8],\
"B-mode",\
"temp.log")

datasetSize = len(imageId)
featuresNum = len(features[0])

print "num of samples is" , datasetSize
print "num of features per sample is" , featuresNum

pca = PCA(n_components=None)
pca.fit(features)
Y = pca.transform(features)
#print Y , "\n"
print "pca.explained_variance_ratio_ : \n" , pca.explained_variance_ratio_
print "new dataset dim is " , Y.shape
#print Y[0]


