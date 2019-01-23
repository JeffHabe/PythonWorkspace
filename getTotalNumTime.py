# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 19:41:55 2018

@author: Jeff PC
"""
from os import walk,makedirs
import os.path as pth 
import numpy as np
from math import pi
import csv 
from scipy.signal import savgol_filter
import pandas as pd 
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import plot
import datetime
from numpy.polynomial import chebyshev as chy
import random
cf.go_offline()
mypath ='excelFolder/'
import time
def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return f
def readCSV(fileName):
    data=[]
    times=[]
    f = open(mypath+fileName+'.csv', 'r')
    for row in csv.DictReader(f):
        ms=float(row['timestamp'])
        date=datetime.datetime.fromtimestamp(ms)
        #print(date)
        times.append(date)
        data.append(float(row['value']))
    f.close()
    return (data,times)



fileName=getFileName(mypath)
totT=0
cnt=0
fName=[]
aryTimes=[]
maxSecond=[]
meanSecond=[]
minSecond=[]
maxSTime=[]
for i in range(0,len(fileName)): 
    #i=rndFile
    
    sensorType=fileName[i][6:]  
    #print(sensorType)
    if(sensorType=='T1'):
        cnt+=1
        cuntT=0
        #if(cnt !=8 and cnt!=12 and cnt!=17 and  cnt!=18 and cnt!=29 ):
            #print(fileName[i])
        data,times=readCSV(fileName[i])
        totT+=len(times)
        aryTimes.append(len(times))
        second=[int(times[n+1].timestamp())-int(times[n].timestamp()) for n in range(len(times)-1)]
        #print(second)
        for t in second:
            #print(t)
            if(t>=30 and t<=60):
                cuntT+=1
        meanSecond.append(round(np.mean(second)))
        maxSecond.append(np.max(second))
        minSecond.append(np.min(second))
        maxSTime.append(cuntT)
        fName.append(fileName[i][:-3])
       #print(fileName[i][:-3])
dictData={'Date':fName,
          '#time':aryTimes,
          'mean Second':meanSecond,
          'minSecond':minSecond,
          'maxSecond':maxSecond,
          'count Max Time':maxSTime
          }
        #print(times[1].timestamp())
pd.DataFrame(dictData).to_excel('.\Data LFS\\DateDetial_more30_less60.xlsx')

print(np.mean(maxSecond))
print('total num of time :',totT,'count: ',cnt)
print(totT/cnt)

                