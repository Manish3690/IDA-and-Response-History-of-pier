import openseespy.opensees as op
import opsvis as opsv
# import vfo.vfo as vfo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from PierModel import ModelPier, units, materialProperties




def analysis(key, value):
    earthquake= pd.read_csv(key)
    earthquake.dropna(inplace=True)
    Eq=earthquake.iloc[:, 0].to_numpy()
    timesteps= len(Eq)
    i=0
    time=[0]*timesteps
    if value== 0.005:
        limiter=3
    elif value==0.0025:
        limiter=4
    else:
        limiter=2
        
    for i in range(timesteps):
        time[i]=round(i*value,limiter)
    Eq=earthquake.iloc[:, 0].to_numpy()
    print(Eq)

    
    op.wipeAnalysis()
    
    op.recorder('Node','-file',f"Recorders/{key}disp102.out",'-time','-node',102,'-dof',1,'disp')
    # op.recorder('Node','-file','Recorders/reactionBottom.out','-time','-node',102,'-dof',*[1,2],'reaction')
      
    
    # print(time)  
    # plt.plot(time,earthquake)
    # plt.show()
    
    
    
    
    op.remove("timeSeries",1)
    op.remove("pattern",1)
    op.timeSeries("Path",1,'-values',*Eq,"-time",*time,"-factor",9.81)
    op.pattern("UniformExcitation",1,*[1],"-accel",1)#here
    
    # op.timeSeries('Path',4, '-dt', 0.005, '-values',file_path, '-factor', 9.81)
    # op.timeSeries('Path', 4, '-dt', 0.02, '-filePath', '"C:\\Users\\acer\\Desktop\\Pounding in bridge\\Bijayapur 2.0\\code\\Finalized model\\elcentro.csv"', '-factor', 9.81)
    # ops.pattern('UniformExcitation',200,1,'-accel',2)
    # op.pattern('UniformExcitation',4,1,'-accel',4)
    op.system('BandSPD')
    op.test('NormDispIncr',1.e-3,100)
    # op.algorithm('Newton')
    # op.algorithm('NewtonLineSearch')
    op.algorithm('Newton')
    op.constraints('Transformation')
    # op.integrator('Newmark',0.5,0.25)
    alpha=0.85
    gamma=1.5-alpha
    beta=(2-alpha)**2/4
    op.integrator('HHT', 0.85, gamma, beta)
    op.numberer('RCM')
    op.analysis('Transient')
    # dt = np.diff(time)[0]
    # dt=0.02
    # step = 0
    # loadFactor = list()
    print(f"The analysis of {key} has started.")
    k=op.analyze(len(Eq),value)


    df=pd.read_csv(f"Recorders/{key}disp102.out", delimiter=" ").iloc[:, 1]
    time = time[:len(df)]
    plt.plot(time, df)
    plt.xlabel("Time(sec)")
    plt.ylabel(f"Disp at the top of pier (mm) for {key}")
    plt.show()
    plt.savefig(f"Recorders/Response history/{key}photo.jpg")


    
def drift_ratio_ma(key,scale,value):

    units()
    materialProperties()
    ModelPier()


    earthquake= pd.read_csv(key)
    earthquake.dropna(inplace=True)
    Eq=earthquake.iloc[:, 0].to_numpy()
    timesteps= len(Eq)
    i=0
    time=[0]*timesteps
    if value== 0.005:
        limiter=3
    elif value==0.0025:
        limiter=4
    else:
        limiter=2
        
    for i in range(timesteps):
        time[i]=round(i*value,limiter)
    Eq=earthquake.iloc[:, 0].to_numpy()
    # print(Eq)

    
    op.wipeAnalysis()
    
    op.recorder('Node','-file',f"RecordersIDA/{key}{scale}disp102.out",'-time','-node',102,'-dof',1,'disp')
    op.recorder('Node','-file',f'RecordersIDA/{key}{scale}disp103.out','-time','-node',103,'-dof',1,'disp')
      
    
    # print(time)  
    # plt.plot(time,earthquake)
    # plt.show()
    
    
    
    
    op.remove("timeSeries",1)
    op.remove("pattern",1)
    op.timeSeries("Path",1,'-values',*Eq,"-time",*time,"-factor",scale)
    op.pattern("UniformExcitation",1,*[1],"-accel",1)#here
    
    # op.timeSeries('Path',4, '-dt', 0.005, '-values',file_path, '-factor', 9.81)
    # op.timeSeries('Path', 4, '-dt', 0.02, '-filePath', '"C:\\Users\\acer\\Desktop\\Pounding in bridge\\Bijayapur 2.0\\code\\Finalized model\\elcentro.csv"', '-factor', 9.81)
    # ops.pattern('UniformExcitation',200,1,'-accel',2)
    # op.pattern('UniformExcitation',4,1,'-accel',4)
    op.system('BandSPD')
    op.test('NormDispIncr',1.e-3,100)
    # op.algorithm('Newton')
    # op.algorithm('NewtonLineSearch')
    op.algorithm('Newton')
    op.constraints('Transformation')
    # op.integrator('Newmark',0.5,0.25)
    alpha=0.85
    gamma=1.5-alpha
    beta=(2-alpha)**2/4
    op.integrator('HHT', 0.85, gamma, beta)
    op.numberer('RCM')
    op.analysis('Transient')
    # dt = np.diff(time)[0]
    # dt=0.02
    # step = 0
    # loadFactor = list()
    print(f"The analysis of {key}{scale} has started.")
    k=op.analyze(len(Eq),value)

    if k==0:
        df1=pd.read_csv(f"RecordersIDA/{key}{scale}disp102.out", delimiter=" ").iloc[:,1]
        df2= pd.read_csv(f"RecordersIDA/{key}{scale}disp103.out", delimiter=" ").iloc[:,1]
        drift_ratio= (abs(df1)-abs(df2))*100/6
        drift_ratio_max =drift_ratio.max()

        return k, drift_ratio_max
    else:
        return k,0

