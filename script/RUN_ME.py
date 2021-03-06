#!/usr/bin/env python

"""
    File name:          RUN_ME.py
    Author:             Guy Tevet
    Date created:       9/6/2017
    Date last modified: 9/6/2017
    Description:        running script:
                        1.parsing all unexecuted experiments from experiments.xlsx
                        2.instansing an Experiment class for each unexecuted experiment
                        3.executing all experiments
"""

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
