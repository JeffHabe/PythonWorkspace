# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:27:43 2018

@author: Jeff
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
    #print(data)
     
def getRnSData(SGwd_length,SGpolyOrd):
    for i in range(len(data)):
        t.append(i)
        v.append(float(data[i]))
    sgf=savgol_filter(data,SGwd_length,SGpolyOrd)
    global pltData
    #print(times)
    pltData += [
        go.Scatter(
            x=times, # assign x as the dataframe column 'x'
            y=v,
            name='raw data',
            mode='lines+markers',
            marker=dict(
                    size=2,
                    color='rgba(0,0,255,0.5)'),
                    ),
        go.Scatter(        
            x=times, # assign x as the dataframe column 'x'
            y=sgf,
            name='sgf data',
            mode='line',
            marker=dict(
                    size=10,
                    color='rgba(0,0,0,0)'),
                    line=dict(
                            width=5,
                            color='rgba(0,255,0,0.5)')
           )]
    return sgf
    
    
def mkfolder(directory):
    if not pth.exists(directory):
        makedirs(directory)
        
        
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
def coeff_of_determination(ys_orig, ys_line,startPt,endPt):
    y_mean=np.mean(ys_orig)
    y_mean_line = [y_mean for y in ys_orig]
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
#==============PlotLy============
    
def PlotLy(min_interval_percent,SGpolyOrd,polyIndex,SGwd_length,fileName,pltData):
    
    layout={'title':fileName+' Plot',
                          'font': dict(size=16)}
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\min_interval_percent '+str((round(min_interval_percent,2)))+'\\' 
    mkfolder(filePath)
    plot(pltData,layout,filename=filePath+fileName+".html")
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

    coeff=chy.chebfit(x,y,polyIndex)
# =============================================================================
#     print(chy.Chebyshev.fit(x,y,polyIndex))
#     print(coeff)
#     print(np.poly1d(coeff))
# =============================================================================
    ys_line=chy.chebval(x,coeff)                    
    #=================rsq: 決定係數=========
    rsqSGF=round(coeff_of_determination(np.array(y),ys_line,startPt,endPt),3)
    rsqTT=round(coeff_of_determination(np.array(vt),ys_line,startPt,endPt),3)
    return coeff,ys_line,rsqSGF,rsqTT
#==============Seg2Poly==========
def Seg2poly(fileName,SGwd_length=11,SGpolyOrd=3,max_slope=1,min_r2=0.95,polyIndex=1,window_size_percent=0.5,min_interval_percent=0,isplot=False):
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
    angle=int(round((np.arctan(max_slope)*180)/pi))
    interval=int(len(t)*window_size_percent)-1
    start=[]
    end=[]
    #intervalAry=[]
    coef_ary=[]
    #first_inl=0
    R2_PnS=[]
    R2_PnR=[]
    Dlta=[]
    dtMean={}
    sensor=fileName[6:-1]
    Maxr2SGF=0.0
    MaxEnd=0
    MaxCoeff=[]
    MaxYs=[]
    rsqSGF=0
    rsqTT=0
    ys_line=[]
    tot_segNum=0
    dirSnr=''
    if(sensor=='T'):
        print(fileName)
        dirSnr=sensor+'\\'
    elif(sensor=='H'):
        print(fileName)
        dirSnr=sensor+'\\'
    #dirFoder='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr+'\\Poly_Index '+str(pIndex)+'\\max angle '+str(angle) #'\\Poly_Index '+str(pIndex)+'\\SGwd_length '+str(SGwd_length)
    dirFoder='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr+'min_interval_percent '+str(round(min_interval_percent,2))
    mkfolder(dirFoder)
    #===condition====
    #max_slope=2 #  反應差
    min_time_interval= int(len(t)*min_interval_percent)
    c=1
    segNum=0

    while(startPt<(len(t)-1)):
        #MaxStart=0
        islimit=False
# =============================================================================
#             
#             if ((interval-startPt)<=min_time_interval) :
#                 interval=interval+int((len(t)/10))
#     
# =============================================================================
        for i in range(interval,startPt-1,-1):
            #print(i)
        #=================數據斜率==========
            y=abs(int((sgf[i]-sgf[startPt])))
            x=abs(int((i-startPt)))
            if(x!=0):
                slope=abs(float(y/x))
            else:
                slope=np.tan(pi/2)
            #print(slope)
