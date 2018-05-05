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
for (dirpath, dirnames, filenames) in walk(mypath):
    f=list(filenames[i][:-4] for i in range(len(filenames)))
    break
print(f[1][6:])