# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 00:29:25 2018

@author: Jeff PC
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:27:43 2018

@author: Jeff
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
import datetime

mypath ='excelFolder/'
cf.go_offline()
def compR(Nc,Nr):
    #print(Nc,Nr)
    Nr=Nr*2*8
    Nc=Nc*(pIndex+4)*8
    comp_ratio=(Nr-Nc)/Nr
    return round(comp_ratio,2)
def calRMSD(tdata,dData):
    rmsdCData=[]
    mRMSD=0
    sumData=0
# =============================================================================
#     print(len(tdata))
#     print(len(dData))
# =============================================================================
    if(len(tdata)!=0):
        for n in range(len(tdata)):
        ## to compare decompress Alg data and Decompress DB data
            sumData+=(np.round(tdata[n],5)-np.round(dData[n],5))**2
        rmsdCData.append(float(np.round(math.sqrt(sumData/len(tdata)),5)))
        mRMSD=round(np.mean(rmsdCData),3)
    else:
        mRMSD=0
    return mRMSD
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
            x=plotTime, # assign x as the dataframe column 'x'
            y=v,
            name='Raw',
            mode='lines',
            marker=dict(
                    size=10,
                    color='rgba(104,103,103,0.8)'),
                    line=dict(width=5,)
# =============================================================================
#                     ),
#         go.Scatter(        
#             x=times, # assign x as the dataframe column 'x'
#             y=sgf,
#             name='S-Gf: R2:'+str(R2_RnS),
#             mode='line',
#             marker=dict(
#                     size=5,
#                     color='rgba(0,0,0,0.0)'),
#                     line=dict(
#                             width=3,
#                             color='rgba(0,0,0,0.0)')
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
    R2_ngt=[]
    R2_noon=[]
    R2_afr=[]
    R2_mrg=[]
    mrgData=[]
    noonData=[]
    aftData=[]
    ngtData=[]
    Dlta=[]
    dtMean={}
    sensor=fileName[6:-1]
    Maxr2SGF=0.0
    Maxr2RW=0.0
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

    mrg=0
    noon=0
    aft=0
    ngt=0
    OmrgData=[]
    OnonData=[]
    OaftData=[]
    OngtData=[]
    OrgMrg=0
    OrgNoon=0
    OrgAft=0
    OrgNgt=0
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
            if ((i-startPt)>1):
                endPt=i+1
                delta=endPt-startPt
                coeff,ys_line,rsqSGF,rsqRW = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                if(rsqRW>=Maxr2RW):
                     Maxr2RW=rsqRW
                     MaxYs=ys_line
                     MaxEnd=endPt
                     MaxCoeff=coeff
            elif((i-startPt)<=1):                 
                if(Maxr2RW==0.0):
                    endPt=len(t)
                    delta=endPt-startPt
                    coeff,ys_line,rsqSGF,rsqRW = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                    islimit=True
                else:
                    rsqRW=Maxr2RW
                    endPt=MaxEnd
                    coeff=MaxCoeff
                    delta=endPt-startPt
                    ys_line=MaxYs
                    delta=endPt-startPt
                    islimit=True
            if (rsqRW>=min_r2) or islimit :    
                start.append(times[startPt])                
                if(endPt!=len(times)):    
                    end.append(times[endPt])
                else:
                    end.append(times[endPt-1])            
                coeff_5.append(float(coeff[0]))
                coeff_4.append(float(coeff[1]))
                coeff_3.append(float(coeff[2]))
                coeff_2.append(float(coeff[3]))
                coeff_1.append(float(coeff[4]))
                coeff_0.append(float(coeff[5]))
                coef_ary.extend(coeff)
                decompData.extend(ys_line)
                Dlta.append(delta)
                    
                DeltaCnt =DeltaCnt+endPt-startPt
                global pltData

                c+=1
                R2_PnR.append(round(rsqRW,3))
                R2_PnS.append(round(rsqSGF,3))
                startPt= endPt
                interval=startPt+int((len(t)*window_size_percent))-1
                
    # =============================================================================
                if (interval>=len(t)):
                    interval=len(t)-1
                MaxCoeff=[]
                MaxYs=[]
                Maxr2RW=0.0
                MaxEnd=interval
                break
            
    tEnd = time.time()#計時結束

    for x in range(len(data)):
        if(times[x].hour<6):
            OrgMrg+=1
        elif(times[x].hour>=6 and times[x].hour<12):
            OrgNoon+=1
        elif(times[x].hour>=12 and times[x].hour<=18):
            OrgAft+=1
        elif(times[x].hour>=18 and times[x].hour<=23):
            OrgNgt+=1
