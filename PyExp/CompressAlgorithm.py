# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 17:13:47 2018

@author: Jeff PC
"""


import numpy as np
from scipy.signal import savgol_filter
import cufflinks as cf
import plotly.graph_objs as go
import folderTool as fT
import plotTool as pltT
import mathTool as mthT
import time


mypath ='excelFolder/'
cf.go_offline()
t=[]
v=[]
times=[]
data=[]

def getRnSData(SGwd_length,SGpolyOrd):
    for i in range(len(data)):
        t.append(i)
        v.append(float(data[i]))
    sgf=savgol_filter(data,SGwd_length,SGpolyOrd)
    R2_RnS=round(mthT.coeff_of_determination(np.array(data),sgf),3)
    global pltData
    #print(times)
    pltData += [
        go.Scatter(
            x=times, # assign x as the dataframe column 'x'
            y=v,
            name='Raw',
            mode='lines',
            marker=dict(
                    size=10,
                    color='rgba(170,170,0,1)'),
                    line=dict(width=10,)
                    ),
        go.Scatter(        
            x=times, # assign x as the dataframe column 'x'
            y=sgf,
            name='S-Gf: R2:'+str(R2_RnS),
            mode='line',
            marker=dict(
                    size=5,
                    color='rgba(0,0,0,0.8)'),
                    line=dict(
                            width=3,
                            color='rgba(0,0,0,0.8)')
           )]
    return sgf

def Seg2poly(fileName,sgf,
             SGwd_length=11,
             SGpolyOrd=5,
             min_r2=0.99,
             polyIndex=5,
             window_size_percent=0.05,
             min_interval_percent=0.0,
             isplot=False):
    startPt=0
    endPt=0
    delta=0
    timer=0
    '''
    plot(t,v,'-')
    plot(t,sgf,'-')
    '''
    tStart = time.time()#計時開始
    #plt.plot(t,v,'-')
    #plt.plot(t,sgf,'-')
    if(len(t)>100):
        pass
    else:
        window_size_percent=1
    print('wdSize:',window_size_percent)
    interval=int(len(t)*window_size_percent)-1
    start=[]
    end=[]
    #intervalAry=[]
    coef_ary=[]
    
    decompData=[]
    #first_inl=0
    R2_PnS=[]
    R2_PnR=[]
    Dlta=[]
    sensor=fileName[6:-1]
    Maxr2SGF=0.0
    MaxEnd=0
    MaxCoeff=[]
    MaxYs=[]
    rsqSGF=0
    rsqTT=0
    ys_line=[]
    dirSnr=''
    DeltaCnt=0
    if(sensor=='T'):
        print(fileName)
        dirSnr=sensor+'\\'
    elif(sensor=='H'):
        print(fileName)
        dirSnr=sensor+'\\'
    #dirFoder='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr+'\\Poly_Index '+str(pIndex)+'\\max angle '+str(angle) #'\\Poly_Index '+str(pIndex)+'\\SGwd_length '+str(SGwd_length)
    #dirFoder='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr
    dirFoder='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr
    fT.mkfolder(dirFoder)
    dirWCdetailFolder='Data_csv\\SlidingWindow\\Chebyshev\\Worst compressing data\\'
    fT.mkfolder(dirWCdetailFolder)
    #===condition====
    #max_slope=2 #  反應差
    min_time_interval= int(len(t)*min_interval_percent)
    c=1

    while(startPt<(len(t))):
        #MaxStart=0
        
        islimit=False
# =============================================================================
#             
#             if ((interval-startPt)<=min_time_interval) :
#                 interval=interval+int((len(t)/10))
#     
# =============================================================================
        for i in range(interval,startPt-1,-1):
             
            if ((i-startPt)>min_time_interval):
                endPt=i+1
                delta=endPt-startPt
                coeff,ys_line,rsqSGF,rsqTT = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                if(rsqSGF>=Maxr2SGF):
                     Maxr2SGF=rsqSGF
                     MaxYs=ys_line
                     #MaxStart=startPt
                     MaxEnd=endPt
                     MaxCoeff=coeff
                break
            elif((i-startPt)<=min_time_interval+1):
                if(Maxr2SGF==0):
                    endPt=len(t)
                    delta=endPt-startPt
                    coeff,ys_line,rsqSGF,rsqTT = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                    islimit=True
                else:
                    endPt=MaxEnd
                    coeff=MaxCoeff
                    delta=endPt-startPt
                    rsqSGF=Maxr2SGF
                    ys_line=MaxYs
                    delta=endPt-startPt
                    islimit=True
                break
        if (rsqSGF>=min_r2) or islimit :    
#====coeff[0] = A  coeff[1] = B coeff[2] = C; Ax^2+Bx+C
            #start.append(time[startPt])
            #end.append(time[endPt])
# =============================================================================
#             if(rsqTT<min_r2):
#                 print(c)
#                 print(Maxr2SGF)
#                 print(islimit)
#                 print(i)
#                 print(startPt)
# =============================================================================
            start.append(times[startPt])
            if(endPt!=len(times)):    
                end.append(times[endPt])
                #print(len(times),':',endPt)
            else:
                end.append(times[endPt-1])
                #print(len(times),':',endPt)
            #coef_ary.append(coeff)
            #print(np.poly1d(coeff))
            coef_ary.extend(coeff)
            decompData.extend(ys_line)
            print()
            Dlta.append(delta)
                
            DeltaCnt =DeltaCnt+endPt-startPt
           # print(len(decompData),'Delta=',DeltaCnt)
            global pltData
            pltData += [
                go.Scatter(
                    x=times[startPt:endPt], # assign x as the dataframe column 'x'
                    y=ys_line,
                    mode='lines',
                    name=str(c)+':S: '+ str(rsqSGF)+',R: '+str(rsqTT),
                    marker=dict(
                            size=5,
                            color='rgba(255,0,0,0.9)'
                            )
                    )]
            c+=1
            #print(startPt,"-",endPt)
            R2_PnR.append(round(rsqTT,3))
            R2_PnS.append(round(rsqSGF,3))
            startPt= endPt
            interval=startPt+int((len(t)*window_size_percent))-1
            
# =============================================================================
            if (interval>=len(t)):
                interval=len(t)-1
                
            #intervalAry.append(interval)
            MaxCoeff=[]
            MaxYs=[]
            Maxr2SGF=0.0
            MaxEnd=interval
        else:
            interval-=1
            
    tEnd = time.time()#計時結束
    timer=tEnd-tStart
    print('Compressing Time:',timer)
    pltT.PlotLy(t,window_size_percent,min_interval_percent,polyIndex,fileName,pltData,isplot)
    return coef_ary,decompData