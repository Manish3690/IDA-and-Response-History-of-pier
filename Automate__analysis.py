# Calculation of time period of structure:

import openseespy.opensees as op
import opsvis as opsv
# import vfo.vfo as vfo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import necessary modules
from PierModel import units, materialProperties, ModelPier
from DynamicAnalysis import analysis, drift_ratio_ma

def automationIDA(filename, dt):
    sf = [0]*41
    drift_ratio = [0]*40
    count = 0

    # Initialize the first value in sf
    sf[0]=0.1
    
    
    while count<40:
        k, drift_ratio_value = drift_ratio_ma(filename, sf[count], dt)
        if k==0 and count>=2:
            drift_ratio[count]=drift_ratio_value
            count+=1
            sf[count]=round(sf[count-1]*1.2,2)
        elif k!=0 and count>=2:
            sf[count]=round((sf[count]+sf[count-1])/3,2)
        elif k==0 and count<2:
            drift_ratio[count]=drift_ratio_value
            count+=1
            sf[count]=round(sf[count-1]*1.5,2)
        else:
            sf[count]=round(sf[count]/1.8,2)
    # k, drift_ratio_value = drift_ratio_ma(filename, sf[count], dt)
    # drift_ratio[count]=drift_ratio_value
            
    return sf,drift_ratio
    
