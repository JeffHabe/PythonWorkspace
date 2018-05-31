#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from os import walk,makedirs
import os.path as pth 
import pandas as pd
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt
import sys
import numpy
import datetime
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import plot
import warnings


cf.go_offline()
pltData=[]
mypath ='excelFolder\\'
#===========getFileName==================
def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return f
#=========mkfolder====================
def mkfolder(directory):
    if not pth.exists(directory):
        makedirs(directory)
#=============Squared Error=============
def squared_error(ys_orig,ys_line):
    return sum((ys_line-ys_orig)**2)
#==============coeff_of_determination==========
def coeff_of_determination(ys_orig, ys_line):
    y_mean_line = [numpy.mean(ys_orig) for y in ys_orig]
    squared_error_regr = round(squared_error(ys_orig,ys_line),4)
    squared_error_y_mean = round(squared_error(ys_orig,y_mean_line),4)
    if(squared_error_y_mean==0):
        #print(startPt,'-',endPt)
        return 1
    else:    
        R2= 1 - ( squared_error_regr / squared_error_y_mean)
        return R2
#===========PlotLy=======================   
def PlotLy(pltData,fileName,polyOrd,polyIndex,wd_length):
    #print(pltData)
    layout={'title':fileName+' Plot',
                          'font': dict(size=16)}
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")

    filePath=".\Plot_html\\SWAB\\"+'wdL'+str(wd_length)+'\\'+'polyOrd'+str(polyOrd)+'\\Index'+str(polyIndex)+'\\'
    mkfolder(filePath)
    plot(pltData,layout,filename=filePath+fileName+".html")
########################################
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    #print(x)
    pd.reset_option('display.max_rows')
#=============calculate_error=============

def calculate_error(s1, s2,poly_index):
    '''
    A function which takes in a time series and returns the approximation
    error of the linear segment approximation of it
    
    BESSER TODO: Use https://en.wikipedia.org/wiki/Least_trimmed_squares
    weil normaler Error failen kann!
    
    '''
    # cost of merging segment s1 and s2
    fuse = pd.concat([s1, s2])
    
    # define line
    times = fuse.index.astype(numpy.int64)
    values = [f[0] for f in fuse.values.astype(numpy.float64)]
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            coefficients = numpy.polyfit(times, values, poly_index)
        except numpy.RankWarning:
            coefficients = numpy.polyfit(times, values, 1)
            #print('======poly index change to "1" ======')
            with open("log.txt", "a") as text_file:
                text_file.write("log : length %s \n" % len(values))
    approximated_values = numpy.poly1d(coefficients)(times)
    # Error measure
    mean_distance = (abs(values - approximated_values)).mean(axis=0)   
    return mean_distance


#=====================bottom_up=========================
def bottom_up(T, max_error,poly_index):
    seg_ts = []    
    if(len(T)<3):
        return [T]
    
    for i in range(0, len(T), 2):
        seg_ts = seg_ts + [T.iloc[i:i+2]]
        #print(seg_ts)
    merge_cost = [0]* (len(seg_ts)-1)
    for i in range(0, len(seg_ts)-1):
        merge_cost[i] = calculate_error(seg_ts[i], seg_ts[i+1],poly_index)
    #print(merge_cost)    
    while min(merge_cost) < max_error:
        index = merge_cost.index(min(merge_cost)) # find cheapest pair to merge
        seg_ts[index] = pd.concat([seg_ts[index], seg_ts[index+1]])
        del(seg_ts[index+1])
        del(merge_cost[index])
        if(len(seg_ts)==1):
            #print("\n\nSEG "+ str(seg_ts))
            #print("\nCosts "+ str(merge_cost))
            break
        if (index+1)< len(seg_ts): merge_cost[index] = calculate_error(seg_ts[index], seg_ts[index+1],poly_index)
        merge_cost[index-1] = calculate_error(seg_ts[index-1], seg_ts[index],poly_index);
        #print(merge_cost)
        #print("\n\nSEG "+ str(seg_ts))
        #print("\nCosts "+ str(merge_cost))
    return seg_ts

#=======================best line========================
def best_line(max_error, input_df, w, start_idx, upper_bound,poly_index):
    ''' 
    finds data corresponding to a single segment using the 
    (relatively poor) Sliding Windows and gives it to the buffer.
    '''
    error = 0
    idx = start_idx + len(w)
    S_prev = w
    if(idx >= len(input_df)):
        return S_prev
    
    while error <= max_error:
        #print(input_df)
        #print(input_df.iloc[idx:idx+1])
        # ADD ONE Point as long as smaller than error
        S = pd.concat([S_prev, input_df.iloc[idx:idx+1]])
        idx += 1
        
        times = S.index.astype(numpy.int64)
        values = [f[0] for f in S.values.astype(numpy.float64)]
        
        # line approximation
        coefficients = numpy.polyfit(times, values, poly_index)
