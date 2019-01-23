# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 22:03:28 2018

@author: Jeff PC
"""


import random
from os import walk,makedirs

def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return f
mypath ='excelFolder/'
fileName=getFileName(mypath)
print(len(fileName))
reset=True

# =============================================================================
# for t in range(10):
#     a=random.sample(range(158),10)#不重複
#     print(a)
# =============================================================================
if(reset):
    rndList=[]
    fin=True  
    cntT=0
    cntH=0
    i=0
    while(fin):
        #n=random.randint(0,len(fileName)-1)#不重複
        sensorType=fileName[i][6:-1]
        print(fileName[i])
        if(sensorType=='T'):
                #rndList.append(n)
            cntT+=1
        elif(sensorType=='H'):
                #rndList.append(n)
            cntH+=1 
        if(len(rndList)==len(fileName)or (i==len(fileName)-1)):
            fin=False
        else:
             i+=1
            
print('T: ',cntT,'H: ',cntH)
# =============================================================================
# for n in range(len(rndList)):
#     sensorType=fileName[n][6:-1]
#     print(sensorType,end=' ')
# print()    
# =============================================================================
