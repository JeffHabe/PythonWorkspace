# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 21:14:14 2018

@author: Jeff
"""
import numpy as np
#from numpy import * 
import csv 
from scipy.signal import savgol_filter
#from scipy.interpolate import *
#import scipy.interpolate as scInterpolate
#from scipy.interpolate import CubicSpline
#from scipy import interpolate
#matplotlib inline
import pandas as pd 
import cufflinks as cf
import plotly.graph_objs as go
from plotly.offline import plot
cf.go_offline()
t=[]
v=[]
data={}
sgf=[]
time=[]
stop=False
def readCSV():
    f = open('0201T3.csv', 'r')
    for row in csv.DictReader(f):
        data[row['時間']]=row['值']
    f.close()
def getData():
    i=0
    for key,value in data.items():
        t.append(i)
        time.append(key)
        v.append(float(value))
        i+=1
    global sgf
    sgf=savgol_filter(np.array(v),11,2)
# =============================================================================
#     dtRawData={
#             "Time":t,
#             "Value":v}
#     dfRD = pd.DataFrame(dtRawData)
#     dtSGFData={
#             "Time":t,
#             "Value":sgf}
#     dfSGFD = pd.DataFrame(dtSGFData)
# #    print(df)
# #   df.head()
#     pltData = [
#     go.Scatter(
#         x=dfRD['Time'], # assign x as the dataframe column 'x'
#         y=dfRD['Value'],
#         name='raw data'
#         ),
#     go.Scatter(        
#         x=dfSGFD['Time'], # assign x as the dataframe column 'x'
#         y=dfSGFD['Value'],
#         name='sgf data'
#         )]
#     plot(pltData)
# =============================================================================
    #plot({'data': [{'x':df['Time'],'y': df['Value']}],'layout': {'title': 'Test Plot','font': dict(size=16)}},image='png')
    #iplot([{'x':t,'y':v}])
    # IPython notebook
    # py.iplot(data, filename='pandas/basic-line-plot')
    #cs=cubic_spline(t,v)
    #print(len(cs[0]))
    #tck,u=interpolate.splprep([t,v],s=0.0)
    #x_i,y_i= interpolate.splev(u,tck)
  
    
    #csx_i,csy_i=cbspVal(t,cs)
    #printfx(cs)
    #plot(t,v,'o')
    #plot(t,sgf,'-')
    #plot(t,cs(t))
    
    #plot(t,csy_i)
    #.plot(t, v, 'b-',t,sgf, 'r--')
    #plt.legend(['data',  'sgf'], loc='best')

    
    #print(coeff_of_determination(array(v),y_i))
    #print(coeff_of_determination(array(v),csy_i))
    '''av=array(v)
    am=mean(av)
    print(am)
    a=[mean(av) for y in av]
    print(a)
    print(rsq(t,v,sgf))
    print(coeff_of_determination(array(v),sgf))
    '''

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

def squared_error(ys_orig,ys_line):
    return sum((ys_line-ys_orig)**2)

def coeff_of_determination(ys_orig, ys_line):
    y_mean_line = [np.mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig,ys_line)
    squared_error_y_mean = squared_error(ys_orig,y_mean_line)   
    return 1 - ( squared_error_regr / squared_error_y_mean)

def least_square(fuc,ys_orig,m,n,x):
    ys_line=np.polyval(fuc,x)
    err=squared_error(ys_orig,ys_line)
    lsq=err/(m-n-1)
    return lsq


def lab2():
    mkfile()
    startPt=0
    endPt=0
    delta=0
    d=0
    rsqSGF=0.0
    rsqTT=0.0
    '''
    plot(t,v,'-')
    plot(t,sgf,'-')
    '''
    #plt.plot(t,v,'-')
    #plt.plot(t,sgf,'-')
    print(len(t))
    d=int(len(t)/4)
    plyVal_Y=[]
    start=[]
    end=[]
    coefA_fun=[]
    coefB_fun=[]
    coefC_fun=[]
    R2_SGF=[]
    R2_Raw=[]
    Dlta=[]
    while(startPt<(len(t)-1)):
        x=[]
        y=[]
        vt=[]
        for i in range(startPt,d):
            if(i<(d-1)) and (i<(len(t)-1)) and (abs(sgf[startPt]-sgf[i])<=2):
                x.append(t[i])
                y.append(float(sgf[i]))
                vt.append(float(v[i]))  
            else:
                delta=i-startPt     
                endPt=i
                x.append(t[i])
                y.append(float(sgf[i]))
                vt.append(float(v[i]))
                break

        tp =np.polyfit(x,y,3)
        #f=np.poly1d(tp)
        ys_line=np.polyval(tp,x)
        rsqSGF=coeff_of_determination(np.array(y),ys_line)
        rsqTT=coeff_of_determination(np.array(vt),ys_line)
        if (rsqSGF>=0.89) or ((d-15)<=startPt) :    
# =============================================================================
#             
#             print(count,'.'," start : ",'{:>4d}'.format(startPt),"  end : ",endPt," polyStartValue : ",'%.2f' % round(ys_line[0], 2),\
#                   " orgStartValue : ",v[endPt], " sgfStartValue : ",'%.2f' % round(sgf[startPt], 2)) 
            
#             print( '%44s' %(" "),"polyEndValue :",'%.2f' % round(ys_line[delta],2),"orgEndValue : ",v[startPt],\
#                   "sgfEndValue : ",'%.2f' % round(sgf[startPt], 2))
#             print('%44s' %(" "),"Rsq(Orig) : ",'%.3f ' % round(rsqTT,3),"Rsq(SGF) : ",'%.3f ' % round(rsqSGF,3)) 
#             print('delta:',delta)
#             print()
#            
#             with open('pt.csv','a')as csvfile:
#                csvHeader=["start","end","polyStartValue","orgStartValue","polyEndValue","orgEndValue","Rsq","f(x)"]
#                writer=csv.DictWriter(csvfile,csvHeader)
#                writer.writerow({"start":startPt ,"end":endPt,"polyStartValue":ys_line[0],
#                                  "orgStartValue":v[endPt],"polyEndValue":ys_line[delta],"orgEndValue":v[startPt],"Rsq":rsqTT,"f(x)":tp})  
# =============================================================================
#             tp[0] = A  tp[1] = B tp[2] = C; Ax^2+Bx+C
            start.append(startPt)
            end.append(endPt)
            coefA_fun.append(tp[0])
            coefB_fun.append(tp[1])
            coefC_fun.append(tp[2])
            Dlta.append(delta)
            R2_Raw.append(round(rsqTT,3))
            R2_SGF.append(round(rsqSGF,3))   
            if(d>=len(t)/2):
                d=len(t)
            else:
                d=endPt+int((len(t)-delta)/2)
            startPt= endPt+1
                #print("round :",c)
            for k in range(0,len(ys_line)):
                plyVal_Y.append(ys_line[k])    
        else:
            d-=10

    dtPolyData={'start':start,
                'end':end,
                'A':coefA_fun,
                'B':coefB_fun,
                'C':coefC_fun,
                'Delta':Dlta,
                'R2_Raw':R2_Raw,
                'R2_SGF':R2_SGF
                }
    header=['start','end','A','B','C','Delta','R2_Raw','R2_SGF']
    dfpolyDtlData=pd.DataFrame(dtPolyData,columns=header)
    dfpolyDtlData.to_csv("0201T3DtlData.csv")
    print(dfpolyDtlData)
    print(round(coeff_of_determination(np.array(v),sgf),3))
    print(np.mean(R2_Raw))
    print(np.mean(R2_SGF))

    dtRawData={
            "Time":time,
            "Value":v}

    dtSGFData={
            "Time":time,
            "Value":sgf}

    dtPolyData={
            "Time":time,
            "Value":plyVal_Y}

#    print(df)
#   df.head()

    pltData = [
    go.Scatter(
        x=dtRawData['Time'], # assign x as the dataframe column 'x'
        y=dtRawData['Value'],
        name='raw data',
        mode='lines+markers',
        marker=dict(
                size=10,
                color='rgba(111,111,111,2)'),
                line=dict(
                        width=2,
                        color='rgba(111,111,111,2)')
        ),
    go.Scatter(        
        x=dtSGFData['Time'], # assign x as the dataframe column 'x'
        y=dtSGFData['Value'],
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
        x=dtPolyData['Time'], # assign x as the dataframe column 'x'
        y=dtPolyData['Value'],
        name='Poly data',
        mode='line',
        marker=dict(
                size=10,
                color='rgba(0,0,0,0)'),
                line=dict(
                        width=2,
                        color='rgba(0,255,255,8)')
        )]
    layout={'title': 'Test Plot',
                          'font': dict(size=16)}
    plot(pltData,layout,image='png',image_filename='Plot_image/ABC',filename='.\Plot_html\ABC')



readCSV()        
getData()
lab2()