# =============================================================================
#         with warnings.catch_warnings():
#             warnings.filterwarnings('error')
#             try:
#                 coefficients = numpy.polyfit(times, values, poly_index)
#             except numpy.RankWarning:
#                 coefficients = numpy.polyfit(times, values, (poly_index-1))
#                 print('======poly index changed ======')
#                 with open("best_line_LOG.txt", "a") as text_file:
#                     text_file.write("log : length %s \n" % len(values))
# =============================================================================
        approximated_values = numpy.poly1d(coefficients)(times)

        # curve y(x) = a[0] * x + a[1]
        
        # determine error = mean of di stance between points
        error = (abs(values - approximated_values)).mean(axis=0)
        
        if error <= max_error:
            S_prev = S
        
        if(len(S_prev)>upper_bound) or len(input_df.iloc[idx:idx+1])==0:
            break
        # todo: gebe 2 Punkte zurueck die die Linie darstellt fuer diesen 
        # Abschnitt wegen Zeit passt es trotzdem normal

    # return line of best fit approximated_values
    #S_prev = pd.TimeSeries([approximated_values[0], approximated_values[-2]], index=[S_prev.index[0], S_prev.index[-1]]).to_frame()
    return S_prev
#==============approximated_segment========
def approximated_segment(in_seg,poly_index):
# =============================================================================
#     if len(in_seg)<3:
#         in_seg['avg_value'] =-10# numpy.mean([f[0] for f in in_seg.values.astype(numpy.float64)])        
#         return in_seg
# =============================================================================
        
    times = in_seg.index.astype(numpy.int64)
    values = [f[0] for f in in_seg.values.astype(numpy.float64)]
    #print(in_seg.index[0])
    #print(in_seg.index[-1])  
    coefficients = numpy.polyfit(times, values, poly_index)
# =============================================================================
#     with warnings.catch_warnings():
#         warnings.filterwarnings('error')
#         try:
#             coefficients = numpy.polyfit(times, values, poly_index)
#         except numpy.RankWarning:
#             coefficients = numpy.polyfit(times, values,1)
#             print('======poly index changed ======')
#             with open("approximated_segment_lOG.txt", "a") as text_file:
#                 text_file.write("log : length %s \n" % len(values))
# =============================================================================
    approximated_values = numpy.poly1d(coefficients)(times)
    #print(approximated_values[-2])

    new_seg = pd.Series([approximated_values[0], approximated_values[-1]], index=[in_seg.index[0],in_seg.index[-1]]).to_frame()
# =============================================================================
#     print()
#     print(len(approximated_values))
#     print(approximated_values)  
#     print('[approximated_values[0], approximated_values[-2]]')
#     print([approximated_values[0], approximated_values[-2]])
#     print()
#     print(len(in_seg))
#     print('[in_seg.index[0],in_seg.index[-1]]')
#     print([in_seg.index[0],in_seg.index[-1]])
#     print()
#     print(new_seg)
# =============================================================================

    # new_seg['avg_value'] = numpy.mean(values)
    #print(new_seg)
    
    return new_seg
#==============swab====================
def swab(raw_df,input_df, max_error, seg_num, in_window_size,poly_index):

    # 1. read in w data points     
    cur_nr = 0
    window_size = in_window_size
    w_nr = cur_nr + window_size
    tot_size = len(input_df)
    w = input_df.iloc[cur_nr:w_nr]
    lower_bound = w_nr/2
    upper_bound = 2*w_nr
    seg_ts = []
    rsqSGF=[]
    rsqTT=[]
    Delta=[]
    fun_Coef=[]
    #plt.plot(input_df.index, input_df.values, marker="o", linestyle="None")
    #plt.show()
    #print("Processing from "+ str(cur_nr) +" to "+ str(w_nr))
    #print("From "+ str(w.iloc[0:1]) + " to "+ str(w.iloc[-2:-1]))
    last_run = False
    
    while True:
        T = bottom_up(w, max_error,poly_index)
        # creates new approximated segment for T[0] and adds it
        #print(T)
        seg_ts += [approximated_segment(T[0],poly_index)] # add this segment represented by a line
