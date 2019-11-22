# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 13:52:32 2018

@author: Jeff PC
"""

from os import walk,makedirs
import datetime,time
import os.path as pth 
#mypath ='excelFolder/'
import csv 

def getFileName(mypath=''):
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return f

def mkfolder(directory):
    if not pth.exists(directory):
        makedirs(directory)
        
def readCSV(mypath,fileName):
    data=[]
    times=[]
    f = open(mypath+fileName+'.csv', 'r')
    for row in csv.DictReader(f):
        ms=float(row['timestamp'])
        #print(ms)
        date=datetime.datetime.utcfromtimestamp(ms)
        #print(time.mktime(date.timetuple()))
        #date1=datetime.datetime.utcfromtimestamp(ms).strftime('%Y-%m-%d %H:%M:%S.%f')
        #print(date)
        times.append(date)
        data.append(float(row['value']))
    f.close()
    return (data,times)
    #print(data)

