##EXPERIMENT
from experimentInclude import *

class Experiment(object):

        def __init__(self , experimentId = -1):
                self.experimentId = experimentId
                if not self.isExists():
                        raise Exception('experiment isnt exists')
                self.initAtrributes()
                return


        def initAtrributes(self):
                
                ##ATTRIBUTES##
                self.name = xl.getAttributeValue('name',self.experimentId)
                self.done = xl.getAttributeValue('done',self.experimentId)
                self.timeStamp = xl.getAttributeValue('time stamp',self.experimentId)
                
                #dataset
                self.datasetType = xl.getAttributeValue('dataset type',self.experimentId)
                self.croppingMethod = xl.getAttributeValue('cropping method',self.experimentId)
                self.imageEnhancement = xl.getAttributeValue('image enhancement',self.experimentId)
               
                #neural network
                self.networkSubType = xl.getAttributeValue('network sub type',self.experimentId)
                self.minLayer = int(xl.getAttributeValue('min layer to extract',self.experimentId))
                self.maxLayer = int(xl.getAttributeValue('max layer to extract',self.experimentId))
                
                #classifier
                if xl.getAttributeValue('use PCA',self.experimentId) == 'y':
                        self.usePCA = True
                else:
                        self.usePCA = False
                self.classifierType = xl.getAttributeValue('classifier type',self.experimentId)
                self.classifierSubType = xl.getAttributeValue('classifier sub type',self.experimentId) 
                        #valid values : linear , poly , rbf , sigmoid
                self.resultsType = xl.getAttributeValue('results type',self.experimentId)
                
                if self.resultsType == 'AUC':
                        self.useProbabilities = True
                else:
                        self.useProbabilities = False

                self.testingMethod = xl.getAttributeValue('testing method',self.experimentId)
                self.levelList = self.getLayersList()
                                
                ##PATH##
                self.experimentDir = EXPERIMENT_RESULTS_DIR + '/' + self.getExperimentName()
                self.logDir = self.experimentDir + '/log'
                self.datasetDir = DATASET_DIR + '/' + self.getDatasetName()
                self.featuresDir = FEATURES_DIR + '/' + self.getFeaturesName()

                ##LOG##
                self.mainLogPath = self.logDir + '/mainLog.log'
                self.mainLog = None

                ##RESULTS FILE##
                self.resultsFile = self.experimentDir + '/results.%s.xlsx'%self.name 

                return


        def createDirectories(self):

                if(not os.path.exists(EXPERIMENT_RESULTS_DIR)): 
                        os.mkdir(EXPERIMENT_RESULTS_DIR)      

                if(not os.path.exists(self.experimentDir)):
                        os.mkdir(self.experimentDir)

                if(not os.path.exists(self.logDir)):
                        os.mkdir(self.logDir)

                if(not os.path.exists(FEATURES_DIR)):
                        os.mkdir(FEATURES_DIR)
                
                if(not os.path.exists(self.featuresDir)):
                        os.mkdir(self.featuresDir)

                if(not os.path.exists(DATASET_DIR)):
                        os.mkdir(DATASET_DIR)

                #no need to do this
                #if(not os.path.exists(self.datasetDir)):
                #        os.mkdir(self.datasetDir)

                return

        def string(self):
                return "TODO"
                

        def openLog(self):
                self.mainLog = open(self.mainLogPath,'w')
                self.mainLog.write('')
                self.mainLog = open(self.mainLogPath,'a')

        def closeLog(self):
                self.mainLog.close()
               
        def createDataset(self):
                self.mainLog.write('@@@@\tSTARTING createDataset\t@@@@\n')

                logPath = self.logDir + '/' + 'preprocess.log'
                croppingMethdNum = -1

                if(self.croppingMethod == 'smart_crop'):
                        croppingMethdNum = 0
                elif(self.croppingMethod == 'no_crop'):
                        croppingMethdNum = 10
                else:
                        raise Exception('invalid cropping method')

                if(os.path.exists(self.datasetDir)):
                        return

                pre.preprocess(logPath,DATASET_SIGMENTATION_DIR,DATASET_SRC_DIR,self.datasetDir,\
                croppingMethdNum,\
                None,10,\
                101,311)

                return

        def extractFeatures(self):
                self.mainLog.write('@@@@\tSTARTING extractFeatures\t@@@@\n')

                for layer in range(self.minLayer,self.maxLayer+1):
                        featureExtraction.extractLayer(layer,self.datasetDir,self.featuresDir,self.networkSubType,self.datasetType)
                return

        def runClassifier(self):

                self.mainLog.write('@@@@\tSTARTING runClassifier\t@@@@\n')

                if(not self.testingMethod == 'leave_one_out'):
                        raise Exception('invalid testing method')
                
                #initialize experiment
                subExperimentNum = -1
                accuracyRateVector = []
                AUCVector = []
                
                #create xls results files and copy experiment atrributes to the head of the file
                self.createResultsFile()
                
                for layers in self.layersList:
                        
                        subExperimentNum +=1

                        #write to xls file
                        self.writeNewSubExperiment(subExperimentNum,layers)

                        #instance classifier
                        if(self.classifierType == 'SVM'):
                                classifier = svm.SVC(kernel = str(self.classifierSubType) , probability = self.useProbabilities)
                        else:
                                raise Exception('invalid classifier type') 
                        
                        #feature parsing
                        [imageId , imageFiles , features , groundTruth] = featureParsing.dirFeatureParsing(\
                        self.featuresDir,\
                        layers,\
                        self.datasetType,\
                        self.logDir + '/' + 'featureParsing_%s.log'%layers)
                        
                        #initialize sub-experiment
                        datasetSize = len(imageId)
                        probabilitiesVector = np.zeros((datasetSize,2))
                        successVector = np.zeros((datasetSize))

                        for i in range(datasetSize):
                                #create test dataset (one image at a time)
                                [test_imageId , test_imageFiles , test_features , test_groundTruth] =\
                                [imageId[i] , imageFiles[i] , features[i] , groundTruth[i]]
                                
                                #create training dataset
                                [train_imageId , train_imageFiles , train_features , train_groundTruth] =\
                                [list(imageId) , list(imageFiles) , list(features) , list(groundTruth)]
                                
                                train_imageId.pop(i)
                                train_imageFiles.pop(i)
                                train_features.pop(i)
                                train_groundTruth.pop(i)

                                #shuffle training dataset
                                [train_imageId , train_imageFiles , train_features , train_groundTruth] =\
                                sh.shuffleLists(train_imageId , train_imageFiles , train_features , train_groundTruth)

                                #writing log header
                                self.mainLog.write('\n==start training dataset - tested sample is %s==\n'%test_imageId)

                                #PCA
                                if self.usePCA is True:
                                        pca = PCA(n_components=None)
                                        old_train_features = train_features
                                        pca.fit(old_train_features)
                                        train_features = pca.transform(old_train_features)
                                        
                                        #write to log
                                        self.mainLog.write('\n==DONE PCA==\n')
                                        self.mainLog.write('original features dim is %s\n'%len(old_train_features[0]))
                                        self.mainLog.write('new features dim is %s\n'%len(train_features[0]))
                                else:
                                        self.mainLog.write('\n==not using PCA==\n')


                                #write to log
                                self.mainLog.write('\ntest dataset:\n')
                                self.mainLog.write('ID\tnFiles\tnFeatures\tgTruth\n')
                                self.mainLog.write('%s\t,%s\t,%s\t,%s\n' %(test_imageId , len(test_imageFiles) , len(test_features) , test_groundTruth))

                                self.mainLog.write('train dataset:\n')
                                self.mainLog.write('ID\tnFiles\tnFeatures\tgTruth\n')
                                for j in range(len(train_features)):
                                        self.mainLog.write('%s\t,%s\t,%s\t,%s\n' %(train_imageId[j] , len(train_imageFiles[j]) , len(train_features[j]) , train_groundTruth[j]))

                                #assert vectors size
                                assert len(train_imageId) == datasetSize -1
                                assert len(train_imageFiles) == datasetSize -1
                                assert len(train_features) == datasetSize -1
                                assert len(train_groundTruth) == datasetSize -1

                                for j in range(len(train_features)):
                                        assert len(train_features[j]) == len(train_features[0])
                                
                                #trainig classifier
                                train_array = np.array(train_groundTruth)
                                #train_array = train_array.reshape(-1, 1)#single feature
                                classifier.fit(train_features , train_array)

                                #testing classifier
                                if self.usePCA is True:
                                        test_features = pca.transform(test_features)

                                #test_features = test_features.reshape(1,-1)#single sample

                                if self.useProbabilities == True:
                                        probabityResult = classifier.predict_proba(test_features)
                                else:
                                        probabityResult = None
                                
                                predictionResult = classifier.predict(test_features)

                                #append results
                                if self.useProbabilities == True:
                                        probabilitiesVector[i,:] = np.asarray(probabityResult).reshape(1,2)
                                
                                if predictionResult == groundTruth[i]:
                                        successVector[i] = 1
                                else:
                                        successVector[i] = 0
                                
                                #calculate distance from hyperplane
                                if self.classifierSubType == 'linear': #and self.useProbabilities == False:
                                        y = classifier.decision_function(test_features)
                                        w_norm = np.linalg.norm(classifier.coef_)
                                        distanceFromHyperplane = y / w_norm
                                        assert distanceFromHyperplane.shape == (1,)
                                        distanceFromHyperplane = distanceFromHyperplane[0]
                                else:
                                        distanceFromHyperplane = None

                                #write results to xl
                                self.writeResult(subExperimentNum,i,imageId[i],groundTruth[i],successVector[i],probabityResult,predictionResult,distanceFromHyperplane)

                        #summaries sub experiment
                        accuracyRateVector.append(      self.calcAccuracyRate(successVector,datasetSize))
                        AUCVector.append(               self.calcAUC(probabilitiesVector,groundTruth,datasetSize))
                        self.subExperimentSummary(subExperimentNum,datasetSize,layers,accuracyRateVector[subExperimentNum],AUCVector[subExperimentNum],
                                                        successVector,probabilitiesVector,groundTruth)

                #summaries experiment
                self.experimentSummary(accuracyRateVector,AUCVector,self.layersList,subExperimentNum+1)
                        
                return
        
        def execute(self):

                if(not self.isExists()):
                        return
                if (self.isDone()):
                        return               
                
                self.createDirectories()
                self.openLog()
                self.setTimeStamp()

                self.createDataset()
                self.extractFeatures()
                self.runClassifier()
                self.markDone()
                self.closeLog()

                return

        def createResultsFile(self):
                os.system('cp ' + EXPERIMENT_RESULTS_TEMPLATE + ' ' + self.resultsFile)
                xl.copyRow(EXPERIMENTS_FILE,int(ATTRIBUTES_ROW)-1,self.resultsFile,2)
                xl.copyRow(EXPERIMENTS_FILE,int(ATTRIBUTES_ROW),self.resultsFile,3)
                xl.copyRow(EXPERIMENTS_FILE,xl.getExperimentRow(self.experimentId),self.resultsFile,4)
                return

        def openResultsFile(self):
                wb = xl.load_workbook(filename= self.resultsFile)
                ws = wb[RESULTS_TAB]
                return [wb,ws]

        def saveResultFile(self,wb):
                wb.save(self.resultsFile)
                return

        def writeNewSubExperiment(self,exp_i , layers):
                [wb,ws] = self.openResultsFile()
                starting_col = RESULTS_SUB_EXPERIMENT_WIDTH*exp_i
                
                thin = Side(border_style="thin", color="000000")
                double = Side(border_style="double", color="000000")
                _border_reg = Border(top=thin, left=thin, right=thin, bottom=thin)
                _border_start = Border(top=thin, left=double, right=thin, bottom=thin)


                ws[get_column_letter(starting_col + 1)\
                + str(RESULTS_TITLES_ROW-1)].value = 'Layers: %s'%(layers)
                ws[get_column_letter(starting_col + 1)\
                + str(RESULTS_TITLES_ROW-1)].font = Font(bold=True)
               
                ws[get_column_letter(starting_col + 1)\
                + str(RESULTS_TITLES_ROW)].value = '#'
                ws[get_column_letter(starting_col + 1)\
                + str(RESULTS_TITLES_ROW)].border = _border_start

                ws[get_column_letter(starting_col + 2)\
                + str(RESULTS_TITLES_ROW)].value = 'ground truth'
                ws[get_column_letter(starting_col + 2)\
                + str(RESULTS_TITLES_ROW)].border = _border_reg

                ws[get_column_letter(starting_col + 3)\
                + str(RESULTS_TITLES_ROW)].value = 'prediction'
                ws[get_column_letter(starting_col + 3)\
                + str(RESULTS_TITLES_ROW)].border = _border_reg

                ws[get_column_letter(starting_col + 4)\
                + str(RESULTS_TITLES_ROW)].value = 'success'
                ws[get_column_letter(starting_col + 4)\
                + str(RESULTS_TITLES_ROW)].border = _border_reg

                ws[get_column_letter(starting_col + 5)\
                + str(RESULTS_TITLES_ROW)].value = 'dist. from plane'
                ws[get_column_letter(starting_col + 5)\
                + str(RESULTS_TITLES_ROW)].border = _border_reg
                
                ws[get_column_letter(starting_col + 6)\
                + str(RESULTS_TITLES_ROW)].value = 'probability'
                ws[get_column_letter(starting_col + 6)\
                + str(RESULTS_TITLES_ROW)].border = _border_reg
               
                self.saveResultFile(wb)
                return

        def writeResult(self,exp_i,res_i,_id,_gtruth,_success,_probability,_prediction,_distanceFromHyperplane):
                [wb,ws] = self.openResultsFile()

                starting_col = RESULTS_SUB_EXPERIMENT_WIDTH*exp_i

                p_id = get_column_letter(starting_col + 1) + str(RESULTS_TITLES_ROW+1 + res_i)
                p_groundTruth = get_column_letter(starting_col + 2) + str(RESULTS_TITLES_ROW+1 + res_i)
                p_prediction = get_column_letter(starting_col + 3) + str(RESULTS_TITLES_ROW+1 + res_i)
                p_success = get_column_letter(starting_col + 4) + str(RESULTS_TITLES_ROW+1 + res_i) 
                p_dist =  get_column_letter(starting_col + 5) + str(RESULTS_TITLES_ROW+1 + res_i)
                p_probbability = get_column_letter(starting_col + 6) + str(RESULTS_TITLES_ROW+1 + res_i)
                
                #writing content
                ws[p_id].value = str(_id)
                ws[p_groundTruth].value = str(_gtruth) 
                ws[p_prediction].value = str(_prediction[0])
                ws[p_success].value = "%d"%(_success) #'=IF(%s=%s,1,0)'%(p_groundTruth,p_prediction)

                if _distanceFromHyperplane is not None:
                        ws[p_dist].value = "%.2f"%_distanceFromHyperplane

                if self.useProbabilities == True:
                        ws[p_probbability].value = str(_probability[0])
                
                #adding colors
                if(_gtruth == _prediction[0]):
                        color = 'C7DFB6' #GREEN
                else:
                        color = 'FFC7C7' #RED

                #filling green for success , red o.w.
                ws[p_success].fill = PatternFill("solid", fgColor=color)

                #adding border
                thin = Side(border_style="thin", color="000000")
                double = Side(border_style="double", color="000000")
                _border_reg = Border(top=thin, left=thin, right=thin, bottom=thin)
                _border_start = Border(top=thin, left=double, right=thin, bottom=thin)

                ws[p_id].border = _border_start
                ws[p_groundTruth].border = _border_reg
                ws[p_prediction].border = _border_reg
                ws[p_success].border = _border_reg
                ws[p_dist].border = _border_reg
                ws[p_probbability].border = _border_reg

                self.saveResultFile(wb)               
                return


        def writeSubExperimentSummary(self,exp_i,datasetSize,layers,accuracyRate,AUCscore):
                [wb,ws] = self.openResultsFile()

                starting_col = RESULTS_SUB_EXPERIMENT_WIDTH*exp_i

                res_col = get_column_letter(starting_col + 4)
                res_min = res_col + str(RESULTS_TITLES_ROW+1)
                res_max =  res_col + str(RESULTS_TITLES_ROW+datasetSize)
                
                p_layers = get_column_letter(starting_col + 1) + str(RESULTS_TITLES_ROW+1 + datasetSize)
                p_sum = get_column_letter(starting_col + 3) + str(RESULTS_TITLES_ROW+1 + datasetSize)
                p_res = get_column_letter(starting_col + 4) + str(RESULTS_TITLES_ROW+1 + datasetSize)
                p_auc = get_column_letter(starting_col + 5) + str(RESULTS_TITLES_ROW+1 + datasetSize)
                p_auc_res = get_column_letter(starting_col + 6) + str(RESULTS_TITLES_ROW+1 + datasetSize)
                
                ws[p_layers].value = 'Layers: %s'%(layers)
                ws[p_layers].font = Font(bold=True)
                

                ws[p_sum].value = 'accuracy rate (%)'
                ws[p_sum].font = Font(bold=True)
                #ws[p_res].value = '=SUM(%s:%s)/%s*100'%(res_min,res_max,datasetSize)
                ws[p_res].value = "%.4f"%accuracyRate

                ws[p_auc].value = 'AUC'
                ws[p_auc].font = Font(bold=True)
                ws[p_auc_res].value = '%.4f'%(AUCscore)
                
                #if self.resultsType == 'AUC':
                #        assert datasetSize == len(probabilitiesVector[:,1])
                #        assert datasetSize == len(groundTruth)
                #        AUCscore = metrics.roc_auc_score(groundTruth, probabilitiesVector[:,1])
                #        ws[p_auc].value = 'AUC'
                #        ws[p_auc].font = Font(bold=True)
                #        ws[p_auc_res].value = '%.4f'%(AUCscore)

                self.saveResultFile(wb)
                return

        def calcAccuracyRate(self,successVector,datasetSize):
                accuracyRate =  sum(successVector)/float(datasetSize)
                return accuracyRate

        def calcAUC(self,probabilitiesVector,groundTruth,datasetSize):
                if self.resultsType == 'AUC':
                        assert datasetSize == len(probabilitiesVector[:,1])
                        assert datasetSize == len(groundTruth)
                        AUC = metrics.roc_auc_score(groundTruth, probabilitiesVector[:,1])
                else:
                        AUC = 0
                return AUC
        
        def createROCplot(self,exp_i,datasetSize,layers,probabilitiesVector,groundTruth):

                self.mainLog.write("\n@ starting createROCplot for layer %s\n"%layers)
                self.mainLog.write("got probabilitiesVector: \n %s"%probabilitiesVector)
                self.mainLog.write("got groundTruth vector: \n %s"%groundTruth)


                assert datasetSize == len(probabilitiesVector[:,1])
                assert datasetSize == len(groundTruth)
                
                #calc AUC
                AUCscore = metrics.roc_auc_score(groundTruth, probabilitiesVector[:,1])
                self.mainLog.write("calculated AUC score %.4f\n"%AUCscore)

                #calc ROC points
                [fpr , tpr , _] = metrics.roc_curve(groundTruth,probabilitiesVector[:,1])
                self.mainLog.write("calculated #fpr#\t#tpr#\n")
                for i in range(len(fpr)):
                        self.mainLog.write("%.2f ,\t %.2f\n"%(fpr[i],tpr[i]))
                
                plt.figure()
                lw = 2
                plt.plot(fpr, tpr, color='darkorange',
                        lw=lw, label='ROC curve for (area = %.4f)' % (AUCscore))
                plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title("ROC for layers %s , experiment_id [%d] \n dataset [%s]"%(layers,self.experimentId,self.datasetType))
                plt.legend(loc="lower right")
                plt.savefig(os.path.join(self.experimentDir,"ROC_fig_lvl_%s.jpg"%layers),format='jpg')

                self.mainLog.write("\n@ done createROCplot for layer %s\n"%layers)

                return

        def subExperimentSummary(self,subExperimentNum,datasetSize,layersList,accuracyRate,AUCscore,successVector,probabilitiesVector,groundTruth):
                
                self.writeSubExperimentSummary(subExperimentNum,datasetSize,layersList,accuracyRate,AUCscore)
                if self.resultsType == 'AUC':
                        self.createROCplot(subExperimentNum,datasetSize,layersList,probabilitiesVector,groundTruth)

                self.mainLog.write("\n==sub-experiment(%d) - for layers %s summary==\n"%(subExperimentNum,layersList))
                self.mainLog.write("dataset size is %d\n"%datasetSize)
                self.mainLog.write("AUC score is %.4f , accuracy rate is %.4f\n"%(AUCscore,accuracyRate))
                self.mainLog.write("success vector:\n%s\n\n"%successVector)
                self.mainLog.write("probabilities vector:\n%s\n\n"%probabilitiesVector)
                self.mainLog.write("groundTruth vector:\n%s\n\n"%groundTruth)

                return

        def experimentSummary(self,accuracyRateVector,AUCVector,layersFullList,SubExperimentsNum):
                self.mainLog.write("\n==EXPERIMENT [%s] SUMMARY==\n"%(self.name))
                self.mainLog.write("#\tlayers\taccuracy\tAUC\n")
                for i in range(SubExperimentsNum):
                        self.mainLog.write("%d\t%s\t%.4f\t%.4f\n"%(i,layersFullList[i],accuracyRateVector[i],AUCVector[i]))         
                self.mainLog.write("\n")

                plt.figure()
                lw = 2
                plt.plot(range(1,SubExperimentsNum+1), accuracyRateVector, 'ro', label='accuracy rate')
                plt.plot(range(1,SubExperimentsNum+1), AUCVector,          'bs', label='AUC 0f ROC score')
                plt.xlabel('classifier based on OVERFEAT layer # features')
                plt.ylabel('AUC / accuracy rate')
                plt.title("experiment [%s] ,dataset[%s]\naccuracy rate & AUC of ROC scores"%(self.name,self.datasetType))
                plt.legend(loc="lower right")
                plt.savefig(os.path.join(self.experimentDir,"summary_plot_%s.jpg"%self.name),format='jpg')
                return


        def markDone(self):
                [wb,ws] = xl.loadExperiments()
                ws[xl.getAttributeCol('done') + xl.getExperimentRow(self.experimentId)].value = 'y'
                self.done = 'y'
                xl.saveExperiments(wb)
                return

        def isDone(self):
                if (self.done == 'y'):
                        return 1
                else:
                        return 0

        def isExists(self):
                [wb,ws] = xl.loadExperiments()
                for row in range(int(ATTRIBUTES_ROW)+1,ws.max_row+1):
                        cell = ws[EXPERIMENT_NUM_COL + str(row)]
                        try:
                                if(int(cell.value) == self.experimentId):
                                        return 1
                        except TypeError:
                                continue

                return 0

        def getTimeStamp(self):
                return strftime("%d_%m_%Y_%H:%M:%S", localtime())

        def setTimeStamp(self):
                [wb,ws] = xl.loadExperiments()
                ws[xl.getAttributeCol('time stamp') + xl.getExperimentRow(self.experimentId)].value = self.getTimeStamp()
                xl.saveExperiments(wb)
                return

        def getDatasetName(self):
                return 'dataset.'\
                + xl.getAttributeValue('cropping method',self.experimentId) + '.'\
                + xl.getAttributeValue('image enhancement',self.experimentId)

        def getFeaturesName(self):
                return 'features.'\
                + xl.getAttributeValue('cropping method',self.experimentId) + '.'\
                + xl.getAttributeValue('image enhancement',self.experimentId) + '.'\
                + xl.getAttributeValue('network type',self.experimentId) + '.'\
                + xl.getAttributeValue('network sub type',self.experimentId)
                

        def getExperimentName(self):
                return 'experiment.'\
                + str(self.experimentId) + '.'\
                + self.name + '.'\
                + self.getTimeStamp()

        def getLayersList(self):
                self.layersList = xl.getAttributeValue('layers list',self.experimentId)
                self.layersList = self.layersList.split(';')
                for i in range(len(self.layersList)) :
                        self.layersList[i] = self.layersList[i].split(',')
                for i in range(len(self.layersList)) :
                        if type(self.layersList[i]) is list:
                                for j in range(len(self.layersList[i])):
                                        self.layersList[i][j] = int(self.layersList[i][j])
                        else:
                                self.layersList[i] = int(self.layersList[i])


