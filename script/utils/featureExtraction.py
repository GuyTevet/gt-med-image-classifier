from subprocess import call
import os
EXE = " ../overfeat/bin/linux_64/overfeat "

def extractLayer(paperLayerNum , inputDir , outputDir , networkSubType , imageType = 'fusion'):
        
        outputDir = "%s%soutput_L%d" %(outputDir,'/' ,paperLayerNum)
        actualLayerNum = paperLayer2actualLayerTranslator(paperLayerNum,networkSubType)

        if(networkSubType == "large"):
                networkSubTypeFlag = "-l"
        else:
                networkSubTypeFlag = ""

        if(actualLayerNum == -1):
               raise Exception("illegal input paperLayer(%d)"%paperLayerNum) 

        if(not os.path.exists(outputDir)):
                os.mkdir(outputDir) 

        for f in os.listdir(inputDir):
                inputFilePath = os.path.join(inputDir,f)
                outputFilePath = os.path.join(outputDir,f) + '.features'
                if((imageType == 'fusion' or os.path.basename(f).find(imageType) > -1)\
                and (not os.path.exists(outputFilePath) or os.path.getsize(outputFilePath) < 200)): #should override some currupted files
                        flags = networkSubTypeFlag + " -L %d %s > %s" %(actualLayerNum,inputFilePath,outputFilePath)
                        print inputFilePath
                        print outputFilePath
                        print "[" + networkSubType + "network]"
                        print "paperLayer(%d) , actualLayer(%d)"%(paperLayerNum,actualLayerNum)
                        print "executing: " + EXE + flags
                        print ''
                        os.system(EXE + flags)
                        #TODO: add checker for successful extraction


def paperLayer2actualLayerTranslator (paperLayer,networkSubType):
        actualLayer = -1 #error

        #layer translator for the LARGE network
        if(networkSubType == "large"):
                if  (paperLayer == 1): actualLayer = 3
                elif(paperLayer == 2): actualLayer = 6
                elif(paperLayer == 3): actualLayer = 9
                elif(paperLayer == 4): actualLayer = 12
                elif(paperLayer == 5): actualLayer = 15
                elif(paperLayer == 6): actualLayer = 19
                elif(paperLayer == 7): actualLayer = 21
                elif(paperLayer == 8): actualLayer = 23
                elif(paperLayer == 9): actualLayer = 24

        #layer translator for the SMALL network
        else:
                if  (paperLayer == 1): actualLayer = 3
                elif(paperLayer == 2): actualLayer = 6
                elif(paperLayer == 3): actualLayer = 9
                elif(paperLayer == 4): actualLayer = 12
                elif(paperLayer == 5): actualLayer = 16
                elif(paperLayer == 6): actualLayer = 18
                elif(paperLayer == 7): actualLayer = 20
                elif(paperLayer == 8): actualLayer = 21

        print "[paperLayer2actualLayerTranslator] [%s network] translated paper(%d) -> actual(%d)"%(networkSubType,paperLayer,actualLayer)

        return actualLayer

"""
for i in range(1,22):
        extractLayer(i)
        print "done layer %d" %i
"""