# =============================================================================
#             if(minDiff>=diff):
#                 minDiff=diff
#                 #minD_i=i
# =============================================================================
            if(slope<=max_slope) and ((i-startPt)>min_time_interval):
                endPt=i+1
                delta=endPt-startPt
                coeff,ys_line,rsqSGF,rsqTT = polyLine(startPt,endPt,polyIndex,t,sgf,data)
                if(rsqSGF>=Maxr2SGF):
                     Maxr2SGF=rsqSGF
                     MaxYs=ys_line
                     #MaxStart=startPt
                     MaxEnd=endPt
                     MaxCoeff=coeff
                break
            elif((i-startPt)<=min_time_interval):
                #print('interval:',interval,' start:',startPt,' minDi',minD_i,":",i,'minDiff:',minDiff,'diff=',diff)
                #print('start:',startPt,'-',endPt,":delta",delta," 1st interval = ",first_inl)
                #startPt=MaxStart
                if ((len(t)-startPt)<=min_time_interval):
                    endPt=len(t)-1
                    delta=endPt-startPt
                    coeff,ys_line,rsqSGF,rsqTT = polyLine(startPt,endPt,polyIndex,t,sgf,data)
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
            start.append(startPt)
            end.append(endPt)
            coef_ary.append(coeff)
            Dlta.append(delta)
            global pltData
            pltData += [
                go.Scatter(
                    x=times[startPt:endPt], # assign x as the dataframe column 'x'
                    y=ys_line,
                    mode='lines',
                    name=str(c)+': '+ str(rsqSGF),
                    marker=dict(
                            size=10,
                            color='rgba(255,0,0,0.9)'
                            )
                    )]
            c+=1
            R2_PnR.append(round(rsqTT,3))
            R2_PnS.append(round(rsqSGF,3))
            startPt= endPt
            interval=startPt+int((len(t)*window_size_percent))

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

#===================================================
    dtPolyData={'start':start,
                'end':end,
                'coef':coef_ary,
                'Delta':Dlta,
                'R2_Raw':R2_PnR,
                'R2_SGF':R2_PnS
                }
    tEnd = time.time()#計時結束
    header=['start','end','Delta','R2_Raw','R2_SGF','coef']
    dfpolyDtlData=pd.DataFrame(dtPolyData,columns=header,index=None)
    SnrCsvfileName=dirFoder+'\\'+fileName+"_DetailData.csv"
    dfpolyDtlData.to_csv(SnrCsvfileName,mode='w')
    segNum=len(start)# num of segement 
    tot_segNum+=segNum# total number of segements in all data 
    comp_ratio=abs(len(t)-segNum)/len(t)
    #print(dfpolyDtlData)
    R2_RnS=round(coeff_of_determination(np.array(data),sgf,startPt,endPt),3)
    MeanR2PnR=round(np.mean(R2_PnR),3)
    MeanR2PnS=round(np.mean(R2_PnS),3)
    STD=round(np.std(R2_PnS),3)
    timer=tEnd-tStart
    #print('MeanR2PnR = ' ,MeanR2PnR,', MeanR2PnS = ',MeanR2PnS)
    #print(fileName[:2]+fileName[3:])
    dtMean={
            'date':fileName[:-3],
            'Sensor':fileName[6:],
            'Minium interval':min_time_interval,
            'segNum':segNum,
            'comp_ratio':comp_ratio,
            'R2_R&S':R2_RnS,
            'timer': timer,
            'Mean_R2_P&R':MeanR2PnR,
            'Mean_R2_P&S':MeanR2PnS,
            'STD':STD
            }
#    print(df)
#    df.head()
    #print(pltData)
    
    if isplot:
        PlotLy(min_interval_percent,SGpolyOrd,polyIndex,SGwd_length,fileName,pltData)
    return dtMean

fileName=getFileName(mypath)

#print(fileName)
#===condition====
SGwd_length=11# window length must odd ,SGwd_length >2N+1
Ord=5
pIndex=4
angle=0
#  反應差  1 2 3 4 5  10 20 30
wdsize_percent=0.5 #
min_interval_percent=0.00#
min_r2=0.9 #固定
#rndFile=88#random.randint(0,len(fileName))
count=0
while(wdsize_percent>=0.1):
    count+=1
    max_slope=np.tan(angle*(pi/180))
    w=SGwd_length
    print('Started')
    print('pIndex: ',pIndex,' wd Length: ',w,' Angle: ',str(round(angle,2)))
# =============================================================================
#     dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\SGpolyOrd '\
#     +str(Ord)+'\\PolyIndex '+str(pIndex)+'\\SGwd_length '+str(w)\
#     +'\\max angle '+str(angle)
# =============================================================================
    dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\min_interval_percent '\
    +str(round(min_interval_percent,2))
    mkfolder(dirMean)
    #print('wd Length: ',SGwd_length,'SGpolyOrd: ',SGpolyOrd)
    Meanheader=["date","Sensor",'Minium interval',"segNum","R2_R&S","comp_ratio","Mean_R2_P&R","Mean_R2_P&S",'timer','STD']
    #for i  in range(len(fileName)):
    count_T=0
    ltMean=[]
    
    for i  in range(0,len(fileName)):#len(fileName)
        #i=rndFile
        sensorType=fileName[i][6:-1]  
        #print(sensorType)
