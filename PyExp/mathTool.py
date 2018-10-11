# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:02:14 2018

@author: Jeff PC
"""

import numpy as np
from numpy.polynomial import chebyshev as chy


def rsq(x,y,pfit):
    if (len(y)==len(pfit)):
          Sresid =(y - pfit)
    else:
        Sresid =(y - np.polyval(pfit,x))
    SSresid= sum(pow(Sresid,2))
    SStotal=len(y)*np.var(y)
    rsq=1-SSresid/SStotal
    return rsq


#==============squared_error==========
def squared_error(ys_orig,ys_line):
    return sum((ys_line-ys_orig)**2)
#==============coeff_of_determination==========
def coeff_of_determination(ys_orig, ys_line,startPt=0,endPt=0):
    y_mean=np.mean(ys_orig)
    y_mean_line = [y_mean for y in ys_orig]## 生成一個值為y_mean,長度為ys_orig的陣列
    squared_error_regr = round(squared_error(ys_orig,ys_line),4)
    squared_error_y_mean = round(squared_error(ys_orig,y_mean_line),4)
    if(squared_error_y_mean==0):
        #print(startPt,'-',endPt)
        return 1
    else:    
        R2= 1 - ( squared_error_regr / squared_error_y_mean)
        return R2
    
#==============least_square==========
def least_square(fuc,ys_orig,m,n,x):
    ys_line=np.polyval(fuc,x)
    err=squared_error(ys_orig,ys_line)
    lsq=err/(m-n-1)
    return lsq

#=========== poly s ========    
def polyLine(startPt,endPt,polyIndex,t,sgf,data):
    x=[]
    y=[]
    vt=[]
    for j in range(startPt,endPt):#for loop 特性,需要到endpt 因此要+1
        x.append(t[j])
        y.append(float(sgf[j]))
        vt.append(float(data[j]))  
    #=================Polyfit 回歸多項式 =========
    # =============================================================================
    #                     tp=np.polyfit(x,y,polyIndex)
    #                     ys_line=np.polyval(tp,x)
    # =============================================================================
    #=================chebyshev 回歸多項式 =========
    coeffRaw=chy.chebfit(x,vt,polyIndex)
    coeffSGF=chy.chebfit(x,y,polyIndex)
    #print(np.poly1d(coeffRaw))
    ys_lineRaw=chy.chebval(x,coeffRaw)                    
    ys_lineSGF=chy.chebval(x,coeffSGF)                    
    #=================rsq: 決定係數=========
    rsqSGF=round(coeff_of_determination(np.array(y),ys_lineRaw,startPt,endPt),2)
    rsqTT=round(coeff_of_determination(np.array(vt),ys_lineRaw,startPt,endPt),2)
    return coeffRaw,ys_lineRaw,rsqSGF,rsqTT

# =============================================================================
# if __name__ == "__main__":
# # =============================================================================
# #      y_mean_line = [2 for y in [1,2,3,4,5,0]]
# #      print(y_mean_line)
# # =============================================================================
# 
# =============================================================================
