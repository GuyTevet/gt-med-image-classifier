#!/usr/bin/env python

"""
    File name:          elastoPCA.py
    Author:             Guy Tevet
    Date created:       9/6/2017
    Date last modified: 9/6/2017
    Description:        create PCA transform for reducing elasto images
                        from 3D to 2D.
                        creating comb detaset using 2D elasto images.
"""

import os
import numpy as np
import matplotlib.colors as colors
from sklearn.decomposition import PCA , KernelPCA
from scipy.ndimage import imread
from scipy.misc import imresize , imsave , imshow
import matplotlib.pyplot as plt

def createElastoTransformation(inputElastoDir,logFile,elastoDims = 2):
        
        txt = "starting createElastoTransformation()\n"
        print txt
        logFile.write(txt)

        elastoImg = []
        for f in os.listdir(inputElastoDir): 
                if(os.path.basename(f).find("Elasto") != -1):
                        elastoImg.append(colors.rgb_to_hsv(imread(os.path.join(inputElastoDir,f))))
                        #elastoImg.append(imread(os.path.join(inputElastoDir,f)))

        datasetSize = len(elastoImg)

        txt = "num of img is %d"%datasetSize
        print txt
        logFile.write(txt)

        pixels = []

        for im in elastoImg:
                for i in range(im.shape[0]):
                        for j in range(im.shape[1]):
                                pixels.append(im[i,j,:])

        txt = "pixels dimentions are " + str(np.asarray(pixels).shape) + "\n"
        print txt
        logFile.write(txt)

        pca = PCA(n_components=None)
        pca.fit(pixels)
        txt = "pca.explained_variance_ratio_ : \n%s"%pca.explained_variance_ratio_ + "\n"
        print txt
        logFile.write(txt)

        epsilon = 0.02
        if  pca.explained_variance_ratio_[2] > epsilon and elastoDims == 2 : 
                txt = "ERROR! pca to 2D cousing too much data loss (%lf)\n"%pca.explained_variance_ratio_[2]
                print txt
                logFile.write(txt)
                return None
        elif (pca.explained_variance_ratio_[2] + pca.explained_variance_ratio_[1] ) > epsilon and elastoDims == 1 : 
                txt = "ERROR! pca to 1D cousing too much data loss (%lf)\n"%(pca.explained_variance_ratio_[2] + pca.explained_variance_ratio_[1])
                print txt
                logFile.write(txt)
                return None
        else:
                txt = "data loss is minor. creating %0dD transformation...\n"%elastoDims
                print txt
                logFile.write(txt)
                pca = PCA(n_components=elastoDims)
                pca.fit(pixels)
                return pca


# H,S channel will contain the 2D elastography image
# V   channel will contain the B-mode image
def createBmodeElastoCombinedImage(elastoFile,BmodeFile,binaryFile,destFile,pca,logFile,elastoPlot = False,elastoDims = 2):


        txt = "handling %s\n"%elastoFile 
        print txt
        logFile.write(txt)

        #open elastography image at HSV
        elasto = colors.rgb_to_hsv(imread(elastoFile))
        #print "HH" , elasto[20,:,0]
        #print "SS" , elasto[20,:,1]
        #print "VV" , elasto[20,:,2]
        
        hight = elasto.shape[0]
        width = elasto.shape[1]

        #open B-mode at gray scale
        bmode = imread(BmodeFile,"L")

        #open binary at gray scale and modify it to saturation levels
        if binaryFile is not None:
                binary = imread(binaryFile,"L")

                for i in range(binary.shape[0]):
                        for j in range(binary.shape[1]):
                                if binary[i,j] == 0:            #NOT ROI
                                        binary[i,j] = 0.8
                                else:                           #ROI
                                        binary[i,j] = 0.2

                #for debug
                #imshow(binary)
                #print binary[20,:]
                
        #print "LL" , bmode[20,:]
        
        #transform elastography to 2D image
        assert elasto.shape[2] == 3
        #_2Delasto = np.zeros((elasto.shape[0],elasto.shape[1],2))

        print "before" , elasto.shape
        elasto = np.reshape(elasto,(-1,3))
        print "after reshape" , elasto.shape
        _2Delasto = pca.transform(elasto)
        print "after transform" , _2Delasto.shape
        _2Delasto = np.reshape(_2Delasto,(hight,width,-1))
        print "after reshape" , _2Delasto.shape
        #print "HHH" , _2Delasto[20,:,0]
        #print "SSS" , _2Delasto[20,:,1]

        if elastoDims == 2 :
                #normlizing valuse to [0,1] scale
                H_min = _2Delasto[:,:,0].min()
                S_min = _2Delasto[:,:,1].min()
                H_max = _2Delasto[:,:,0].max()
                S_max = _2Delasto[:,:,1].max()

                #print H_min , S_min
                #print H_max , S_max

                #create elasto H,S plot
                if elastoPlot is True:
                        plt.plot(_2Delasto[:,:,0],_2Delasto[:,:,1], 'ro')
                        plt.title('H , S elasto channels after transformation')
                        plt.xlabel('H channel')
                        plt.ylabel('S channel')
                        plt.savefig(destFile.replace(".bmp","_plot.jpg"),format='jpg')
                
                _2Delasto[:,:,0] = (_2Delasto[:,:,0] - H_min)/(H_max-H_min)
                _2Delasto[:,:,1] = (_2Delasto[:,:,1] - S_min)/(S_max-S_min)

                #combine images
                dest = np.zeros((hight,width,3))
                dest[..., 0] = _2Delasto[..., 0]        #H channel
                dest[..., 1] = _2Delasto[..., 1]        #S channel
        elif elastoDims == 1 :
                #normlizing valuse to [0,1] scale
                H_min = _2Delasto[..., 0].min()
                H_max = _2Delasto[..., 0].max()
               
                _2Delasto[..., 0] = (_2Delasto[..., 0] - H_min)/(H_max-H_min)

                dest = np.zeros((hight,width,3))
                dest[..., 0] = _2Delasto[..., 0]                #H channel
                if binaryFile is not None: 
                        dest[..., 1] = binary                   #S channel
                else:
                        dest[..., 1] = np.ones((hight,width))   #S channel
        else:
                print "ERROR! illegal elastoDims(%0d)"%elastoDims
                return 
         
        dest[..., 2]   = bmode                  #V channel
        
        #back to RGB
        dest = colors.hsv_to_rgb(dest)

        #save image
        imsave(destFile,dest)

        return