# =============================================================================
#             if(sensorType=='T'):
# =============================================================================
            #print(fileName[i])
        data,times=readCSV(fileName[i])
        t=[]
        v=[]
        sgf=[]
        pltData=[]
        tot_segNum=0
        count_T+=1
        stop=False        
        sgf=getRnSData(w,Ord)
        ltMean.append(Seg2poly(fileName[i],
                               SGwd_length=w,
                               SGpolyOrd=Ord,
                               max_slope=max_slope,
                               min_r2=min_r2,
                               polyIndex=pIndex,
                               window_size_percent=wdsize_percent,
                               min_interval_percent=min_interval_percent,
                               isplot=False))
    dfpolyMeanDay=pd.DataFrame(ltMean,columns=Meanheader)
    
    MeanCsvfileName=dirMean+'\\2018_Mean_R2Data.csv'
    dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
# =============================================================================
#         if (pth.isfile(MeanCsvfileName)!=True):  
#            dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
#         else:
#             dfpolyMeanDay.to_csv(MeanCsvfileName,mode='a',header=None,index=None)
# =============================================================================
    #print(dfpolyMeanDay)
# =============================================================================
#     print('sgf window length: ',SGwd_length)
#     print('sgf SGpolyOrder: ',SGpolyOrd)
#     print('反應差: ',max_slope)
#     print('最小決定系數: ',min_r2)
#     print('擬合n次多項式 n : ',polyIndex)
#    
#     print('All R2 R&S mean :',round(np.mean(dfpolyMeanDay['R2_R&S']),3),
#           'All R2 P&S mean :',round(np.mean( dfpolyMeanDay['Mean_R2_P&S']),3))
#     
# =============================================================================
    mean_segTol=round(np.mean(dfpolyMeanDay['segNum']),3)
    T_r2=[]
    H_r2=[]
    for i in range(0,len(dfpolyMeanDay)):
        checkChar=dfpolyMeanDay['Sensor'][i][0]
        if (checkChar=='T'):
            #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
            T_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
        if (checkChar=='H'):
            #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
            H_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
            
    #idx=dfpolyMeanDay.index[dfpolyMeanDay['Sensor']=='T'].tolist()
    T_meanindf=dfpolyMeanDay['Mean_R2_P&S'].values
    #H_meanindf=dfpolyMeanDay.loc['Mean_R2_P&S',[dfpolyMeanDay['Sensor']=='T'].tolist
    mean_compRatio=round(np.mean(dfpolyMeanDay['comp_ratio']),3)
    allR2rns=round(np.mean(dfpolyMeanDay['R2_R&S']),3)
    allR2pns=round(np.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
    Tr2pns=round(np.mean(T_r2),3)
    Hr2pns=round(np.mean(H_r2),3)
    STDall=round(np.std(dfpolyMeanDay['Mean_R2_P&S']),3)
    TimerMean=round(np.mean(dfpolyMeanDay['timer']),3)
    #print('T ',Tr2pns,' H ',Hr2pns)
    tolMean={'sgf window length':[w],
             'sgf SGpolyOrder':[Ord],
             'Angle':[angle],
             'Poly n':[pIndex],
             'wd_size_%':wdsize_percent,
             'min_interval_%':min_interval_percent,
             'mean_segTol':[mean_segTol],
             'mean_compRatio':[mean_compRatio],
             'All R2 R&S mean':[allR2rns],
             'All R2 P&S mean':[allR2pns],
             'T R2 P&S mean':Tr2pns,
             'H R2 P&S mean':Hr2pns,
             'STD_All':STDall,
             'TimerMean':TimerMean
             }
    tolMheader=['sgf window length',
                'sgf SGpolyOrder',
                'Angle',
                'Poly n',
                'wd_size_%',
                'min_interval_%',
                'mean_segTol',
                'mean_compRatio',
                'All R2 R&S mean',
                'All R2 P&S mean',
                'T R2 P&S mean',
                'H R2 P&S mean',
                'STD_All',
                'TimerMean']
    
    tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllMean.csv'
    dftolMean=pd.DataFrame(tolMean,columns=tolMheader)
    #print(dftolMean)
    #print(tolMeanFile)
    if (pth.isfile(tolMeanFile)!=True):  
        dftolMean.to_csv(tolMeanFile,mode='w',index=None)
    else:
        dftolMean.to_csv(tolMeanFile,mode='a',header=None,index=None)
    dftolMean=pd.DataFrame(None,None)
    #dftolMean.to_csv(tolMeanFile,mode='a',line_terminator="\n")
    print('All is done in '+str(round(angle,2)))
    if(angle==90):
        angle=0
        wdsize_percent-=0.05
        dftolMean.to_csv(tolMeanFile,mode='a',line_terminator="\n")
    else:
        angle+=15
# =============================================================================
#     if(count==1):
#         wdsize_percent=0.25
#         wdsize_percent=round(wdsize_percent,2)
#     elif(count==2):
#         wdsize_percent=0.5
#         wdsize_percent=round(wdsize_percent,2)
# =============================================================================
    # =============================================================================
    # data,time=readCSV(fileName[9])
    # t=[]
    # v=[]
    # sgf=[]
    # stop=False        
    # sgf=getRnSData(SGwd_length,SGpolyOrd)
    # ltMean.append(Seg2poly(fileName[9],max_slope,min_r2,polyIndex,min_interval_percent))    
    # 
    # =============================================================================
    #print(ltMean)
