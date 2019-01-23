# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 23:40:21 2018

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

def mkfolder(directory):
    if not pth.exists(directory):
        makedirs(directory)
        

def readCSV(fileName):

    f = open(mypath+fileName+'.csv', 'r')
    for row in csv.DictReader(f):
        ms=float(row['timestamp'])
        date=datetime.datetime.fromtimestamp(ms)
        #print(date)
        times.append(date)
        data.append(float(row['value']))
    f.close()
    return (data,times)
    #print(data)
def getRnSData(SGwd_length,SGpolyOrd):
    for i in range(len(data)):
        t.append(i)
        v.append(float(data[i]))
    #sgf=savgol_filter(data,SGwd_length,SGpolyOrd)
# =============================================================================
#     global pltData
#     #print(times)
#     pltData += [
#         go.Scatter(
#             x=times, # assign x as the dataframe column 'x'
#             y=v,
#             name='raw data',
#             mode='lines+markers',
#             marker=dict(
#                     size=2,
#                     color='rgba(0,0,255,0.9)'),
#                     )]
# =============================================================================
# =============================================================================
#         go.Scatter(        
#             x=times, # assign x as the dataframe column 'x'
#             y=sgf,
#             name='sgf data',
#             mode='line',
#             marker=dict(
#                     size=5,
#                     color='rgba(0,0,0,0)'),
#                     line=dict(
#                             width=5,
#                             color='rgba(0,255,0,0.9)')
#            )]    
def PlotLy(minr2,wdP,angle,min_ivlP,SGpolyOrd,polyIndex,SGwd_length,fileName,pltData):
    
    layout={'title':fileName+' Plot',
                          'font': dict(size=16)}
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    filePath=".\Plot_html\\SlidingWindow\\"+'R2min_'+str(minr2)+'\\wdS_'+str(wdP)+'angle_'+str(angle)+'\\min_interval_percent_'+str((round(min_ivlP,2)))+'\\' 
    mkfolder(filePath)
    plot(pltData,layout,filename=filePath+fileName+".html")    


v=[]
t=[]
data=[]
times=[]
fileName=getFileName(mypath)
for i in range(0,len(fileName)): 
    #i=rndFile
    sensorType=fileName[i][6:]  
    if(sensorType=='H1'):
        #data,times=readCSV(fileName[i])
        f = open(mypath+fileName[i]+'.csv', 'r')
        for row in csv.DictReader(f):
            ms=float(row['timestamp'])
            date=datetime.datetime.utcfromtimestamp(ms)
            print(date)
            times.append(date)
            if(float(row['value'])>=0 and float(row['value'])<=100):
                data.append(float(row['value']))
            elif(float(row['value'])>100):
                data.append(100.0)
            else:
                data.append(0.0)
            
        f.close()
df={'time':times,
    'value':data}
pd.DataFrame(df).to_excel('Data LFS\\AllHdata.xlsx')
# =============================================================================
#         for i in range(len(data)):
#             t.append(i)
#             v.append(float(data[i]))
# =============================================================================
pltData =[]
pltData += [
        go.Scatter(
            x=times, # assign x as the dataframe column 'x'
            y=data,
            name='raw data',
            mode='lines+markers',
            marker=dict(
                    size=1,
                    color='rgba(0,0,255,0.9)'),
                    )]    
layout={'title':'T_'+'Plot','font': dict(size=16)}
#plot(pltData,layout,filename="T_Plot ALl Data.html")    