#input dir should contain elastography and B-mode images
def createBmodeElastoCombinedDataset(inputDir,outputDir,logFile,datasetName,elastoPlot = False,elastoDims = 2):

        if(not os.path.exists(inputDir)):
                print "%s was not found"%inputDir
                return

        if(not os.path.exists(outputDir)):
                os.mkdir(outputDir)
    
        #first - create a PCA transformation
        pca = createElastoTransformation(inputDir,logFile,elastoDims)

        if pca == None :
                return
        else:
        #        for f in os.listdir(inputDir):
        #                if(os.path.basename(f).find("B-mode") != -1):
        #                        BmodeFile  = os.path.join(inputDir,os.path.basename(f))                                   
        #                        elastoFile = os.path.join(inputDir,os.path.basename(f).replace("B-mode","Elasto"))
        #                        binaryFile = os.path.join(inputDir,os.path.basename(f).replace("B-mode","binary"))
        #                        destFile = os.path.join(outputDir,os.path.basename(f).replace("B-mode",datasetName))
        #                        if(os.path.exists(BmodeFile) and os.path.exists(elastoFile) and os.path.exists(binaryFile)): 
        #                                createBmodeElastoCombinedImage(elastoFile,BmodeFile,binaryFile,destFile,pca,logFile,elastoPlot,elastoDims)
                for f in os.listdir(inputDir):
                        if(os.path.basename(f).find("bmode_multiSorf") != -1):
                                sorfFile  = os.path.join(inputDir,os.path.basename(f))                                   
                                elastoFile = os.path.join(inputDir,os.path.basename(f).replace("bmode_multiSorf","Elasto"))
                                binaryFile = os.path.join(inputDir,os.path.basename(f).replace("bmode_multiSorf","binary"))
                                destFile = os.path.join(outputDir,os.path.basename(f).replace("bmode_multiSorf",datasetName))
                                if(os.path.exists(sorfFile) and os.path.exists(elastoFile) and os.path.exists(binaryFile)): 
                                        createBmodeElastoCombinedImage(elastoFile,sorfFile,binaryFile,destFile,pca,logFile,elastoPlot,elastoDims)
        return


#script
log = open("./utils/elastoPca.log","w")
log.write("")
log = open("./utils/elastoPca.log","a")
#createBmodeElastoCombinedDataset("../dataset/dataset","../dataset/dataset_comb_bmode_elasto_hsv_with_plot",log,"comb_bmode_elasto_hsv",True)
#createBmodeElastoCombinedDataset("../dataset/dataset","../dataset/dataset_comb_bmode_elasto_hv",log,"comb_bmode_elasto_hv",False,1)
#createBmodeElastoCombinedDataset("../dataset/dataset","../dataset/dataset_comb_bmode_binary_i02o08_elasto_hsv",log,"comb_bmode_binary_i02o08_elasto_hsv",False,1)
#createBmodeElastoCombinedDataset("../dataset/dataset","../dataset/dataset_comb_sorf_elasto_hsv",log,"comb_sorf_elasto_hsv",False,2)

log = open("./utils/elastoPcaAtRGB.log","w")
log.write("")
log = open("./utils/elastoPcaAtRGB.log","a")
createElastoTransformation("../dataset/dataset",log,elastoDims = 3)

log.close()