# =============================================================================
#         print(seg_ts)
#         print(seg_ts[-1].index[0])
#         print(seg_ts[-1].values)
#         #print(w[seg_ts[-1].index[0]:seg_ts[-1].index[1]].values)
#         print()
# =============================================================================
        global pltData

        #t =[datetime.timedelta(times) for times in T[0].index.astype(numpy.int64)]
       # print(t)
        times = T[0].index.astype(numpy.int64)
        values = [f[0] for f in T[0].values.astype(numpy.float64)]
        r_values=[f[0] for f in raw_df.iloc[cur_nr:cur_nr+len(T[0])].values.astype(numpy.float64)]   
        #print(values)
        #print(r_values)
        # line approximation
        fun_Coef.append(numpy.polyfit(times, values, poly_index))
        approximated_values = numpy.poly1d(fun_Coef[-1])(times)
        
        times=T[0].index
        #values = [f for f in approximated_values] 

        # finished if cur_nr > length of input
        if cur_nr >= tot_size or last_run:            
            if T[1:]: 
                seg_ts += [approximated_segment(T[1])]
            break
        # remove elements of T[0] from w
        cur_nr += len(T[0])-1 # overlap
        w_nr = cur_nr + window_size
        
        if (len(input_df) <= w_nr): 
            w_nr = -1
            last_run = True
            w  = input_df.iloc[cur_nr:]
        else:
            w  = input_df.iloc[cur_nr:w_nr] # - 4

        w = w.sort_index()

        w = best_line(max_error, input_df, w, cur_nr, upper_bound,poly_index) # == w + best_line add further data points (=variable window)

        # adjust depending on lower and upper bound
        if len(w)>upper_bound:
            w = w.iloc[:upper_bound]
            #print("Processing from "+ str(cur_nr) +" to "+ str(cur_nr+len(w)) + "   Total: " + str(tot_size))
        #else: 
            #print("Processing from "+ str(cur_nr) +" to "+ str(w_nr+len(w)) + "   Total: " + str(tot_size))
       #     print(w_nr)
#===============coef of det====================
        rsqTT.append(round(coeff_of_determination(numpy.array(r_values),approximated_values),3))
        rsqSGF.append(round(coeff_of_determination(numpy.array(values),approximated_values),3))
        #seg_ts['rsq'] = pd.Series(rsqSGF)
        Delta.append(len(T[0]))
        #print('rsqSGF: ',rsqSGF[-1],'rsqTT: ',rsqTT[-1])
        
        pltData+=[go.Scatter(        
                        x=times, # assign x as the dataframe column 'x'
                        y=approximated_values,
                        mode='line',
                        name=str(rsqSGF[-1])
                       )]
        #print(pltData)
        #plt.plot(seg_ts[-1].index, seg_ts[-1].values,'r--')
        #plt.show()

#======================================================================================
        if last_run :
            break
    ''' iterate further!'''
    seg_data={'seg_ts':seg_ts,
              'Coeff':fun_Coef,
              'rsqSGF':rsqSGF,
              'rsqTT':rsqTT,
              'Delta':Delta}
    #print(seg_data)
    return seg_data
#=========getR2S data=====================
def getR2SData(df,wd_length,polyOrd):
    times = df.index
    values = [f[0] for f in df.values.astype(numpy.float64)]
    sgf=savgol_filter(values,wd_length,polyOrd)
    sgf_df=pd.Series(sgf,
                     index=pd.to_datetime(df.index,unit='s',utc=True),
                     name='SGf'
                     ).to_frame()
    #print(sgf_df)
    global pltData
    #print(times)
    pltData += [
        go.Scatter(
            x=times, # assign x as the dataframe column 'x'
            y=values,
            name='raw data',
            mode='lines+markers',
            marker=dict(
                    size=2,
                    color='rgba(0,0,255,0.7)'),
                    line=dict(
                            width=2,
                            color='rgba(0,0,255,0.3)')),
        go.Scatter(        
            x=times, # assign x as the dataframe column 'x'
            y=sgf,
            name='sgf data',
            mode='lines',
            marker=dict(
                    size=10,
                    color='rgba(0,0,0,0)'),
                    line=dict(
                            width=5,
                            color='rgba(0,255,0,0.5)')
           )]
    return sgf_df
    
