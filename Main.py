import openseespy.opensees as op
import opsvis as opsv
# import vfo.vfo as vfo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from PierModel import units, ModelPier
from DynamicAnalysis import analysis
from Automate__analysis import automationIDA

#list of different earthquakes...
ListEQ={
    "cmendocino_dt0.02.txt": 0.02 ,
    "gorkha_dt 0.005.txt": 0.005,
    "kobe_dt 0.01.txt": 0.01,
    "landers.txt": 0.01,
    "lomaprieta_lexdam_dt0.01.txt": 0.01,
    "lomaprieta_losgatos_dt0.005.txt": 0.005,
    "northridge_oliveview_dt 0.01.txt": 0.01,
    "northridge_rinaldi_dt 0.0025.txt": 0.0025
    }

SFDrift={
    "cmendocino_dt0.02.txt": 0 ,
    "gorkha_dt 0.005.txt": 0,
    "kobe_dt 0.01.txt": 0,
    "landers.txt": 0,
    "lomaprieta_lexdam_dt0.01.txt": 0,
    "lomaprieta_losgatos_dt0.005.txt": 0,
    "northridge_oliveview_dt 0.01.txt": 0,
    "northridge_rinaldi_dt 0.0025.txt": 0
    }


SF= [0]*40
Drift=[0]*40


for key, value in ListEQ.items():
    # units()
    # ModelPier()
    # analysis(key, value)     # Use this for response history...
    SFDrift[key]= automationIDA(key, value)
    print(SFDrift[key])
    
    i=0
    for i in range(len(SFDrift[key][1])):
        SF[i]= SFDrift[key][0][i]
        Drift[i]= SFDrift[key][1][i]
    plt.plot(SF,Drift)
    plt.title(key)


    # plt.show()
    plt.savefig(f"IDA Curves/{key[:4]}photo.jpg")


    


    

# Time history analysis and response is plotted upto this.