#=================每一天壓縮後數據==================================
# =============================================================================
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
# =============================================================================
# =============================================================================
# 
#     print('總結:times=',len(times),'deCompDaya=',len(decompData),'min_r2=',min_r2)
#     print('分段數量: 0-6點: ',mrg,'  6-12點: ',noon,'  12-18點: ',aft,'  18-23點: ',ngt)
#     print('R2: 0-6點: ',round(mthT.coeff_of_determination(np.array(OmrgData),mrgData,startPt,endPt),3),
#           '6-12點: ',round(mthT.coeff_of_determination(np.array(OnonData),noonData,startPt,endPt),3),
#           '12-18點: ',round(mthT.coeff_of_determination(np.array(OaftData),aftData,startPt,endPt),3),
#           '18-23點: ',round(mthT.coeff_of_determination(np.array(OngtData),ngtData,startPt,endPt),3))
#     print('壓縮比: 0-6點: ',compR(mrg,OrgMrg),
#           '6-12點: ',compR(noon,OrgNoon),
#           '12-18點: ',compR(aft,OrgAft),
#           '18-23點: ',compR(ngt,OrgNgt))
#     print('RMSD: 0-6點: ',calRMSD(OmrgData,mrgData),
#           '6-12點: ',calRMSD(OnonData,noonData),
#           '12-18點: ',calRMSD(OaftData,aftData),
#           '18-23點: ',calRMSD(OngtData,ngtData))
#     
#     
#     
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
    R2=round(mthT.coeff_of_determination(np.array(data),decompData,startPt,endPt),3)
    MeanR2=round(np.mean(R2),3)
    STD=round(np.std(R2_PnR,ddof=1 ),3)
    
    sumDCData=0
    for n in range(len(data)):
    ## to compare decompress Alg data and Decompress DB data
        sumDCData+=(np.round(data[n],5)-np.round(decompData[n],5))**2
    RMSDCData.append(float(np.round(math.sqrt(sumDCData/len(data)),5)))
    MeanRMSD=round(np.mean(RMSDCData),3)
    CRatio=round(comp_ratio,3)
    timer=tEnd-tStart
    print('分段總數= ',str(mrg+noon+aft+ngt),'  Mean R2=',MeanR2,'  CompRatio=',CRatio,'  RMSD=',MeanRMSD,)
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
            'Mean_R2':MeanR2,
            'Mean_RMSD':MeanRMSD,
            'STD':STD
            }
