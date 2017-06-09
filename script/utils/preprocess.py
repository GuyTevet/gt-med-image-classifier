#!/usr/bin/env python

"""
    File name:          preprocess.py
    Author:             Guy Tevet
    Date created:       9/6/2017
    Date last modified: 9/6/2017
    Description:        create cropped datasets using
                        smart_crop or no_crop
"""

import numpy
from scipy.ndimage import imread
from scipy.misc import imresize , imsave , imshow

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from smartCrop import overfeatSmartCrop
import os
import sys

##detection method 1

#print overfeatSmartCrop('../dataset_sigmentation/44.1_1_B-mode.bmp',
#                        '../dataset_sigmentation/44.1_1_B-mode.bmp','try.bmp',10)


#image1 = imread('../dataset_sigmentation/17.1_1_B-mode.bmp')
#image2 = imread('../dataset/17.1_B-mode.bmp')

#image = image1 - image2

#print image1.shape[2]
#print image2.shape[2]
#print image.shape[2]

#plt.figure()
#imgplot = plt.imshow(image)
#plt.show()


def preprocess(logPath,refDir,srcDir,destDir,detectionMethod,threshhold,margin,firstZeroImage,lastImage):
        log = open(logPath,"w")
        log.write("")
        log = open(logPath,"a")

        if(not os.path.exists(destDir)):
                os.mkdir(destDir)

        for i in range(1,lastImage + 1):
                if(i >= firstZeroImage):
                        groundTruth = 0
                else:
                        groundTruth = 1

                refStr = '%s/%s.%s_1_B-mode.bmp'%(refDir,i ,groundTruth)
                
                bmodeSrcStr = '%s/%s.%s_B-mode.bmp'%(srcDir,i ,groundTruth)
                elastoSrcStr = '%s/%s.%s_Elasto.bmp'%(srcDir,i ,groundTruth)
                bmodeSorfSrcStr = '%s/%s.%s_bmode_multiSorf.bmp'%(srcDir,i ,groundTruth)
                contourSrctStr = '%s/%s.%s_contour.bmp'%(srcDir,i ,groundTruth)
                binarySrcStr = '%s/%s.%s_binary.bmp'%(srcDir,i ,groundTruth)
                ecutSrcStr = '%s/%s.%s_e_cut.bmp'%(srcDir,i ,groundTruth)
                bcutSrcStr = '%s/%s.%s_b_cut.bmp'%(srcDir,i ,groundTruth) 
                comb_bmode_bcut_binSrcStr = '%s/%s.%s_comb_bmode_bcut_bin.bmp'%(srcDir,i ,groundTruth)
                comb_bmode_elasto_hsvSrcStr = '%s/%s.%s_comb_bmode_elasto_hsv.bmp'%(srcDir,i ,groundTruth)
                comb_sorf_elasto_hsvSrcStr = '%s/%s.%s_comb_sorf_elasto_hsv.bmp'%(srcDir,i ,groundTruth)
                comb_bmode_elasto_hvSrcStr = '%s/%s.%s_comb_bmode_elasto_hv.bmp'%(srcDir,i ,groundTruth)
                comb_bmode_binary_i02o08_elasto_hsvSrcStr = '%s/%s.%s_comb_bmode_binary_i02o08_elasto_hsv.bmp'%(srcDir,i ,groundTruth)
                comb_bmode_binary_i08o02_elasto_hsvSrcStr = '%s/%s.%s_comb_bmode_binary_i08o02_elasto_hsv.bmp'%(srcDir,i ,groundTruth)

                sigDstStr = '%s/%s.%s_sig.bmp'%(destDir,i ,groundTruth)
                bmodeDstStr = '%s/%s.%s_B-mode.bmp'%(destDir,i ,groundTruth)
                elastoDstStr = '%s/%s.%s_Elasto.bmp'%(destDir,i ,groundTruth)
                bmodeSorfDstStr = '%s/%s.%s_bmode_multiSorf.bmp'%(destDir,i ,groundTruth)
                contourDstStr = '%s/%s.%s_contour.bmp'%(destDir,i ,groundTruth)
                binaryDstStr = '%s/%s.%s_binary.bmp'%(destDir,i ,groundTruth)
                ecutDstStr = '%s/%s.%s_e_cut.bmp'%(destDir,i ,groundTruth)
                bcutDstStr = '%s/%s.%s_b_cut.bmp'%(destDir,i ,groundTruth)
                comb_bmode_bcut_binDstStr = '%s/%s.%s_comb_bmode_bcut_bin.bmp'%(destDir,i ,groundTruth)
                comb_bmode_elasto_hsvDstStr = '%s/%s.%s_comb_bmode_elasto_hsv.bmp'%(destDir,i ,groundTruth)
                comb_sorf_elasto_hsvDstStr = '%s/%s.%s_comb_sorf_elasto_hsv.bmp'%(destDir,i ,groundTruth)
                comb_bmode_elasto_hvDstStr = '%s/%s.%s_comb_bmode_elasto_hv.bmp'%(destDir,i ,groundTruth)
                comb_bmode_binary_i02o08_elasto_hsvDstStr = '%s/%s.%s_comb_bmode_binary_i02o08_elasto_hsv.bmp'%(destDir,i ,groundTruth)
                comb_bmode_binary_i08o02_elasto_hsvDstStr = '%s/%s.%s_comb_bmode_binary_i08o02_elasto_hsv.bmp'%(destDir,i ,groundTruth)

                log.write("\n%s\n"%refStr)

                if(os.path.isfile(refStr) and os.access(refStr, os.R_OK)):
                        log.write("Sigmentation %s result: %d\n"%(i  , overfeatSmartCrop(refStr,refStr,sigDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(bmodeSrcStr) and os.access(bmodeSrcStr, os.R_OK)):
                                log.write("B-mode %s result: %d\n"%(i  , overfeatSmartCrop(refStr,bmodeSrcStr,bmodeDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("Elastography %s result: %d\n"%(i  , overfeatSmartCrop(refStr,elastoSrcStr,elastoDstStr,margin,detectionMethod,threshhold,log)))

                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("Contour %s result: %d\n"%(i  , overfeatSmartCrop(refStr,contourSrctStr,contourDstStr,margin,detectionMethod,threshhold,log)))

                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("Binary %s result: %d\n"%(i  , overfeatSmartCrop(refStr,binarySrcStr,binaryDstStr,margin,detectionMethod,threshhold,log)))

                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("Elasto cut %s result: %d\n"%(i  , overfeatSmartCrop(refStr,ecutSrcStr,ecutDstStr,margin,detectionMethod,threshhold,log)))

                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("B-mode cut %s result: %d\n"%(i  , overfeatSmartCrop(refStr,bcutSrcStr,bcutDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_bcut_bin %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_bmode_bcut_binSrcStr,comb_bmode_bcut_binDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_elasto_hsv %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_bmode_elasto_hsvSrcStr,comb_bmode_elasto_hsvDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_elasto_hsv %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_sorf_elasto_hsvSrcStr,comb_sorf_elasto_hsvDstStr,margin,detectionMethod,threshhold,log)))
                        
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_elasto_hv %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_bmode_elasto_hvSrcStr,comb_bmode_elasto_hvDstStr,margin,detectionMethod,threshhold,log)))
                 
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_binary_i08o02_elasto_hsv %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_bmode_binary_i08o02_elasto_hsvSrcStr,comb_bmode_binary_i08o02_elasto_hsvDstStr,margin,detectionMethod,threshhold,log)))
                
                
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("comb_bmode_binary_i02o08_elasto_hsv %s result: %d\n"%(i  , overfeatSmartCrop(refStr,comb_bmode_binary_i02o08_elasto_hsvSrcStr,comb_bmode_binary_i02o08_elasto_hsvDstStr,margin,detectionMethod,threshhold,log)))
                
                        if(os.path.isfile(elastoSrcStr) and os.access(elastoSrcStr, os.R_OK)):
                                log.write("bmode_multiSorf %s result: %d\n"%(i  , overfeatSmartCrop(refStr,bmodeSorfSrcStr,bmodeSorfDstStr,margin,detectionMethod,threshhold,log)))
                
                elif(os.path.isfile(bmodeSrcStr) or os.path.isfile(elastoSrcStr)):
                        log.write("WARNING! source file %s exists but ref file is missing . do nothing\n"%i)

        log.close()
        print "done preprocess! files at %s , logfile at %s"%(destDir,logPath)

###############################
def createRefDataset(logPath,srcDir,sigDir,dstRefDir,lastImage,firstZeroImage):
        
        log = open(logPath,"w")
        log.write("createRefDataset log start:\n")
        log = open(logPath,"a")

        if(not os.path.exists(dstRefDir)):
                os.mkdir(dstRefDir)
    
        for i in range(1,lastImage + 1):
                if(i >= firstZeroImage):
                        groundTruth = 0
                else:
                        groundTruth = 1

                sigStr = '%s/%s.%s_1_B-mode.bmp'%(sigDir,i ,groundTruth)
                srcStr = '%s/%s.%s_B-mode.bmp'%(srcDir,i ,groundTruth)
                dstStr = '%s/%s.%s_1_B-mode.bmp'%(dstRefDir,i ,groundTruth)

                if(os.path.isfile(sigStr) and os.access(sigStr, os.R_OK) and os.path.isfile(srcStr) and os.access(srcStr, os.R_OK)):
                        imsave(dstStr , imread(sigStr) - imread(srcStr))
                        log.write("%s created successfully\n"%dstStr)


        log.close()
        print "createRefDataset done! files at %s , logfile at %s"%(dstRefDir,logPath)




