# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:19:22 2018

@author: User
"""
from os import listdir,walk
#from os.path import isfile,join 
mypath ='excelFolder'
# =============================================================================
# onlyfiles=[f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
# =============================================================================
t={'index':'date'}
n=0
Tcnt=0
Hcnt=0
Vcnt=0
SWcnt=0
Lcnt=0
for (dirpath, dirnames, filenames) in walk(mypath):
    f=list(filenames[i][:-4]for i in range(len(filenames)))    
    idx=list(i for i in range(len(filenames)))    
    for n in range(len(filenames)):
        print(n,':',filenames[n][:-4])
        if(filenames[n][6:-5]=="T"):
            Tcnt+=1
        if(filenames[n][6:-5]=="H"):
            Hcnt+=1
        if(filenames[n][6:-5]=="V"):
            Vcnt+=1
        if(filenames[n][6:-5]=="SW"):
            SWcnt+=1
        if(filenames[n][6:-5]=="L"):
            Lcnt+=1
print('# of T =',Tcnt)
print('# of H =',Hcnt)
print('# of V =',Vcnt)
print('# of SW =',SWcnt)
print('# of L =',Lcnt)
    #break
#print(t)