def swab_alg(df,fileName, max_error = 0.1, window_size = 3, label_time = "timestamp",
             label_value = "mid", unit_time = "s", thr_steady = 0.1, thr_steep = 1.75,
             plot_it = True, polyIndex = 1, wd_length = 11 , polyOrd = 2):

    # 1. Load data
    df= df.sort_values(label_time)
    pre_df = pd.Series(df[label_value].get_values(), index=pd.to_datetime(df[label_time],unit='s',utc=True),name= fileName).to_frame()
    #print(pre_df)
    sgf_df=getR2SData(pre_df,wd_length,polyOrd)
    
    
  
    #print(pre_df.values)
    #print(pre_df.iloc[:,0])
    # 2. SWAB Algorithm by Eamonn Keogh
    error_bound = (max(sgf_df.iloc[:,0]) - min(sgf_df.iloc[:,0]))*max_error
    seg_dt= swab(pre_df,sgf_df, error_bound, 10, window_size,polyIndex)#[0]
    #print(seg_dt)
    res_list=seg_dt['seg_ts']
    # 3. assign value now depending on slope of curve
    # 1. plot points
# =============================================================================
#     if plot_it:
#         #plt.plot(pre_df.index, pre_df.values, "c--", linestyle="-")
#         #print(pltData)
#         PlotLy(pltData,fileName,polyOrd,polyIndex,wd_length)
#         #plt.show()
# =============================================================================
    # pass result segments to dataframe
    res_df = []
    first = True
    seg_id = 0
    for sub_df in res_list: 
        seg_id += 1
        #print(sub_df)
        if len(sub_df) < 2: continue           
# =============================================================================
#         slope = 1000000000*(sub_df.values[1][0] - sub_df.values[0][0])/(sub_df.index.astype(numpy.int64)[1]-sub_df.index.astype(numpy.int64)[0])
#         assign = "steady" # -16 to 16 degrees
#         if slope > thr_steady and slope <= thr_steep: assign = "increase" # 10 to 60 degrees
#         if slope > thr_steep: assign = "steep_increase" # 60 to 90 degrees
#         if slope < -thr_steady and slope >= -thr_steep: assign = "decrease"  # -10 to -60 degrees
#         if slope < -thr_steep: assign = "steep_decrease" # -60 to -90 degrees
#         sub_df["trend"] = pd.Series([assign, assign], index=sub_df.index)
# =============================================================================
        sub_df["seg_id"] = seg_id
        #sub_df[label_time] = pd.to_datetime(sub_df.index.astype(numpy.int64)[0])
        sub_df[label_time+"_end"] =pd.to_datetime(sub_df.index.astype(numpy.int64)[1])
        # segment 
        if first:
            res_df = sub_df.head(1)
            first = False
        else: 
            ''' if same as previous remove redundant information NEU? '''
            res_df = pd.concat([res_df, sub_df.head(1)])

    res_df.rename(columns= {0:'value'},inplace =True)
    res_df.columns.name=label_time
    res_df.value.name =label_value
    res_df['Coeff']=seg_dt['Coeff']
    res_df['Delta']=seg_dt['Delta']
    res_df['R2_SGF']=seg_dt['rsqSGF']
    res_df['R2_Raw']=seg_dt['rsqTT']
    #print(res_df)
    dirSnr=''
    sensor=fileName[6:-1]
    if(sensor=='T'):
        dirSnr=sensor+'\\'
    dirT='Data_csv\\SWAB\\'+dirSnr+'PolyOrd\\'+str(polyOrd)+'\\PolyIndex\\'+str(polyIndex)+'\\WD_Length\\'+str(wd_length) 
    mkfolder(dirT)
    SnrCsvfileName=dirT+'\\'+fileName+"_DetailData.csv"
    res_df.to_csv(SnrCsvfileName)
    global tot_segNum
    tot_segNum+=len(res_df)
    R_values =numpy.array( [f[0] for f in pre_df.values.astype(numpy.float64)])
    SG_values = numpy.array([f[0] for f in sgf_df.values.astype(numpy.float64)])
    R2_RnS=round(coeff_of_determination(R_values,SG_values),3)
    MeanR2_Raw=round(numpy.mean(res_df['R2_Raw']),3)
    MeanR2_SGF=round(numpy.mean(res_df['R2_SGF']),3)
    #print(MeanR2_Raw)
    #print(MeanR2_SGF)
    dtMean={
                 'date':fileName[:-3],
                 'Sensor':fileName[6:],
                 'window_size':window_size,
                 'tot_segNum':tot_segNum,
                 'R2_R&S':R2_RnS,
                 'Mean_R2_P&R':MeanR2_Raw,
                 'Mean_R2_P&S':MeanR2_SGF
                 }
        #===================================================
