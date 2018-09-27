# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:43:40 2018

@author: Jeff PC
"""

from os import walk,makedirs
import csv 
import datetime


mypath ='D:/PythonWorkspace/excelFolder/'

def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        file=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return file

def readCSV(fileName):
    data=[]
    date=0
    sensorType=fileName[6:-1] 
    node_id=int(fileName[7:])
    #print(sensorID)
    f = open(mypath+fileName+'.csv', 'r')
    for row in csv.DictReader(f):
        ms=float(row['timestamp'])
        #pltDate=datetime.datetime.fromtimestamp(ms)
        date=datetime.datetime.utcfromtimestamp(ms)
# =============================================================================
#         if(date.hour != 0)and ((date.hour)%2==0)and(date.minute>=0)and (date.minute<=15):
#             data.append(random.randint(0,10))
#             #print(str(date.hour)+':'+str(date.minute))  
#         else:
# =============================================================================
        if(float(row['value'])>=0 and float(row['value'])<=100):
            value=(float(row['value']))
        elif(float(row['value'])>100):
            value=(100.0)
        else:
            value=(0.0)
        if(sensorType=='T'):
            sensor_id=1
        elif(sensorType=='H'):
            sensor_id=2
        sensor_id={
                'T':1,
                'H':2,
        }[sensorType]
        t=(node_id,sensor_id,date,value)
        data.append(t)
    f.close()
    #print(data)
    return (data)