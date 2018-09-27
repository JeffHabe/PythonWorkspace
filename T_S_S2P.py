# -*- coding: utf-8 -*-
"""
Created on Sun May  6 00:24:31 2018

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:27:43 2018

@author: Jeff
"""

from os import walk,makedirs
import os.path as pth 
import numpy as np
import csv 
from scipy.signal import savgol_filter
import pandas as pd 
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import plot
import datetime
import warnings
from numpy.polynomial import chebyshev as chy
cf.go_offline()
mypath ='excelFolder/'

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
     
def getRnSData(wd_length,polyOrd):
    for i in range(len(data)):
        t.append(i)
        v.append(float(data[i]))
    sgf=savgol_filter(data,wd_length,polyOrd)
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
    
def PlotLy(polyOrd,polyIndex,wd_length,fileName,pltData):
    
    layout={'title':fileName+' Plot',
                          'font': dict(size=16)}
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    filePath=".\Plot_html\\SlidingWindow\\"+'wdL'+str(wd_length)+'\\'+'polyOrd'+str(polyOrd)+'\\Index'+str(polyIndex)+'\\'
    mkfolder(filePath)
    plot(pltData,layout,filename=filePath+fileName+".html")
    
#==============Seg2Poly==========
def Seg2poly(fileName,wd_length,polyOrd,limit_diff,limit_r2,polyIndex,limit_interval_percent,isplot=False):
    startPt=0
    endPt=0
    delta=0
    '''
    plot(t,v,'-')
    plot(t,sgf,'-')
    '''
    #plt.plot(t,v,'-')
    #plt.plot(t,sgf,'-')

    interval=int(len(t)/4)
    plyVal_Y=[]
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
    MaxYs=[]
    rsqSGF=0
    rsqTT=0
    ys_line=[]
    tp=np.array([])
    dirSnr=''
    if(sensor=='T'):
        print(fileName)
        dirSnr=sensor+'\\'
        dirT='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr+'PolyOrd\\'+str(polyOrd)+'\\PolyIndex\\'+str(polyIndex)+'\\WD_Length\\'+str(wd_length) 
        mkfolder(dirT)
        #===condition====
        #diff=2 #  反應差
        limit_time_interval= int(len(t)*limit_interval_percent)
# =============================================================================
#         if(limit_time_interval<=20):
#             limit_time_interval=5
# =============================================================================
        #limit_r2=0.95
        #polyCoeff=2
        #print(limit_time_interval)
        c=1
        tot_segNum=0
        while(startPt<=(len(t)-1)):
            x=[]
            y=[]
            vt=[]
            minDiff=100
            minD_i=0
            islimit=False
# =============================================================================
#             
#             if ((interval-startPt)<=limit_time_interval) :
#                 interval=interval+int((len(t)/10))
#     
# =============================================================================
            for i in range(interval,startPt-1,-1):

            #=================數據反應差==========
                diff=int(abs(sgf[startPt]-sgf[i]))
                if(minDiff>=diff):
                    minDiff=diff
                    minD_i=i
                if(diff<=limit_diff) and ((i-startPt)>=limit_time_interval):
                    endPt=i
                    delta=endPt-startPt
                    for j in range(startPt,endPt+1):#for loop 特性,需要到endpt 因此要+1
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
                    #print(chy.(coeff))
                    ys_line=chy.chebval(x,coeff)                    
#=================rsq: 決定係數=========
                    rsqSGF=round(coeff_of_determination(np.array(y),ys_line,startPt,endPt),3)
                    rsqTT=round(coeff_of_determination(np.array(vt),ys_line,startPt,endPt),3)
                    
                    break
                elif((i-startPt)<limit_time_interval):
                    endPt=minD_i
                    #print('interval:',interval,' start:',startPt,' minDi',minD_i,":",i,'minDiff:',minDiff,'diff=',diff)
                    delta=endPt-startPt
                    islimit=True
                    for j in range(startPt,endPt+1):#for loop 特性,需要到endpt 因此要+1
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
                    ys_line=chy.chebval(x,coeff)