# =============================================================================
#         dtPolyData={'start':start,
#                     'end':end,
#                     #'interval':intervalAry,
#                     #'A':coefA_fun,
#                     #'B':coefB_fun,
#                     #'C':coefC_fun,
#                     #'D':coefD_fun,
#                     'Delta':Dlta,
#                     'R2_Raw':R2_PnR,
#                     'R2_SGF':R2_PnS
#                     }
#         dirT='Data_csv\\'+dirSnr+'PolyOrd\\'+str(polyOrd)+'\\PolyIndex\\'+str(polyIndex)+'\\WD_Length\\'+str(wd_length) 
#         mkfolder(dirT)
#         header=['start','end','Delta','R2_Raw','R2_SGF']
#         dfpolyDtlData=pd.DataFrame(dtPolyData,columns=header,index=None)
#         SnrCsvfileName=dirT+'\\'+fileName+"_DetailData.csv"
#         dfpolyDtlData.to_csv(SnrCsvfileName)
#         tot_segNum+=len(R2_PnS)
#         #print(dfpolyDtlData)
#         R2_RnS=round(coeff_of_determination(np.array(data),sgf,startPt,endPt),3)
#         MeanR2PnR=round(np.mean(R2_PnR),3)
#         MeanR2PnS=round(np.mean(R2_PnS),3)
#         #print('MeanR2PnR = ' ,MeanR2PnR,', MeanR2PnS = ',MeanR2PnS)
#         #print(fileName[:2]+fileName[3:])
#         dtMean={
#                 'date':fileName[:-3],
#                 'Sensor':fileName[6:],
#                 'limit interval':limit_time_interval,
#                 'tot_segNum':tot_segNum,
#                 'R2_R&S':R2_RnS,
#                 'Mean_R2_P&R':MeanR2PnR,
#                 'Mean_R2_P&S':MeanR2PnS
#                 }
# 
#     
#     
# =============================================================================
    
    #print(res_df[[ label_time+"_end", label_value, "trend", "seg_id"]])
    return dtMean
    

if __name__ == '__main__':
    ''' USAGE '''
    
    fileName=getFileName(mypath)
 
    
    #===condition====
    wdlength=11# window length must odd ,wd_length >2N+1
    Ord=3
    pIndex=3
    diff=2 #  反應差
    limit_interval_percent= 0.02
    limit_r2=0.95
     
    #wd_length
    for w in range(wdlength,45,2):
        dirMean='Data_csv\\SWAB\\Mean\\PolyOrd\\'+str(Ord)+'\\PolyIndex\\'+str(pIndex)+'\\WD_Length\\'+str(w)
        mkfolder(dirMean)
        #print('wd Length: ',wd_length,'polyOrd: ',polyOrd)
        Meanheader=["date","Sensor","tot_segNum","R2_R&S","Mean_R2_P&R","Mean_R2_P&S"]
        #for i  in range(len(fileName)):
        count_T=0
        ltMean=[]
        for i  in range(0,len(fileName)):
            sensorType=fileName[i][6:-1]  
            if(sensorType=='T'):
                t=[]
                v=[]
                sgf=[]
                pltData=[]
                tot_segNum=0
                count_T+=1
                stop=False        
                print(fileName[i])
                input_df = pd.read_csv(mypath+fileName[i]+".csv", delimiter =",")
                ltMean.append(swab_alg(input_df,fileName[i], 
                                 max_error = 0.1, 
                                 window_size = 10,
                                 label_time = "timestamp",
                                 label_value = "value",
                                 unit_time = "s",
                                 plot_it = True,
                                 polyIndex=pIndex,
                                 wd_length=w,
                                 polyOrd=Ord
                                 ))
        dfpolyMeanDay=pd.DataFrame(ltMean,columns=Meanheader)
        print('wd Length: ',w,'polyOrd: ',Ord,'polyIndex:',pIndex,'window size:',10)
        MeanCsvfileName=dirMean+'\\2018_Mean_R2Data.csv'
        if(sensorType=='T'):
            dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
    # =============================================================================
    #         if (pth.isfile(MeanCsvfileName)!=True):  
    #            dfpolyMeanDay.to_csv(MeanCsvfileName,mode='w',index=None)
    #         else:
    #             dfpolyMeanDay.to_csv(MeanCsvfileName,mode='a',header=None,index=None)
    # =============================================================================
        print(dfpolyMeanDay)
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
        mean_segTol=round(numpy.mean(dfpolyMeanDay['tot_segNum']),3)
        allR2rns=round(numpy.mean(dfpolyMeanDay['R2_R&S']),3)
        allR2pns=round(numpy.mean(dfpolyMeanDay['Mean_R2_P&S']),3)
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
        
        tolMeanFile='Data_csv\\SWAB\\Mean\\AllMean.csv'
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
