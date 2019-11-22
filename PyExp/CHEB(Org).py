# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 17:52:47 2018

@author: Jeff PC
"""
import readList as rdList
import os.path as pth 
import numpy as np
from math import pi
import math
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
# =============================================================================
#                     ),
#         go.Scatter(        
#             x=times, # assign x as the dataframe column 'x'
#             y=sgf,
#             name='S-Gf: R2:'+str(R2_RnS),
#             mode='line',
#             marker=dict(
#                     size=5,
#                     color='rgba(0,0,0,0.8)'),
#                     line=dict(
#                             width=3,
#                             color='rgba(0,0,0,0.8)')
# =============================================================================
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
    if(len(t)>100):
        pass
    else:
        window_size_percent=1
    #print('wdSize:',window_size_percent)
    interval=int(len(t)*window_size_percent)-1
#    interval=6
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
    RMSDCData=[]
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
    rsqRW=0
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
    dirWCdetailFolder='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\Worst compressing data\\'
    fT.mkfolder(dirWCdetailFolder)
    #===condition====
    #max_slope=2 #  反應差
    min_time_interval= int(len(t)*min_interval_percent)
    c=1
    segNum=0
    #print(len(t))
    while(startPt<=(len(t)-1)):

        endPt=startPt+interval
        coeff,ys_line,rsqSGF,rsqRW = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
       
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
        coeff_5.append(float(coeff[0]))
        coeff_4.append(float(coeff[1]))
        coeff_3.append(float(coeff[2]))
        coeff_2.append(float(coeff[3]))
        coeff_1.append(float(coeff[4]))
        #coeff_0.append(float(coeff[5]))
        coef_ary.extend(coeff)
        decompData.extend(ys_line)
        Dlta.append(delta)

        DeltaCnt =DeltaCnt+endPt-startPt
       # print(len(decompData),'Delta=',DeltaCnt)
        global pltData
# =============================================================================
#         pltData += [
#             go.Scatter(
#                 x=times[startPt:endPt], # assign x as the dataframe column 'x'
#                 y=ys_line,
#                 mode='lines',
#                 name=str(c)+' R: '+str(rsqRW),
#                 marker=dict(
#                         size=5,
#                         color='rgba(255,0,0,0.9)'
#                         )
#                 )]
# =============================================================================
        c+=1
        #print(startPt,"-",endPt)
        R2_PnR.append(round(rsqRW,3))
        R2_PnS.append(round(rsqSGF,3))
        startPt= endPt
        if ((startPt+interval)>=len(t))and (endPt<=len(t)-1):      
            interval=len(t)-startPt


   
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
#                 'Delta':Dlta,
#                 'coeff_5':coeff_5,
#                 'coeff_4':coeff_4,
#                 'coeff_3':coeff_3,
#                 'coeff_2':coeff_2,
#                 'coeff_1':coeff_1,
#                 'coeff_0':coeff_0,
#                 'R2_Raw':R2_PnR,
#                 'R2_SGF':R2_PnS
#                 }
#     headerPD=['start','end','Delta','coeff_5','coeff_4','coeff_3','coeff_2','coeff_1','coeff_0']
#     #輸出沒有了r2 值
#     dfpolyDtlData=pd.DataFrame(dtPolyData,columns=headerPD,index=None)
#     SnrCsvfileName='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\Worst compressing data'+'\\'+fileName+"_DetailData.csv"
#     dfpolyDtlData.to_csv(SnrCsvfileName,mode='w',index=None)
#     print('總結:times=',len(times),'deCompDaya=',len(decompData))
# =============================================================================
    
    
    
     
    
# =============================================================================
#     #==each day deCompression data
#     dtdeCData={'times':times,
#             'Data':decompData
#             }
#     
#     headerDC=['times','Data']
#     dfdeCData=pd.DataFrame(dtdeCData,columns=headerDC,index=None)
#     
#     deCompCsvfileName='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\Worst compressing data'+'\\'+fileName+"_DecompressionDetailData.csv"
# 
#     dfdeCData.to_csv(deCompCsvfileName,mode='w',index=None)
#     
# =============================================================================
    
    segNum=len(start)# num of segement 
    tot_segNum+=segNum# total number of segements in all data 
    Nr=len(t)*2*8
    Nc=segNum*(pIndex+4)*8
    comp_ratio=(Nr-Nc)/Nr
    #print(dfpolyDtlData)
    R2_RnS=round(mthT.coeff_of_determination(np.array(data),sgf,startPt,endPt),3)
    R2_RnP=round(mthT.coeff_of_determination(np.array(data),decompData,startPt,endPt),3)
    MeanR2PnR=round(np.mean(R2_PnR),3)
    MeanR2RnP=round(np.mean(R2_RnP),3)
    MeanR2PnS=round(np.mean(R2_PnS),3)
    STD=round(np.std(R2_PnS,ddof=1 ),3)
    sumDCData=0
    for n in range(len(data)):
    ## to compare decompress Alg data and Decompress DB data
        sumDCData+=(np.round(data[n],5)-np.round(decompData[n],5))**2
    RMSDCData.append(float(np.round(math.sqrt(sumDCData/len(data)),5)))
    MeanRMSD=round(np.mean(RMSDCData),3)
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
            'Mean_R2_R&P':MeanR2RnP,
            'Mean_RMSD':MeanRMSD,
            'STD':STD
            }
#    print(df)
#    df.head()
    #print(pltData)
    pltData += [
    go.Scatter(
        x=times, # assign x as the dataframe column 'x'
        y=decompData,
        mode='lines',
        name='CHEB Org',
        marker=dict(
                size=5,
                color='rgba(255,0,0,0.9)'
                )
        )]
    if isplot:
        #print(window_size_percent)
        pltT.PlotLy(t,window_size_percent,'CHEB',polyIndex,fileName,pltData,plotisOpen)
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
    wdsize_percent=0.10#
    min_interval_percent=1#limit  = 0.001
    min_r2=0.9 #固定
    interval=wdsize_percent   

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
    testList35=[2,15,19,28,29,30,31,32,39,48,49,51,70,73,86,88,
              95,97,98,102,110,117,118,125,130,133,135,137,138,151]
    testList67=[6,21,26,27,30,35,40,41,48,52,53,55,56,60,61,69,
                70,73,78,84,85,91,98,101,104,110,117,118,137,147]

    test=[11]
    while(count<1):
        
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
        dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\CHEBOrg'
        fT.mkfolder(dirMean)
        #print('wd Length: ',SGwd_length,'SGpolyOrd: ',SGpolyOrd)
        Meanheader=["date",
                    "Sensor",
                    'data Length',
                    'pIndex',
                    'Minium interval',
                    "segNum",
                    "comp_ratio",
                    "Mean_R2_P&R",
                    "Mean_R2_R&P",
                    "Mean_RMSD",
                    'timer',
                    'STD']
        #for i  in range(len(fileName)):
        count_T=0
        ltMean=[]
# =============================================================================
#         spList=rSp.Sampling(len(fileName),spNum,OldSplist)##簡單隨機抽樣樣品 list
#         OldSplist.append(spList)
# =============================================================================

        ## 讀取RawData Ver 的1000個樣本
        ## 改動了readOldList 中的檔案名稱
        spList=rdList.readOldList(count-1)
        
        
        for i in range(len(fileName)):#len(fileName)
            #i=rndFile
            sensorType=fileName[i][6:]  
            #print(sensorType)
            if(sensorType=='T1'or sensorType=='T2' ):
                #print(fileName[i])
                data,times=fT.readCSV(mypath,fileName[i])
                t=[]
                v=[]
                sgf=[]
                pltData=[]
                tot_segNum=0
                count_T+=1
                stop=False        
                ssrType=sensorType[0]
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
        
        MeanCsvfileName=dirMean+'\\CHEBOrg'+str(min_r2)+'wd'+str(interval)+ssrType+dt.datetime.now().strftime('%m%d')+'.csv'
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
        cntT=0
        cntH=0
        for i in range(0,len(dfpolyMeanDay)):
            checkChar=dfpolyMeanDay['Sensor'][i][0]
            if (checkChar=='T'):
                #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
                T_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&R'])
                cntT+=1
            if (checkChar=='H'):
                cntH+=1
                #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
                H_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2_P&R'])
                
        #idx=dfpolyMeanDay.index[dfpolyMeanDay['Sensor']=='T'].tolist()
        T_meanindf=dfpolyMeanDay['Mean_R2_P&R'].values
        #H_meanindf=dfpolyMeanDay.loc['Mean_R2_P&S',[dfpolyMeanDay['Sensor']=='T'].tolist
        mean_totLen=round(np.mean(dfpolyMeanDay['data Length']),3)
        mean_compRatio=round(np.mean(dfpolyMeanDay['comp_ratio']),3)
        #allR2rns=round(np.mean(dfpolyMeanDay['R2_R&S']),3)
        allR2pnr=round(np.mean(dfpolyMeanDay['Mean_R2_R&P']),3)
        #allR2pns=round(np.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
        Tr2pnr=round(np.mean(T_r2),3)
        Hr2pnr=round(np.mean(H_r2),3)
        allRMSD=round(np.mean(dfpolyMeanDay['Mean_RMSD']),3)
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
#                 'All R2 R&S mean':allR2rns,
                 'All R2 P&R mean':allR2pnr,
#                 'All R2 P&S mean':allR2pns,
                 'T R2 mean':Tr2pnr,
                 'totNumT':cntT,
                 'H R2 mean':Hr2pnr,
                 'totNumH':cntH,
                 'Mean_RMSD':allRMSD,
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
                    'T R2 mean',
                    'totNumT',
                    'H R2 mean',
                    'totNumH',
                    'Mean_RMSD',
                    'STD_All',
                    'TimerMean'
                    ]
        #tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\AllMeanRaw&Poly.csv'
        tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\CHEBOrg.csv'
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
        