#    print(df)
#    df.head()
    #print(pltData)

    
    
    #print(len(plotTime),':',len(decompData))
    pltData += [
                    go.Scatter(
                        x=plotTime, # assign x as the dataframe column 'x'
                        y=decompData,
                        mode='lines',
                        name='CHEB',
                        marker=dict(
                                size=5,
                                color='rgba(255,0,0,0.9)'
                                )
                        )]
    if isplot:
        #print(window_size_percent)
        pltT.PlotLy(t,window_size_percent,min_r2,polyIndex,fileName,pltData,plotisOpen)
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
    wdsize_percent=0.1#
    min_interval_percent=0.00#limit  = 0.001
    min_r2=0.9#固定
    

    Isplot=False
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

    test=[31]
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
        dirMean='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\2018_Mean_R2Data(Less100)'
        fT.mkfolder(dirMean)
        #print('wd Length: ',SGwd_length,'SGpolyOrd: ',SGpolyOrd)
        Meanheader=["date",
                    "Sensor",
                    'data Length',
                    'pIndex',
                    'Minium interval',
                    "segNum",
                    "comp_ratio",
                    'Mean_R2',
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
        
        #print(len(fileName))
        for i in range(len(fileName)):#len(fileName)
            sensorType=fileName[i][6:]  
            if(sensorType=='H1'or sensorType=='H2' ):
                data,times=fT.readCSV(mypath,fileName[i])
                plotTime=[]
                for ts in times:
                    plotTime.append(datetime.datetime.fromtimestamp(time.mktime(ts.timetuple())))
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
        
        MeanCsvfileName=dirMean+'\\2018_Mean_R2Data(Less100)_R2'+str(min_r2)+'wd'+str(wdsize_percent)+ssrType+dt.datetime.now().strftime('%m%d')+'.csv'
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
                T_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2'])
                cntT+=1
            if (checkChar=='H'):
                cntH+=1
                #print (i,dfpolyMeanDay.iloc[i]['Mean_R2_P&S'])
                H_r2.append(dfpolyMeanDay.iloc[i]['Mean_R2'])
                
        #idx=dfpolyMeanDay.index[dfpolyMeanDay['Sensor']=='T'].tolist()
        T_meanindf=dfpolyMeanDay['Mean_R2'].values
        #H_meanindf=dfpolyMeanDay.loc['Mean_R2_P&S',[dfpolyMeanDay['Sensor']=='T'].tolist
        mean_totLen=round(np.mean(dfpolyMeanDay['data Length']),3)
        mean_compRatio=round(np.mean(dfpolyMeanDay['comp_ratio']),3)
#        allR2rns=round(np.mean(dfpolyMeanDay['R2_R&S']),3)
        allR2pnr=round(np.mean(dfpolyMeanDay['Mean_R2']),3)
        #allR2pns=round(np.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
        Tr2pnr=round(np.mean(T_r2),3)
        Hr2pnr=round(np.mean(H_r2),3)
        
        allRMSD=round(np.mean(dfpolyMeanDay['Mean_RMSD']),3)
        STDall=round(np.std(dfpolyMeanDay['Mean_R2']),3)
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
                 #'All R2 R&S mean':allR2rns,
                 'All R2 P&R mean':allR2pnr,
                 #'All R2 P&S mean':allR2pns,
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
        tolMeanFile='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\Less100AllMeanRaw&PolyRAW'+dt.datetime.now().strftime('%m%d')+'.csv'
        dftolMean=pd.DataFrame(tolMean,columns=tolMheader)
        #print(dftolMean)
        #print(tolMeanFile)
        if (pth.isfile(tolMeanFile)!=True):  
            dftolMean.to_csv(tolMeanFile,mode='w',index=None)
        else:
            dftolMean.to_csv(tolMeanFile,mode='a',header=None,index=None)
        dftolMean=pd.DataFrame(None,None)
        #dftolMean.to_csv(tolMeanFile,mode='a',line_terminator="\n")
        print('All is done in R2 : '+str(min_r2)+' wds : '+str(wdsize_percent)+' count : '+ str(count))
        
        if (count%3==0) and (count!=1):
# =============================================================================
#             if(count==3):
#                 min_r2=0.90
#             elif(count==6):
#                 min_r2=0.85
# =============================================================================
            wdsize_percent=0.05
        else:
            wdsize_percent+=0.05
            wdsize_percent=np.round(wdsize_percent,3)
    AllSpList={'list':OldSplist}
    dfAllSpList=pd.DataFrame(AllSpList)
    AllSpListPath='Data_csv\\SlidingWindow\\Chebyshev\\Mean\\Less100AllSplistRAWT.csv'
    if (pth.isfile(AllSpListPath)!=True):  
        dfAllSpList.to_csv(AllSpListPath,mode='w',header=None,index=None)
    else:
        dfAllSpList.to_csv(AllSpListPath,mode='a',header=None,index=None)

