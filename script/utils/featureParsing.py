#!/usr/bin/env python

"""
    File name:          featuresParsing.py
    Author:             Guy Tevet
    Date created:       9/6/2017
    Date last modified: 9/6/2017
    Description:        parsing features files into floating point arrays
"""

import os
import string

"""FEATURES_LINE = 2

def dirFeaturePatsing(dirPath,imageType):
        groundTruth = []
        features = []
        fileName = []
        for f in os.listdir(dirPath):
                filePath = os.path.join(dirPath,f)
                if os.path.isfile(filePath):
                        if (f.find(imageType) != -1):
                                fileName.append(f);
                                features.append(fileFeaturePatsing(filePath))
                                if(filePath.find(".1_") != -1):
                                        groundTruth.append(1)
                                elif(filePath.find(".0_") != -1):
                                        groundTruth.append(0)
                                else:
                                        print "ground truth of %s was not found. aborting!" %filePath
                                        return None
        return [fileName , features , groundTruth]
"""


def fileFeatureParsing(files):
        features = []

        for i in range(len(files)):
                f = open(files[i])
                s = f.readline()
                s = f.readline()
                s = s.split(" ")
                for num in s:
                        try:
                                features.append(float(num))
                        except:
                                continue
        return features


def dirFeatureParsing(featuresDir,levels,imageType,logPath):
        
        #FIXME:
        lastImage = 311
        firstZeroImage = 101

        log = open(logPath,"w")
        log.write("")
        log = open(logPath,"a")

        groundTruth = []
        features = []
        imageId = []
        imageFiles = []

        for img in range(1,lastImage + 1):
                files = []
                for level in levels:
                        
                        #setting ground truth
                        if(img >= firstZeroImage):
                                gt = 0
                        else:
                                gt = 1

                        bmodeFile = '%s/output_L%s/%s.%s_B-mode.bmp.features'%(featuresDir,level,img ,gt)
                        elastoFile = '%s/output_L%s/%s.%s_Elasto.bmp.features'%(featuresDir,level,img ,gt)

                        bmodeSorfFile = '%s/output_L%s/%s.%s_bmode_multiSorf.bmp.features'%(featuresDir,level,img ,gt)
                        
                        bcutFile = '%s/output_L%s/%s.%s_b_cut.bmp.features'%(featuresDir,level,img ,gt)
                        ecutFile = '%s/output_L%s/%s.%s_e_cut.bmp.features'%(featuresDir,level,img ,gt)

                        contourFile = '%s/output_L%s/%s.%s_contour.bmp.features'%(featuresDir,level,img ,gt)
                        binaryFile = '%s/output_L%s/%s.%s_binary.bmp.features'%(featuresDir,level,img ,gt)

                        comb_bmode_bcut_binFile = '%s/output_L%s/%s.%s_comb_bmode_bcut_bin.bmp.features'%(featuresDir,level,img ,gt)
                        comb_bmode_elasto_hsvFile = '%s/output_L%s/%s.%s_comb_bmode_elasto_hsv.bmp.features'%(featuresDir,level,img ,gt)
                        comb_sorf_elasto_hsvFile = '%s/output_L%s/%s.%s_comb_sorf_elasto_hsv.bmp.features'%(featuresDir,level,img ,gt)
                        comb_bmode_elasto_hvFile = '%s/output_L%s/%s.%s_comb_bmode_elasto_hv.bmp.features'%(featuresDir,level,img ,gt)

                        comb_bmode_binary_i02o08_elasto_hsvFile = '%s/output_L%s/%s.%s_comb_bmode_binary_i02o08_elasto_hsv.bmp.features'%(featuresDir,level,img ,gt)
                        comb_bmode_binary_i08o02_elasto_hsvFile = '%s/output_L%s/%s.%s_comb_bmode_binary_i08o02_elasto_hsv.bmp.features'%(featuresDir,level,img ,gt)


                        if(os.path.isfile(bmodeFile) and (imageType == "B-mode" or imageType == "fusion")):
                                files.append(bmodeFile)
                        if(os.path.isfile(elastoFile) and (imageType == "Elasto" or imageType == "fusion")):
                                files.append(elastoFile)

                        if(os.path.isfile(bmodeSorfFile) and (imageType == "bmode_multiSorf")):
                                files.append(bmodeSorfFile)

                        if(os.path.isfile(ecutFile) and (imageType == "e_cut")):
                                files.append(ecutFile)
                        if(os.path.isfile(bcutFile) and (imageType == "b_cut")):
                                files.append(bcutFile)

                        if(os.path.isfile(contourFile) and (imageType == "contour")):
                                files.append(contourFile)
                        if(os.path.isfile(binaryFile) and (imageType == "binary")):
                                files.append(binaryFile)

                        if(os.path.isfile(comb_bmode_bcut_binFile) and (imageType == "comb_bmode_bcut_bin")):
                                files.append(comb_bmode_bcut_binFile)

                        if(os.path.isfile(comb_bmode_elasto_hsvFile) and (imageType == "comb_bmode_elasto_hsv")):
                                files.append(comb_bmode_elasto_hsvFile)

                        if(os.path.isfile(comb_sorf_elasto_hsvFile) and (imageType == "comb_sorf_elasto_hsv")):
                                files.append(comb_sorf_elasto_hsvFile)

                        if(os.path.isfile(comb_bmode_elasto_hvFile) and (imageType == "comb_bmode_elasto_hv")):
                                files.append(comb_bmode_elasto_hvFile)
                        
                        if(os.path.isfile(comb_bmode_binary_i02o08_elasto_hsvFile) and (imageType == "comb_bmode_binary_i02o08_elasto_hsv")):
                                files.append(comb_bmode_binary_i02o08_elasto_hsvFile)
                        
                        if(os.path.isfile(comb_bmode_binary_i08o02_elasto_hsvFile) and (imageType == "comb_bmode_binary_i08o02_elasto_hsv")):
                                files.append(comb_bmode_binary_i08o02_elasto_hsvFile)

                if(len(files) == 0):
                        continue
                else:

                        imageId.append(img)
                        imageFiles.append(files)

                        f = fileFeatureParsing(files)
                        features.append(f)#TODO: add num of features checker

                        if(files[0].find(".1_") != -1):
                                gt = 1
                        elif(files[0].find(".0_") != -1):
                                gt = 0
                        else:
                                raise Exception("ground truth of image %s was not found" %imageId)

                        groundTruth.append(gt)

                        log.write("\n==%s==\n"%img)
                        log.write("files(%d):\n%s"%(len(files),files))
                        log.write("groundTruth = %s"%gt)
                        log.write("num of features = %s"%len(f))


        log.write("\n==summary==\ndataset size is %s"%len(imageId))
        log.close()
        print "features parsing is done! logfile at %s"%(logPath)

        return [imageId , imageFiles , features , groundTruth]