#=================rsq: 決定係數=========
                    rsqSGF=round(coeff_of_determination(np.array(y),ys_line,startPt,endPt),3)
                    rsqTT=round(coeff_of_determination(np.array(vt),ys_line,startPt,endPt),3)
                    break

#==========Polyfit 回歸多項式 =========
# =============================================================================
#             with warnings.catch_warnings():
#                 warnings.filterwarnings('error')
#                 try:
#                     tp =np.polyfit(x,y,polyIndex)
#                 except np.RankWarning:
#                     print(startPt,'-',endPt)
# =============================================================================
            #f=np.poly1d(tp)
           

# =============================================================================
#             if(rsqSGF>=Maxr2SGF):
#                 Maxr2SGF=rsqSGF
#                 Maxr2TT=rsqTT
#                 MaxYs=ys_line
#                 #MaxStart=startPt
#                 MaxEnd=endPt
#                 Maxtp=tp
#     #==================interval:最終距離
#             if (delta<=limit_time_interval) :
#                 #print('start:',startPt,'-',endPt,":delta",delta," 1st interval = ",first_inl)
#                 #startPt=MaxStart
#                 endPt=MaxEnd
#                 tp=Maxtp
#                 delta=endPt-startPt
#                 rsqSGF=Maxr2SGF
#                 rsqTT=Maxr2TT
#                 ys_line=MaxYs
#                 islimit=True
# =============================================================================
            if (rsqSGF>=limit_r2)or islimit :    
    #====coeff[0] = A  coeff[1] = B coeff[2] = C; Ax^2+Bx+C
                #start.append(time[startPt])
                #end.append(time[endPt])
                start.append(startPt)
                end.append(endPt)
                coef_ary.append(coeff)
                Dlta.append(delta)
# =============================================================================
#                 print(startPt,':',endPt)
#                 print(delta)
#                 print(len(ys_line))
# =============================================================================
                global pltData
                pltData += [
                    go.Scatter(
                        x=times[startPt:endPt], # assign x as the dataframe column 'x'
                        y=ys_line,
                        name=str(c)+':'+ str(rsqSGF),
                        marker=dict(
                                size=10
                                )
                        )]
                c+=1
                R2_PnR.append(round(rsqTT,3))
                R2_PnS.append(round(rsqSGF,3))
                startPt= endPt+1
                interval=startPt+int((len(t)/20))
                if((interval-startPt)<limit_time_interval):
                    interval=interval+int(len(t)/5)
                if (interval>=len(t)):
                    interval=(len(t)-1)
                #intervalAry.append(interval)
                
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
        dirT='Data_csv\\SlidingWindow\\Chebyshev\\'+dirSnr+'PolyOrd\\'\
        +str(polyOrd)+'\\PolyIndex\\'+str(polyIndex)+'\\WD_Length\\'+str(wd_length) 
        mkfolder(dirT)
        header=['start','end','Delta','R2_Raw','R2_SGF','coef']
        dfpolyDtlData=pd.DataFrame(dtPolyData,columns=header,index=None)
        SnrCsvfileName=dirT+'\\'+fileName+"_DetailData.csv"
        dfpolyDtlData.to_csv(SnrCsvfileName,mode='w')
        tot_segNum+=len(R2_PnS)
        comp_ratio=(tot_segNum/len(t))*100
        #print(dfpolyDtlData)
        R2_RnS=round(coeff_of_determination(np.array(data),sgf,startPt,endPt),3)
        MeanR2PnR=round(np.mean(R2_PnR),3)
        MeanR2PnS=round(np.mean(R2_PnS),3)
        #print('MeanR2PnR = ' ,MeanR2PnR,', MeanR2PnS = ',MeanR2PnS)
        #print(fileName[:2]+fileName[3:])
        dtMean={
                'date':fileName[:-3],
                'Sensor':fileName[6:],
                'limit interval':limit_time_interval,
                'tot_segNum':tot_segNum,
                'comp_ratio':comp_ratio,
                'R2_R&S':R2_RnS,
                'Mean_R2_P&R':MeanR2PnR,
                'Mean_R2_P&S':MeanR2PnS
                }
    #    print(df)
    #    df.head()
        #print(pltData)
        if isplot:
            PlotLy(polyOrd,polyIndex,wd_length,fileName,pltData)
    return dtMean

