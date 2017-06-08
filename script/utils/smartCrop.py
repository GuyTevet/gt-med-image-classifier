import numpy
from scipy.ndimage import imread
from scipy.misc import imresize , imsave , imshow

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#constants
DIM = 2
HIGHT = 0
WIDTH = 1
MIN = 0
MAX = 1



DETECTION_METHOD_0 = 0
DETECTION_METHOD_1 = 1
NO_CROP = 10


####################################
def overfeatSmartCrop(refImagePath,sourceImgPath,destImgPath,outputMargin,detectionMethod,threshold,logFile):
        outputHight = 231
        outputWidth = 231
        if detectionMethod is NO_CROP :
                return noCrop(refImagePath,sourceImgPath,destImgPath, outputMargin , outputHight , outputWidth, detectionMethod,threshold,logFile)
        else:
                return smartCrop(refImagePath,sourceImgPath,destImgPath, outputMargin , outputHight , outputWidth, detectionMethod,threshold,logFile)
####################################
def smartCrop(refImagePath,sourceImgPath,destImgPath, outputMargin , outputHight , outputWidth, detectionMethod,threshold,logFile):

        print "[smartCrop] prossesing: %s"%(sourceImgPath)
        
        #if(detectionMethod == DETECTION_METHOD_0):
        #        refImage = imread(refImagePath)
        #elif(detectionMethod == DETECTION_METHOD_1):
        #        refImage = imread(refImagePath) - imread(sourceImgPath) 
        refImage = imread(refImagePath)

        ROIpoints = detectROI(refImage,detectionMethod,threshold,logFile)
        
        if (ROIpoints == None):
                return 1

        croppingPoints = findCroppingPoints(ROIpoints,refImage,outputMargin,outputHight / float(outputWidth),logFile)
          
        if (croppingPoints == None):
                return 1

        #for debug
        logFile.write("ROI points are: %s\nCropping points are: %s\n"%(ROIpoints,croppingPoints))

        return cropResizeSave(sourceImgPath,destImgPath,croppingPoints,outputHight,outputWidth,logFile)
###############################
def findCroppingPoints(ROIpoints,refImage,marginSize,hightWidthRatio,logFile):

        #image = imread(refImagePath)
        image = refImage

        hight = image.shape[0]
        width = image.shape[1]
        color = image.shape[2]

        if(color != 3):
                logFile.write("ERROR - got a %d chan image, please insert a RGB image\n"%color)
                return

        h_min = ROIpoints[HIGHT][MIN]
        h_max = ROIpoints[HIGHT][MAX]

        w_min = ROIpoints[WIDTH][MIN]
        w_max = ROIpoints[WIDTH][MAX]
        
        h_min = max((h_min-marginSize),0)
        h_max = min((h_max+marginSize),hight)

        w_min = max((w_min-marginSize),0)
        w_max = min((w_max+marginSize),width)

        h_center = int(round((h_max+h_min)/2.))
        w_center = int(round((w_max+w_min)/2.))

        h_size = h_max-h_min+1;
        w_size = w_max-w_min+1;

        logFile.write("trace 0 : hight = %d , width = %d , h_min = %d, h_max = %d, w_min = %d, w_max = %d, h_size = %d, w_size = %d, h_center = %d ,w_center = %d\n"%(hight,width,h_min,h_max,w_min,w_max,h_size,w_size,h_center,w_center))

        if(h_size > width):
                w_size = int(round(width/2.))
                h_size = int(round(width * hightWidthRatio /2.))
        elif(w_size > hight):
                h_size = int(round(hight/2.))
                w_size = int(round(hight/float(hightWidthRatio)/2.)) 
        elif(h_size > w_size):
                w_size = int(round(h_size/float(hightWidthRatio)/2.))
                h_size = int(round(h_size/2.))
        else:
                h_size = int(round(w_size * hightWidthRatio /2.))
                w_size = int(round(w_size/2.))

        logFile.write("trace 1 : hight = %d , width = %d , h_min = %d, h_max = %d, w_min = %d, w_max = %d, h_size = %d, w_size = %d, h_center = %d ,w_center = %d\n"%(hight,width,h_min,h_max,w_min,w_max,h_size,w_size,h_center,w_center))

        if((h_center+h_size > hight and h_center-h_size < 0) or h_size*2 > hight):
                h_min = 0
                h_max = hight
        elif(h_center+h_size > hight):
                h_max = hight
                h_min = hight - (h_size*2)
        elif(h_center-h_size < 0):
                h_min = 0
                h_max = 0 + (h_size*2)
        else:
                h_min = h_center - h_size
                h_max = h_center + h_size

        logFile.write("trace 2 : hight = %d , width = %d , h_min = %d, h_max = %d, w_min = %d, w_max = %d, h_size = %d, w_size = %d, h_center = %d ,w_center = %d\n"%(hight,width,h_min,h_max,w_min,w_max,h_size,w_size,h_center,w_center))
         
        if((w_center+w_size > width and w_center-w_size < 0) or (w_size*2) > width):#bug
                w_min = 0
                w_max = width   
        elif(w_center+w_size > width):
                w_max = width
                w_min = width - (w_size*2)
        elif(w_center-w_size < 0):
                w_min = 0
                w_max = 0 + (w_size*2)
        else:
                w_min = w_center - w_size
                w_max = w_center + w_size

        logFile.write("trace 3 : hight = %d , width = %d , h_min = %d, h_max = %d, w_min = %d, w_max = %d, h_size = %d, w_size = %d, h_center = %d ,w_center = %d\n"%(hight,width,h_min,h_max,w_min,w_max,h_size,w_size,h_center,w_center))


        #check results
        if((w_min >= w_max) or (w_min == -1) or (w_max == -1)):
                logFile.write("ERROR at width params (%d,%d)\n"%(w_min,w_max))
                return
        if((h_min >= h_max) or (h_min == -1) or (h_max == -1)):
                logFile.write("ERROR at hight params (%d,%d)\n"%(h_min,h_max))
                return

        if (h_size/float(w_size) != hightWidthRatio):
                logFile.write("ERROR! h_size=%d , w_size=%d but hightWidthRatio=%.2f\n"%(h_size*2,w_size*2,hightWidthRatio))
                return
      
        return [[h_min,h_max],[w_min,w_max]]

