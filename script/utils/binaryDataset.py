#!/usr/bin/env python

"""
    File name:          binaryDataset.py
    Author:             Guy Tevet
    Date created:       9/6/2017
    Date last modified: 9/6/2017
    Description:        creating contour & binary datasets from raw dataset
"""

import numpy as np
from scipy.ndimage import imread
from scipy.misc import imresize , imsave , imshow

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os

###############################

def createContourImage(sigSourceImagePath,contourDestImagePath,logFile):

        epsilon = 1000

        sigImage = imread(sigSourceImagePath)

        print "[createContourImage] prossesing: %s"%(sigSourceImagePath)

        hight = sigImage.shape[0]
        width = sigImage.shape[1]
        color = sigImage.shape[2]

        #create blank image
        contourImage = np.zeros(sigImage.shape);

        #print sigImage[31,90,:]
        #print np.var([252,254,255])

        for i in range(hight):
                for j in range(width):
                        if np.var(sigImage[i,j,:]) > epsilon:
                                contourImage[i,j] = 1

        imsave(contourDestImagePath,contourImage)

        return 0
###############################
def createBinaryImage(contourSourceImagePath,binaryDestImagePath,logFile):

        print "[createBinaryImage] prossesing: %s"%(contourSourceImagePath)
        
        sys.setrecursionlimit(10000) #extending the recursive stack depth allowed  
        
        image = imread(contourSourceImagePath,mode='L')

        hight = image.shape[0]
        width = image.shape[1]

        #find first point

        for i in range(1,hight):
                for j in range(1,width):
                        if image[i,j] == 0 and image[i-1,j] == 255 and image[i,j-1] == 255:
                                print i,j
                                #run recursive fill
                                recursiveFill(image,i,j)
                                break
                else:
                        continue  # executed if the loop ended normally (no break)
                break  # executed if 'continue' was skipped (break)



 
        imsave(binaryDestImagePath,image)

###############################
def recursiveFill(image,starting_i,starting_j):
        if   (starting_i >= image.shape[0]) or (starting_j >= image.shape[1]):
                return
        elif (starting_i < 0) or (starting_j < 0):
                return
        elif image[starting_i,starting_j] == 255 :
                return
        else:
                image[starting_i,starting_j] = 255;
                recursiveFill(image,starting_i+1,starting_j) 
                recursiveFill(image,starting_i-1,starting_j)
                recursiveFill(image,starting_i,starting_j-1)
                recursiveFill(image,starting_i,starting_j+1)
###############################
def imageBinaryCut(sourceImage,binaryRefInage,destImage,logFile):

        epsilon = 1000

        cuted_image = imread(sourceImage)
        ref_image = imread(binaryRefInage,mode='L')

        print "[imageBinaryCut] prossesing: %s"%(sourceImage)

        hight = cuted_image.shape[0]
        width = cuted_image.shape[1]
        color = cuted_image.shape[2]

        assert ref_image.shape[0] == hight
        assert ref_image.shape[1] == width

        for i in range(hight):
                for j in range(width):
                        if ref_image[i,j] == 0 :
                                cuted_image[i,j,:] = [0,0,0]

        imsave(destImage,cuted_image)

        return 0

###############################
def createCombinedImage(image1,image2,image3,destImage,logFile):


        print "[createCombinedImage] prossesing: %s"%(image1)

        im1 = imread(image1,mode='L')
        im2 = imread(image2,mode='L')
        im3 = imread(image3,mode='L')

        assert im1.shape == im2.shape and im1.shape == im3.shape

        dest = np.zeros((im1.shape[0],im1.shape[1],3))
        dest[..., 0] = im1
        dest[..., 1] = im2
        dest[..., 2] = im3

        #dest = np.concatenate((im1,im2,im3),axis = 2)

        imsave(destImage,dest)

        return 0