fileName=getFileName(mypath)

#print(fileName)
#===condition====
wd_length=21# window length must odd ,wd_length >2N+1
Ord=3
pIndex=3
diff=10 #  反應差
limit_interval_percent= 0.02
limit_r2=0.95


 
#wd_length
for w in range(wd_length,23,2):
    dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\PolyOrd\\'\
    +str(Ord)+'\\PolyIndex\\'+str(pIndex)+'\\WD_Length\\'+str(w)
    mkfolder(dirMean)
    #print('wd Length: ',wd_length,'polyOrd: ',polyOrd)
    Meanheader=["date","Sensor","tot_segNum","R2_R&S","comp_ratio","Mean_R2_P&R","Mean_R2_P&S"]
    #for i  in range(len(fileName)):
    count_T=0
    ltMean=[]
    for i  in range(0,3):#len(fileName)
        sensorType=fileName[i][6:-1]  
        #print(sensorType)
        if(sensorType=='T'):
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
                                   wd_length=w,
                                   polyOrd=Ord,
                                   limit_diff=diff,
                                   limit_r2=limit_r2,
                                   polyIndex=pIndex,
                                   limit_interval_percent=limit_interval_percent,
                                   isplot=True))
    dfpolyMeanDay=pd.DataFrame(ltMean,columns=Meanheader)
    print('wd Length: ',w,'polyOrd: ',Ord)
    MeanCsvfileName=dirMean+'\\2018_Mean_R2Data.csv'
    if(sensorType=='T'):
        dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
# =============================================================================
#         if (pth.isfile(MeanCsvfileName)!=True):  
#            dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
#         else:
#             dfpolyMeanDay.to_csv(MeanCsvfileName,mode='a',header=None,index=None)
# =============================================================================
    #print(dfpolyMeanDay)
# =============================================================================
#     print('sgf window length: ',wd_length)
#     print('sgf polyOrder: ',polyOrd)
#     print('反應差: ',diff)
#     print('最小決定系數: ',limit_r2)
#     print('擬合n次多項式 n : ',polyIndex)
#    
#     print('All R2 R&S mean :',round(np.mean(dfpolyMeanDay['R2_R&S']),3),
#           'All R2 P&S mean :',round(np.mean( dfpolyMeanDay['Mean_R2_P&S']),3))
#     
# =============================================================================
    mean_segTol=round(np.mean(dfpolyMeanDay['tot_segNum']),3)
    allR2rns=round(np.mean(dfpolyMeanDay['R2_R&S']),3)
    allR2pns=round(np.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
    tolMean={'sgf window length':[w],
             'sgf polyOrder':[Ord],
             'different':[diff],
             'Poly n':[pIndex],
             'mean_segTol':[mean_segTol],
             'limit R2':[limit_r2],
             'All R2 R&S mean':[allR2rns],
             'All R2 P&S mean':[allR2pns]
             }
    tolMheader=['sgf window length',
                'sgf polyOrder',
                'different',
                'Poly n',
                'mean_segTol',
                'limit R2',
                'All R2 R&S mean',
                'All R2 P&S mean']
    
    tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\SWAllMean.csv'
    dftolMean=pd.DataFrame(tolMean,columns=tolMheader)
    #print(dftolMean)
    #print(tolMeanFile)
    if (pth.isfile(tolMeanFile)!=True):  
        dftolMean.to_csv(tolMeanFile,mode='w',index=None)
    else:
        dftolMean.to_csv(tolMeanFile,mode='a',header=None,index=None)
    print()
    dftolMean=pd.DataFrame(columns=tolMheader)
    dftolMean.to_csv(tolMeanFile,mode='a',header=None,index=None)



# =============================================================================
# data,time=readCSV(fileName[9])
# t=[]
# v=[]
# sgf=[]
# stop=False        
# sgf=getRnSData(wd_length,polyOrd)
# ltMean.append(Seg2poly(fileName[9],diff,limit_r2,polyIndex,limit_interval_percent))    
# 
# =============================================================================
#print(ltMean)
