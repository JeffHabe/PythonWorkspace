# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 23:49:38 2018

@author: Jeff PC
"""

import csv
import re
def readOldList(n):
    AllSpListPath='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllSplist1109.csv'
    results=[]
    with open(AllSpListPath, 'r',) as f:
        reader = csv.reader(f)
        for row in reader:
            results.append(row)
    strR=results[n][0]
    #print(results[n][0])
    strList=re.findall("[1-9][0-9][0-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9]|[0-9]",strR)
    splist=[]
    for i in strList:
        splist.append(int(i))
    return splist


if __name__ in "__main__":
    print(readOldList(0))
    for i in readOldList(0):
        print(i)