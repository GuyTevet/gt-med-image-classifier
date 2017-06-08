##RUN SCRIPT
from experiment import *

def getMaxExperimentNum():
        [wb,ws] = xl.loadExperiments()
        experiments = []
        for row in range(int(ATTRIBUTES_ROW)+1,ws.max_row+1):
                cell = ws[EXPERIMENT_NUM_COL + str(row)]
                #if cell.value.type is not 'NoneType':
                try:
                        experiments.append(int(cell.value))
                except TypeError:
                        continue
        return max(experiments)

def isExperimentExists(experimentId):
        [wb,ws] = xl.loadExperiments()
        for row in range(int(ATTRIBUTES_ROW)+1,ws.max_row+1):
                cell = ws[EXPERIMENT_NUM_COL + str(row)]
                try:
                        if(int(cell.value) == experimentId):
                                return 1
                except TypeError:
                        continue
        return 0
        
def executeAllExperiments():
        for i in range(getMaxExperimentNum()+1):
                if isExperimentExists(i):
                        experiment = Experiment(i)
                        experiment.execute()

executeAllExperiments()               
