# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:27:49 2018

@author: Jeff PC
"""

import pandas as pd
import itertools as itetls
import numpy as np
from openpyxl import load_workbook
#2018/1/1 
start_day=1514764800
Sec_perday=86400
Sec_perMth=2678400
def get_sec(time_str,mth,d):
    h, m, s = str(time_str).split(':')
    month=(Sec_perMth)*(mth-1)
    day=(Sec_perday)*(d-1)
    time=int(start_day) + month + day + int(h) * 3600 + int(m) * 60 + int(s)
    #print(time)
    return time

# Assign spreadsheet filename to `file`
#file = 'excelFolder\\RawData\\2018 LFS Sensor Data.xlsx'
file = 'excelFolder\\RawData\\TestDelay.xlsx'
wb=load_workbook(file)
sheetName=[]
for i in range(len(wb.worksheets)):
#print(len(wb.worksheets))
    sheet=wb.worksheets[i]
# =============================================================================
# print(wb.worksheets[1].title)
# print(list(wb.worksheets[1].values))
# sheet = wb.get_sheet_by_name('01-02')
# =============================================================================    
    data = sheet.values
    #print(list(data))
    #print(next(data)[0:])
    cols = next(data)[0:] 
    data=list(data)
    #print(len(cols))
    month=int(sheet.title[:2])
    #print(month)
    day=int(sheet.title[3:5])
    #print(month)
    #print(len(data[0]))
    idx=[r[0]for r in data]
    data = (itetls.islice(r, 0, None,2) for r in data)
    #print(cols)
    if(len(cols)>=10):
        df=pd.DataFrame(data,columns=['時間','H1','H2','H3','T1','T2','T3'])
    elif(len(cols)<=3):
        df=pd.DataFrame(data,columns=['時間','Value'])
    else:
        df=pd.DataFrame(data,columns=['時間','H1','H2','T1','T2'])
    #print(df.shape[1])
    filePath='excelFolder/'
    times=[]
    for j in range(1,df.shape[1]):
        print( sheet.title+'_'+df.columns[j]+' start')
        fileName=filePath+ sheet.title+"_"+df.columns[j] +".csv"

        times=[get_sec(t,month,day) for t in df['時間']]
        first=True
        newtimesTop=[]
        newtimesBottom=[]
        oldtime=times
        Mid_StartPt=0
        Mid_EndPt=len(times)
        for k in range(len(times)):
            if (times[k-1] > times[k])and (first==True):
                newtimesTop=[(times[l]-43200) for l in range(0,k)]
                Mid_StartPt=k
                first=False
                newstart=k
            elif(times[k-1] > times[k])and(first==False):
                newtimesBottom=[(times[l]+43200)for l in range(k,len(times))]
                Mid_EndPt=k
                break
        if not first:
            newtimesMid=[times[l]for l in range(Mid_StartPt,Mid_EndPt)]
            times=newtimesTop+newtimesMid+newtimesBottom
        #print(times)
        dictCsv={'timestamp':times,
                 'value':df[df.columns[j]]}