###############################
def createCombinedDataset(srcDir,destDir,logPath):
        
        if(not os.path.exists(srcDir)):
                print "%s was not found"%srcDir1
                return

        if(not os.path.exists(destDir)):
                os.mkdir(destDir)


        for f in os.listdir(srcDir):
                if(os.path.basename(f).find("B-mode") != -1):
                        srcImage1 = os.path.join(srcDir,os.path.basename(f))                                   #R channel
                        srcImage2 = os.path.join(srcDir,os.path.basename(f).replace("B-mode","b_cut"))         #G channel
                        srcImage3 = os.path.join(srcDir,os.path.basename(f).replace("B-mode","binary"))        #B channel
                        destImage = os.path.join(destDir,os.path.basename(f).replace("B-mode","comb_bmode_bcut_bin"))
                        if(os.path.exists(srcImage1) and os.path.exists(srcImage2) and os.path.exists(srcImage3)): 
                                createCombinedImage(srcImage1,srcImage2,srcImage3,destImage,None)

        return 0
###############################
def createContourDataset(sigDir,contourDir,logPath):
        
        if(not os.path.exists(sigDir)):
                print "%s was not found"%sigDir
                return

        if(not os.path.exists(contourDir)):
                os.mkdir(contourDir)

        for f in os.listdir(sigDir):
                sigSourceImagePath = os.path.join(sigDir,f)
                contourDestImagePath = os.path.join(contourDir,f).replace("B-mode","contour")
                createContourImage(sigSourceImagePath,contourDestImagePath,None)
        return 0
###############################
def createBinaryDataset(contourDir,binaryDir,logPath):
        
        if(not os.path.exists(contourDir)):
                print "%s was not found"%contourDir
                return

        if(not os.path.exists(binaryDir)):
                os.mkdir(binaryDir)

        for f in os.listdir(contourDir):
                contourSourceImagePath = os.path.join(contourDir,f)
                binaryDestImagePath = os.path.join(contourDir,f).replace("contour","binary")
                createBinaryImage(contourSourceImagePath,binaryDestImagePath,None)
        return
###############################
def createCutedDataset(srcDir,refDir,destDir,logPath):
        
        if(not os.path.exists(srcDir)):
                print "%s was not found"%srcDir
                return
        
        if(not os.path.exists(refDir)):
                print "%s was not found"%refDir
                return

        if(not os.path.exists(destDir)):
                os.mkdir(destDir)

        for f in os.listdir(srcDir):
                
                if(os.path.basename(f).find("B-mode") != -1):
                        srcImage = os.path.join(srcDir,os.path.basename(f))
                        destImage = os.path.join(destDir,os.path.basename(f).replace("B-mode","b_cut"))
                        refImage = os.path.join(refDir,os.path.basename(f).replace("B-mode","1_binary"))
                        if(os.path.exists(srcImage) and os.path.exists(refImage)): 
                                print srcImage ,destImage , refImage
                                imageBinaryCut(srcImage,refImage,destImage,None)


                if(os.path.basename(f).find("Elasto") != -1):
                        srcImage = os.path.join(srcDir,os.path.basename(f))
                        destImage = os.path.join(destDir,os.path.basename(f).replace("Elasto","e_cut"))
                        refImage = os.path.join(refDir,os.path.basename(f).replace("Elasto","1_binary"))
                        if(os.path.exists(srcImage) and os.path.exists(refImage)): 
                                print srcImage ,destImage , refImage
                                imageBinaryCut(srcImage,refImage,destImage,None)
                        
        return
###############################
#createContourDataset("../../dataset/dataset_sigmentation","../../dataset/dataset_contour",None)
#createBinaryDataset("../../dataset/dataset_contour","../../dataset/dataset_binary",None)
#createCutedDataset("../../dataset/dataset","../../dataset/dataset_binary","../../dataset/dataset_cut",None)
createCombinedDataset("../../dataset/dataset","../../dataset/dataset_comb_bmode_bcut_bin",None)
