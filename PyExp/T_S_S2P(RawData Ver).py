# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:27:43 2018

@author: Jeff
"""

import os.path as pth 
import numpy as np
from math import pi
from scipy.signal import savgol_filter
import pandas as pd 
import cufflinks as cf
import plotly.graph_objs as go
import folderTool as fT
import randomSampling as rSp
import plotTool as pltT
import mathTool as mthT
import time
import datetime as dt


mypath ='excelFolder/'
cf.go_offline()

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
# =============================================================================
#     if(len(t)>100):
#         pass
#     else:
#         window_size_percent=1
# =============================================================================
    interval=int(len(t)*window_size_percent)-1
    start=[]
    end=[]
    #intervalAry=[]
    coef_ary=[]
    coeff_5=[]
    coeff_4=[]
    coeff_3=[]
    coeff_2=[]
    coeff_1=[]
    coeff_0=[]
    
    decompData=[]
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
    segNum=0

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
            coeff_5.append(coeff[0])
            coeff_4.append(coeff[1])
            coeff_3.append(coeff[2])
            coeff_2.append(coeff[3])
            coeff_1.append(coeff[4])
            coeff_0.append(coeff[5])
            Dlta.append(delta)

            for deCdata in ys_line:
                decompData.append(deCdata)
                
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
# =============================================================================
# #=================每一天壓縮後數據==================================
#     #==each day polynorimal data
#     dtPolyData={'start':start,
#                 'end':end,
#                 'min_r2':min_r2,
#                 'poly n':pIndex,
#                 'wd_size%':wdsize_percent,
#                 'min_interval%':min_interval_percent,
#                 'angle':angle,
#                 'coef':coef_ary,
#                 'coeff_5':coeff_5,
#                 'coeff_4':coeff_4,
#                 'coeff_3':coeff_3,
#                 'coeff_2':coeff_2,
#                 'coeff_1':coeff_1,
#                 'coeff_0':coeff_0,
#                 'Delta':Dlta,
#                 'R2_Raw':R2_PnR,
#                 'R2_SGF':R2_PnS
#                 }
#     headerPD=['start','end','coeff_5','coeff_4','coeff_3','coeff_2','coeff_1','coeff_0','R2_Raw','Delta']
#     dfpolyDtlData=pd.DataFrame(dtPolyData,columns=headerPD,index=None)
#     SnrCsvfileName='Data_csv\\SlidingWindow\\Chebyshev\\Worst compressing data'+'\\'+fileName+"_DetailData.csv"
#     dfpolyDtlData.to_csv(SnrCsvfileName,mode='w')
#     print('總結:times=',len(times),'deCompDaya=',len(decompData))
#     
#     
#     
#     
#     
#     #==each day deCompression data
#     dtdeCData={'times':times,
#             'Data':decompData
#             }
#     
#     headerDC=['times','Data']
#     dfdeCData=pd.DataFrame(dtdeCData,columns=headerDC,index=None)
#     
#     deCompCsvfileName='Data_csv\\SlidingWindow\\Chebyshev\\Worst compressing data'+'\\'+fileName+"_DecompressionDetailData.csv"
# 
#     dfdeCData.to_csv(deCompCsvfileName,mode='w')
#     
# =============================================================================
    
    segNum=len(start)# num of segement 
    tot_segNum+=segNum# total number of segements in all data 
    Nr=len(t)*2*8
    Nc=segNum*(pIndex+4)*8
    comp_ratio=(Nr-Nc)/Nr
    #print(dfpolyDtlData)
    R2_RnS=round(mthT.coeff_of_determination(np.array(data),sgf,startPt,endPt),3)
    MeanR2PnR=round(np.mean(R2_PnR),3)
    MeanR2PnS=round(np.mean(R2_PnS),3)
    STD=round(np.std(R2_PnS),3)
    timer=tEnd-tStart
    #print('MeanR2PnR = ' ,MeanR2PnR,', MeanR2PnS = ',MeanR2PnS)
    #print(fileName[:2]+fileName[3:])
    dtMean={
            'date':fileName[:-3],
            'Sensor':fileName[6:],
            'data Length':len(t),
            'pIndex':pIndex,
            'Minium interval':min_time_interval,
            'angle':angle,
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
        pltT.PlotLy(t,window_size_percent,min_interval_percent,polyIndex,fileName,pltData,plotisOpen)
    return dtMean


if __name__ =="__main__":
    fileName=fT.getFileName(mypath)
    #print(fileName)
    #===condition====
    SGwd_length=11# window length must odd ,SGwd_length >2N+1
    Ord=5
    
    
    pIndex=5##多項式次數
    angle=0
    #  反應差  1 2 3 4 5  10 20 30
    wdsize_percent=0.05#
    min_interval_percent=0.0#limit  = 0.001
    min_r2=0.99 #固定
    

    Isplot=True
    plotisOpen=False
    #rndFile=88#random.randint(0,len(fileName))
    count=0
    reset=True
    spr2Mean=[]
    spRatio=[]
    spTimer=[]
    OldSplist=[]
    spNum=30
    #test=list(range(80,86))

    testList=[3,4,8,10,15,17,23,27,36,41,43,45,49,50,53,54,59,65,74,82,84,85,114,117,121,
              123,130,140,154,156]
    test=[80]
    while(count<1000):
        count+=1
        max_slope=np.tan(angle*(pi/180))
        w=SGwd_length
        print('Started time:',count)
        print('pIndex: ',pIndex,' wd Size: ',wdsize_percent,'r2: ',min_r2 )
        print('Interval: ',str(round(min_interval_percent,5)))
    # =============================================================================
    #     dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\SGpolyOrd '\
    #     +str(Ord)+'\\PolyIndex '+str(pIndex)+'\\SGwd_length '+str(w)\
    #     +'\\max angle '+str(angle)
    # =============================================================================
        dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\2018_Mean_R2Data'
        fT.mkfolder(dirMean)
        #print('wd Length: ',SGwd_length,'SGpolyOrd: ',SGpolyOrd)
        Meanheader=["date",
                    "Sensor",
                    'data Length',
                    'pIndex',
                    'Minium interval',
                    "segNum",
                    "comp_ratio",
                    "R2_R&S",
                    "Mean_R2_P&R",
                    "Mean_R2_P&S",
                    'timer',
                    'STD']
        #for i  in range(len(fileName)):
        count_T=0
        ltMean=[]
        spList=rSp.Sampling(len(fileName),spNum,OldSplist)##簡單隨機抽樣樣品 list
        OldSplist.append(spList)
        
        
        for i in spList :#len(fileName)
            #i=rndFile
            sensorType=fileName[i][6:-1]  
            #print(sensorType)
    # =============================================================================
    #             if(sensorType=='T'):
    # =============================================================================
                #print(fileName[i])
            data,times=fT.readCSV(mypath,fileName[i])
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
                                   isplot=Isplot))
        dfpolyMeanDay=pd.DataFrame(ltMean,columns=Meanheader)
        
        MeanCsvfileName=dirMean+'\\2018_Mean_R2Data'+str(count)+'.csv'
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
                T_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&R'])
            if (checkChar=='H'):
                #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
                H_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&R'])
                
        #idx=dfpolyMeanDay.index[dfpolyMeanDay['Sensor']=='T'].tolist()
        T_meanindf=dfpolyMeanDay['Mean_R2_P&R'].values
        #H_meanindf=dfpolyMeanDay.loc['Mean_R2_P&S',[dfpolyMeanDay['Sensor']=='T'].tolist
        mean_totLen=round(np.mean(dfpolyMeanDay['data Length']),3)
        mean_compRatio=round(np.mean(dfpolyMeanDay['comp_ratio']),3)
        allR2rns=round(np.mean(dfpolyMeanDay['R2_R&S']),3)
        allR2pnr=round(np.mean(dfpolyMeanDay['Mean_R2_P&R']),3)
        allR2pns=round(np.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
        Tr2pnr=round(np.mean(T_r2),3)
        Hr2pnr=round(np.mean(H_r2),3)
        STDall=round(np.std(dfpolyMeanDay['Mean_R2_P&R']),3)
        TimerMean=round(np.mean(dfpolyMeanDay['timer']),3)
        #print('T ',Tr2pns,' H ',Hr2pns)
        tolMean={'count':count,
                 'sgf window length':[w],
                 'sgf SGpolyOrder':[Ord],
                 'Angle':[angle],
                 'Poly n':[pIndex],
                 'wd_size_%':wdsize_percent,
                 'min_interval_%':min_interval_percent,
                 'min_r2':min_r2,
                 'mean_segTol':[mean_segTol],
                 'mean_totalLength':[mean_totLen],
                 'mean_compRatio':[mean_compRatio],
                 'All R2 R&S mean':allR2rns,
                 'All R2 P&R mean':allR2pnr,
                 'All R2 P&S mean':allR2pns,
                 'T R2 mean':Tr2pnr,
                 'H R2 mean':Hr2pnr,
                 'STD_All':STDall,
                 'TimerMean':TimerMean
                 }
        tolMheader=['count',
                    'sgf window length',
                    'sgf SGpolyOrder',
                    'Poly n',
                    'wd_size_%',
                    'min_interval_%',
                    'min_r2',
                    'mean_segTol',
                    'mean_totalLength',
                    'mean_compRatio',
                    'All R2 P&R mean',
                    'All R2 P&S mean',
                    'All R2 R&S mean',
                    'T R2 mean',
                    'H R2 mean',
                    'STD_All',
                    'TimerMean'
                    ]
        #tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllMeanRaw&Poly.csv'
        tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllMeanRaw&Poly.csv'
        dftolMean=pd.DataFrame(tolMean,columns=tolMheader)
        #print(dftolMean)
        #print(tolMeanFile)
        if (pth.isfile(tolMeanFile)!=True):  
            dftolMean.to_csv(tolMeanFile,mode='w',index=None)
        else:
            dftolMean.to_csv(tolMeanFile,mode='a',header=None,index=None)
        dftolMean=pd.DataFrame(None,None)
        #dftolMean.to_csv(tolMeanFile,mode='a',line_terminator="\n")
        print('All is done in '+str(count))
    AllSpList={'list':OldSplist}
    dfAllSpList=pd.DataFrame(AllSpList)
    AllSpListPath='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllSplist.csv'
    if (pth.isfile(AllSpListPath)!=True):  
        dfAllSpList.to_csv(AllSpListPath,mode='w',header=None,index=None)
    else:
        dfAllSpList.to_csv(AllSpListPath,mode='a',header=None,index=None)
    
