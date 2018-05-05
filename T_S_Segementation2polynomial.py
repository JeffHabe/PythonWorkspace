# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:27:43 2018

@author: Jeff
"""

from os import walk
import os.path as pth 
import numpy as np
import csv 
from scipy.signal import savgol_filter
import pandas as pd 
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import plot
import warnings
cf.go_offline()
mypath ='excelFolder/'
def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return f

def readCSV(fileName):
    data=[]
    time=[]
    f = open(mypath+fileName+'.csv', 'r')
    i=0
    for row in csv.DictReader(f):
        data.append(row['值'])
        time.append(row['時間'])
        i+=1
    f.close()
    return (data,time)
    
def getData():
    for i in range(len(data)):
        t.append(i)
        v.append(float(data[i]))
    global sgf
    sgf=savgol_filter(np.array(v),11,2)
    
    
def mkfile():
    with open('pt.csv','wt',newline='') as csvFile:
        csvHeader=["start","end","polyStartValue","orgStartValue","polyEndValue","orgEndValue","Rsq","f(x)"]
        writer=csv.DictWriter(csvFile,csvHeader)
        writer.writeheader()
        
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
    y_mean_line = [np.mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig,ys_line)
    squared_error_y_mean = squared_error(ys_orig,y_mean_line)
    if(squared_error_y_mean==0):
           print(startPt,'-',endPt)
    R2= 1 - ( squared_error_regr / squared_error_y_mean)
    if(R2>=0):
        return R2
    else:
        return 0
    
#==============least_square==========
def least_square(fuc,ys_orig,m,n,x):
    ys_line=np.polyval(fuc,x)
    err=squared_error(ys_orig,ys_line)
    lsq=err/(m-n-1)
    return lsq
#==============Seg2Poly==========
def Seg2poly(fileName):
    mkfile()
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
    coefA_fun=[]
    coefB_fun=[]
    coefC_fun=[]
    coefD_fun=[]
    R2_PnS=[]
    R2_PnR=[]
    Dlta=[]
    dtMean={}
    sensor=fileName[6:-1]
    diff=0
    limit_time_interval=0
    limit_r2=0
    snrFile=''
    if(sensor=='T'):
        print(fileName)
        snrFile='T\\'
        diff=2 #  反應差
        limit_time_interval= int(len(t)*0.02)
        limit_r2=0.89
        print('最小間隔: ',limit_time_interval)
        print('反應差: ',diff)
        print('最小決定系數: ',limit_r2)
        
        while(startPt<(len(t)-1)):
            
            x=[]
            y=[]
            vt=[]
            Maxr2SGF=0.0
            for i in range(interval,startPt,-1):
            #=================數據反應差==========
                if(abs(sgf[startPt]-sgf[i])<=diff)and (i<=len(t)):
                    endPt=i
                    delta=endPt-startPt
                    islimit=False
                    break
            for j in range(startPt,endPt+1):#for loop 特性,需要到endpt 因此要+1
                    x.append(t[j])
                    y.append(float(sgf[j]))
                    vt.append(float(v[j]))  
    #==========Polyfit 回歸多項式 =========
            tp =np.polyfit(x,y,4)
# =============================================================================
#             with warnings.catch_warnings():
#                 warnings.filterwarnings('error')
#                 try:
#                     tp =np.polyfit(x,y,3)
#                 except np.RankWarning:
#                     print(startPt,'-',endPt)
# =============================================================================
            #f=np.poly1d(tp)
            ys_line=np.polyval(tp,x)
    #=================rsq: 決定係數
            rsqSGF=coeff_of_determination(np.array(y),ys_line,startPt,endPt)
            rsqTT=coeff_of_determination(np.array(vt),ys_line,startPt,endPt)
            if(rsqSGF>Maxr2SGF):
                Maxr2SGF=rsqSGF
                Maxr2TT=rsqTT
                MaxStart=startPt
                MaxEnd=endPt
                Maxtp=tp
    #==================interval:最終距離
            if ((endPt-startPt)<=limit_time_interval) :
                startPt=MaxStart
                endPt=MaxEnd
                tp=Maxtp
                delta=endPt-startPt
                rsqSGF=Maxr2SGF
                rsqTT=Maxr2TT
                islimit=True
            if (rsqSGF>=limit_r2)or islimit :    
    #====tp[0] = A  tp[1] = B tp[2] = C; Ax^2+Bx+C
                #start.append(time[startPt])
                #end.append(time[endPt])

                start.append(startPt)
                end.append(endPt)
                coefA_fun.append(tp[0])
                coefB_fun.append(tp[1])
                coefC_fun.append(tp[2])
                #coefD_fun.append(tp[3])
                Dlta.append(delta)
                R2_PnR.append(round(rsqTT,2))
                R2_PnS.append(round(rsqSGF,2)) 
                interval=endPt+int((len(t)-endPt)/10)
                if(interval>=(len(t)/2)):
                    interval=len(t)-1
                startPt= endPt+1
                    #print("round :",c)
                for k in range(0,len(ys_line)):
                    plyVal_Y.append(ys_line[k])  
            else:
                interval-=5

     
    #===================================================
        dtPolyData={'start':start,
                    'end':end,
                    'A':coefA_fun,
                    'B':coefB_fun,
                    'C':coefC_fun,
                    #'D':coefD_fun,
                    'Delta':Dlta,
                    'R2_Raw':R2_PnR,
                    'R2_SGF':R2_PnS
                    }
        header=['start','end','Delta','R2_Raw','R2_SGF']
        dfpolyDtlData=pd.DataFrame(dtPolyData,columns=header,index=None)
        CsvfileName="Data_csv\\"+snrFile+fileName+"_DetailData.csv"
        dfpolyDtlData.to_csv(CsvfileName)
        print(dfpolyDtlData)
        R2_RnS=round(coeff_of_determination(np.array(v),sgf,startPt,endPt),3)
        MeanR2PnR=round(np.mean(R2_PnR),3)
        MeanR2PnS=round(np.mean(R2_PnS),3)
        print('MeanR2PnR = ' ,MeanR2PnR,', MeanR2PnS = ',MeanR2PnS)
        #print(fileName[:2]+fileName[3:])
        dtMean={
                'date':fileName[:-3],
                'Sensor':fileName[6:],
                'R2_R&S':R2_RnS,
                'Mean_R2_P&R':MeanR2PnR,
                'Mean_R2_P&S':MeanR2PnS
                }
    #    print(df)
    #    df.head()
    
        pltData = [
        go.Scatter(
            x=time, # assign x as the dataframe column 'x'
            y=v,
            name='raw data',
            mode='lines+markers',
            marker=dict(
                    size=5,
                    color='rgba(111,111,111,2)'),
                    line=dict(
                            width=2,
                            color='rgba(111,111,111,2)')
            ),
        go.Scatter(        
            x=time, # assign x as the dataframe column 'x'
            y=sgf,
            name='sgf data',
            mode='line',
            marker=dict(
                    size=10,
                    color='rgba(0,0,0,0)'),
                    line=dict(
                            width=5,
                            color='rgba(152,0,0,8)')
            ),
        go.Scatter(        
            x=time, # assign x as the dataframe column 'x'
            y=plyVal_Y,
            name='Poly data',
            mode='line',
            marker=dict(
                    size=10,
                    color='rgba(0,0,0,0)'),
                    line=dict(
                            width=2,
                            color='rgba(0,255,255,8)')
                    )]
        layout={'title':fileName+' Plot',
                              'font': dict(size=16)}
        #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
        plot(pltData,layout,filename=".\Plot_html\\"+fileName+".html")


    return dtMean
fileName=getFileName(mypath)
ltMean=[]
header=["date","Sensor","R2_R&S","Mean_R2_P&R","Mean_R2_P&S"]
#for i  in range(len(fileName)):
# =============================================================================
# for i  in range(4):
#     data,time=readCSV(fileName[i])
#     t=[]
#     v=[]
#     sgf=[]
#     stop=False        
#     getData()
#     ltMean.append(Seg2poly(fileName[i]))
#     
# =============================================================================
data,time=readCSV(fileName[9])
t=[]
v=[]
sgf=[]
stop=False        
getData()
ltMean.append(Seg2poly(fileName[9]))    
#print(ltMean)
dfpolyMeanData=pd.DataFrame(ltMean,columns=header)
#print(dfpolyMeanData)
CsvfileName='Data_csv\\Mean\\2018_Mean_R2Data.csv'
if (pth.isfile(CsvfileName)!=True):  
   dfpolyMeanData.to_csv(CsvfileName,mode='w',index=None)
else:
    dfpolyMeanData.to_csv(CsvfileName,mode='a',header=None,index=None)