####################################
def findSize(refImagePath):
        image = imread(refImagePath)
        hight = image.shape[0]
        width = image.shape[1]
        return [hight,width]

######################################
def detectROI(refImage,detectionMethod,threshold,logFile):
        
        #step 1: initialization
        #image = imread(refImagePath)
        image = refImage

        hight = image.shape[0]
        width = image.shape[1]
        color = image.shape[2]

        if(color != 3):
                logFile.write("ERROR - got a %d chan image, please insert a RGB image\n"%color)
                return

        # Convert RGB2GRAY
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]
        image_gray = R * 299. / 1000 + G * 587. / 1000 + B * 114. / 1000

        h_min = -1
        h_max = -1
        w_min = -1
        w_max = -1

        #step 2: detect points

        ##METHOD0##
        if(detectionMethod == DETECTION_METHOD_0):
                 #detect hight points
                for i in range(0,hight):
                        for j in range(0,width):
                                if(image[i][j][0] != image[i][j][1]):
                                        h_min = i
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                for i in range(0,hight):
                        for j in range(0,width):
                                if(image[hight-i-1][width-j-1][0] != image[hight-i-1][width-j-1][1]):
                                        h_max = hight-i-1
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                #detect width points
                for j in range(0,width):
                        for i in range(0,hight):
                                if(image[i][j][0] != image[i][j][1]):
                                        w_min = j
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                for j in range(0,width):
                        for i in range(0,hight):
                                if(image[hight-i-1][width-j-1][0] < image[hight-i-1][width-j-1][1]):
                                        w_max = width-j-1
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

        ##METHOD1##
        if(detectionMethod == DETECTION_METHOD_1):

                 #detect hight points
                for i in range(0,hight):
                        for j in range(0,width):
                                if(image_gray[i][j] > threshold):
                                        h_min = i
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                for i in range(0,hight):
                        for j in range(0,width):
                                if(image_gray[hight-i-1][width-j-1] > threshold):
                                        h_max = hight-i-1
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                #detect width points
                for j in range(0,width):
                        for i in range(0,hight):
                                if(image_gray[i][j] > threshold):
                                        w_min = j
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)

                for j in range(0,width):
                        for i in range(0,hight):
                                if(image_gray[hight-i-1][width-j-1] > threshold):
                                        w_max = width-j-1
                                        break
                        else:
                                continue  # executed if the loop ended normally (no break)
                        break  # executed if 'continue' was skipped (break)
       

        #step 3:check results
        if((w_min >= w_max) or (w_min == -1) or (w_max == -1)):
                logFile.write("ERROR at width params (%d,%d)\n"%(w_min,w_max))
                return
        if((h_min >= h_max) or (h_min == -1) or (h_max == -1)):
                logFile.write("ERROR at hight params (%d,%d)\n"%(h_min,h_max))
                return

        return [[h_min,h_max],[w_min,w_max]]

######################################
def cropResizeSave(sourceImgPath,destImgPath,cropingPoints,outputHight,outputWidth,logFile):

        image = imread(sourceImgPath)

        #cropping gray scale source image
        if image.ndim == 2 :
                image = image[cropingPoints[HIGHT][MIN] : cropingPoints[HIGHT][MAX] ,
                        cropingPoints[WIDTH][MIN] : cropingPoints[WIDTH][MAX] ]
        #cropping RGB image
        else:
                image = image[cropingPoints[HIGHT][MIN] : cropingPoints[HIGHT][MAX] ,
                        cropingPoints[WIDTH][MIN] : cropingPoints[WIDTH][MAX] , :]

        image = imresize(image, (outputHight, outputWidth)).astype(numpy.float32)

        imsave(destImgPath,image)

        return 0
####################################
def noCrop(refImagePath,sourceImgPath,destImgPath, outputMargin , outputHight , outputWidth, detectionMethod,threshold,logFile):
        image = imread(sourceImgPath)

        print "[noCrop] prossesing: %s"%(sourceImgPath)

        hight = image.shape[0]
        width = image.shape[1]

        if image.ndim == 3:
                color = image.shape[2]

        strip_size = abs((hight-width)/2)

        strip_size = int(abs((hight-width)/2))

        if strip_size is not 0:

                if hight > width :
                        if image.ndim == 3:
                                strip = numpy.zeros((hight,strip_size,color))
                        else:
                                strip = numpy.zeros((hight,strip_size))
                        _axis=1
                        
                else:
                        if image.ndim == 3:
                                strip = numpy.zeros((strip_size,width,color))
                        else:
                                strip = numpy.zeros((strip_size,width))
                        _axis=0

                image = numpy.concatenate((strip,image,strip),axis=_axis)

        #for debug
        logFile.write("using NO_CROP\n new points are: (%0d,%0d)\n"%(image.shape[0],image.shape[1]))

        image = imresize(image, (outputHight, outputWidth)).astype(numpy.float32)

        imsave(destImgPath,image)

        return 0
####################################
