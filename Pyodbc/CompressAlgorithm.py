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


class CompressAlg():  
    mypath ='excelFolder/'
    cf.go_offline()
    def __init__(self):
        pass 
    def getRnSData(self,fileName,SGwd_length,SGpolyOrd):
        t=[]
        v=[]
        pltData=[]
        data,times=fT.readCSV(fileName)
        for i in range(len(data)):
            t.append(i)
            v.append(float(data[i]))
        sgf=savgol_filter(data,SGwd_length,SGpolyOrd)
        R2_RnS=round(mthT.coeff_of_determination(np.array(data),sgf),3)
        #print(times)
        pltData += [
            go.Scatter(
                x=times, # assign x as the dataframe column 'x'
                y=v,
                name='Raw',
                mode='lines',
                marker=dict(
                        size=5,
                        color='rgba(0,0,0,0.8)'),
                        line=dict(width=8,)
# =============================================================================
#                         ),
#             go.Scatter(        
#                 x=times, # assign x as the dataframe column 'x'
#                 y=sgf,
#                 name='S-Gf: R2:'+str(R2_RnS),
#                 mode='line',
#                 marker=dict(
#                         size=5,
#                         color='rgba(0,0,0,0.0)'),
#                         line=dict(
#                                 width=3,
#                                 color='rgba(0,0,0,0.0)')
# =============================================================================
               )]
        return sgf,pltData
    
    def Seg2poly(self,fileName,
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
        t=[]
        v=[]
        
        sgf,pltData=self.getRnSData(fileName,SGwd_length,SGpolyOrd)
        data,times=fT.readCSV(fileName)
        for i in range(len(data)):
            t.append(i)
            v.append(float(data[i]))
        tStart = time.time()#計時開始
        #plt.plot(t,v,'-')
        #plt.plot(t,sgf,'-')
        if(len(data)>100):
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
        #first_inl=0
        R2_PnS=[]
        R2_PnR=[]
        Dlta=[]
        Maxr2SGF=0.0
        Maxr2RW=0.0
        MaxEnd=0
        MaxCoeff=[]
        MaxYs=[]
        rsqSGF=0
        rsqRW=0
        ys_line=[]
        DeltaCnt=0
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
                    coeff,ys_line,rsqSGF,rsqRW = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                    if(rsqRW>=Maxr2SGF):
                         Maxr2SGF=rsqRW
                         MaxYs=ys_line
                         Maxr2RW=rsqRW
                         #MaxStart=startPt
                         MaxEnd=endPt
                         MaxCoeff=coeff
                    break
                elif((i-startPt)<=min_time_interval+1):
                    if(Maxr2SGF==0):
                        endPt=len(t)
                        delta=endPt-startPt
                        coeff,ys_line,rsqSGF,rsqRW = mthT.polyLine(startPt,endPt,polyIndex,t,sgf,data)
                        islimit=True
                    else:
                        rsqRW=Maxr2SGF
                        endPt=MaxEnd
                        coeff=MaxCoeff
                        delta=endPt-startPt
                        rsqRW=Maxr2RW
                        ys_line=MaxYs
                        delta=endPt-startPt
                        islimit=True
                    break
            if (rsqRW>=min_r2) or islimit :    
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
                coeff_0.append(float(coeff[5]))
                coef_ary.extend(coeff)
                decompData.extend(ys_line)
                #print()
                Dlta.append(delta)
                    
                DeltaCnt =DeltaCnt+endPt-startPt
               # print(len(decompData),'Delta=',DeltaCnt)

                pltData += [
                    go.Scatter(
                        x=times[startPt:endPt], # assign x as the dataframe column 'x'
                        y=ys_line,
                        mode='lines',
                        name='',
                        #name=str(c)+'. R: '+str(rsqRW),
                        marker=dict(
                                size=5,
                                color='rgba(255,0,0,1)'),
                        line=dict(width=3,)
                        )]
                c+=1
                #print(startPt,"-",endPt)
                R2_PnR.append(round(rsqRW,3))
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
# =============================================================================
#                 break
# =============================================================================
            else:
                interval-=1
                
        tEnd = time.time()#計時結束
        timer=tEnd-tStart
        #=================每一天壓縮後數據==================================
        #==each day polynorimal data
        dtPolyData={'start':start,
                    'end':end,
                    'Delta':Dlta,
                    'coeff_5':coeff_5,
                    'coeff_4':coeff_4,
                    'coeff_3':coeff_3,
                    'coeff_2':coeff_2,
                    'coeff_1':coeff_1,
                    'coeff_0':coeff_0,
                    'R2_Raw':R2_PnR,
                    }
        headerPD=['start','end','Delta','coeff_5','coeff_4','coeff_3','coeff_2','coeff_1','coeff_0']
        #輸出沒有了r2 值
        dfpolyDtlData=pd.DataFrame(dtPolyData,columns=headerPD,index=None)
        SnrCsvfileName=fileName+"_DetailData.csv"
        dfpolyDtlData.to_csv(SnrCsvfileName,mode='w',index=None)
        print('總結:times=',len(times),'deCompDaya=',len(decompData))
        print('Compressing Time:',timer)
        pltData += [
                        go.Scatter(
                            x=times, # assign x as the dataframe column 'x'
                            y=decompData,
                            mode='lines',
                            name='CHEB',
                            marker=dict(
                                    size=5,
                                    color='rgba(255,0,0,0.0)'
                                    )
                            )]
        pltT.PlotLy(t,window_size_percent,min_interval_percent,polyIndex,fileName,pltData,isplot)
        return coef_ary,decompData
    
if __name__ =="__main__": 
    
    import numpy as np
    import matplotlib.pyplot as pl
    import matplotlib
    import math
    import random
    import pandas as pd
    
    mypath ='excelFolder\\'
    fileName=fT.getFileName(mypath)
    
    N = 250
    fs = 2
    n = [2*math.pi*fs*t/N for t in range(N)]    # 生成了500个介于0.0-31.35之间的点
    # print n
    axis_x = np.linspace(0,2,num=N)

    x = [math.sin(i) for i in n]
    pl.subplot(221)
    pl.plot(axis_x,x)
    pl.title(u'5Hz的正弦信號')
    pl.axis('tight')
     
    #频率为5Hz、幅值为3的正弦+噪声
    x1 = [random.gauss(0,0.25) for i in range(N)]
    xx = []
    #有没有直接两个列表对应项相加的方式？？
    for i in range(len(x)):
        xx.append(x[i]*3 + x1[i])
    
    pl.subplot(221)
    pl.plot(axis_x,xx)
    pl.title(u'5Hz的正弦信號')
    pl.axis('tight')
    xxDict={'timestamp':axis_x,
            'value':xx}
# =============================================================================
#     xxDF=pd.DataFrame(xxDict,columns=['timestamp','value'])
#     xxDF.to_csv(mypath+'sinWaveDiagram.csv',mode='w',index=None)   
# 
# =============================================================================
     
    alg=CompressAlg()
    coef_ary,decompData=alg.Seg2poly(mypath+'sinWaveDiagram',min_r2=0.9,isplot=True)
    #print(decompData)
    
    
    pl.subplot(221)
    pl.plot(axis_x,decompData)
    pl.title(u'DC 後5Hz的正弦信號')
    pl.axis('tight')
    xxDict={'timestamp':axis_x,
            'value':xx}
    #print(coef_ary)

    