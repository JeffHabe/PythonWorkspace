# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 04:07:44 2019

@author: Jeff PC
"""

from os import walk,makedirs
import csv 
import datetime
import folderTool as fT
import numpy as np 

mypath ='excelFolder\\'
def getFileName(mypath):
    for (dirpath, dirnames, filenames) in walk(mypath):
        file=list(filenames[i][:-4] for i in range(len(filenames)))
        break
    return file

if __name__ =='__main__':
    data={}
    v=[]
    t=[]
    pltt=[]
    rate=[]
    maxTime=0
    date=0
    cnt=0
    Snrtype='H1'
    test=[355]
    fileName=getFileName(mypath)
    for i in range(len(fileName)):#2018 DATA 0~117
        tmp=[]
        sensorType=fileName[i][6:] 
        #print(sensorType)
        if(sensorType=="H1"):
# =============================================================================
#         if(sensorType=="T1" or sensorType=="T2" or sensorType=="H1" or sensorType=="H2"):
# =============================================================================
            cnt+=1
            #print(sensorType)
            f = open(mypath+fileName[i]+'.csv', 'r')
            for row in csv.DictReader(f):
                ms=float(row['timestamp'])
                #pltDate=datetime.datetime.fromtimestamp(ms)
                date=datetime.datetime.fromtimestamp(ms)
                pltDate=datetime.datetime.utcfromtimestamp(ms)
                #print(date)
        # =============================================================================
        #         if(date.hour != 0)and ((date.hour)%2==0)and(date.minute>=0)and (date.minute<=15):
        #             data.append(random.randint(0,10))
        #             #print(str(date.hour)+':'+str(date.minute))  
        #         else:
        # =============================================================================
# =============================================================================
#                 if(float(row['value'])>=0 and float(row['value'])<=100):
#                     value=(float(row['value']))
#                 elif(float(row['value'])>100):
#                     value=(100.0)
#                 else:
#                     value=(0.0)
# =============================================================================
                tmp.append(ms)
                t.append(date)
                pltt.append(pltDate)
                v.append(float(row['value']))
            for k in range(len(tmp)-1):
                r=tmp[k+1]-tmp[k]
                rate.append(r)
            
            if(maxTime<=np.max(rate)):
                maxTime=np.max(rate)
                print(fileName[i])
                print('max time: ',np.max(rate))
                
            f.close()   
    data={'timestamp':t,
          'value':v,
          'rate':rate}
    
    #print(data)
    print()
    mean_rate=round(np.mean(data['rate']),3)
    mean_value=round(np.mean(data['value']),3)
    std=round(np.std(data['value']),3)
    print('sensor Type : ',Snrtype)
    print('# of file : ', cnt)
    print('# of data : ',len(data['value']))
    print('mean rate : ',mean_rate)
    print('max time: ',np.max(rate))
    print('min time: ',np.min(rate))
    print('max : ',np.max(data['value']))
    print('min : ',np.min(data['value']))
    print('mean : ',mean_value)
    print('std : ',std)
    from plotly.offline import plot
    import cufflinks as cf
    import plotly.graph_objs as go
    cf.go_offline()
    #plot.init_notebook_mode(connected=True)
    pltData = [
                go.Scatter(
                    x=pltt, # assign x as the dataframe column 'x'
                    y=v,
                    mode='lines',
                    marker=dict(
                            size=5,
                            color='rgba(255,0,0,1)'),
                    line=dict(width=1,)
                    )]
    strtitle=Snrtype+' Plot'
    #dcc.Graph(id=id, figure=figure, config=dict(showlink=True))
    layout=go.Layout(title=strtitle)
    filePath=".\Plot_html\\"
    fT.mkfolder(filePath)
    fig=go.Figure(data=pltData,layout=layout)
    #print(fileName)
    config = {'showlink': False, 'displaylogo':False, 'modeBarButtonsToRemove':['sendDataToCloud']}
    plot(fig,config=dict(showSendToCloud=True),filename=filePath+strtitle+".html")

