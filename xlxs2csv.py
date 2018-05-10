# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:08:28 2018

@author: Jeff
"""

import pandas as pd
import itertools as itetls
import numpy as np
from openpyxl import load_workbook

def get_sec(time_str):
    h, m, s = str(time_str).split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# Assign spreadsheet filename to `file`
file = 'excelFolder\\RawData\\2018 LFS Sensor Data.xlsx'
wb=load_workbook(file)
sheetName=[]
#print(len(wb.worksheets))
for i in range(len(wb.worksheets)):
    sheet=wb.worksheets[i]
# =============================================================================
# print(wb.worksheets[1].title)
# print(list(wb.worksheets[1].values))
# sheet = wb.get_sheet_by_name('01-02')
# =============================================================================    
    data = sheet.values
    #print(list(data))
    cols = next(data)[0:]
    data=list(data)
    #print(len(cols))
    #print(len(data[0]))
    idx=[r[0]for r in data]
    data = (itetls.islice(r, 0, None,2) for r in data)
    if(len(cols)>9):
        df=pd.DataFrame(data,columns=['時間','H1','H2','H3','T1','T2','T3'])
    else:
        df=pd.DataFrame(data,columns=['時間','H1','H2','T1','T2'])
    #print(df.shape[1])
    filePath='excelFolder/'
    times=[]
    for i in range(1,df.shape[1]):
        print( sheet.title+'_'+df.columns[i]+' start')
        fileName=filePath+ sheet.title+"_"+df.columns[i] +".csv"  
        times=[get_sec(t) for t in df['時間']]
        first=True
        newtimesTop=[]
        newtimesBottom=[]
        oldtime=times
        Mid_StartPt=0
        Mid_EndPt=len(times)
        for j in range(len(times)-1):
            if (times[j-1] > times[j])and (first==True):
                newtimesTop=[(times[k]-43200) for k in range(0,j)]
                Mid_StartPt=j
                first=False
                newstart=j
            elif(times[j-1] > times[j])and(first==False):
                newtimesBottom=[(times[k]+43200)for k in range(j,len(times))]
                Mid_EndPt=j
                break
        if not first:
            newtimesMid=[times[k]for k in range(Mid_StartPt,Mid_EndPt)]
            times=newtimesTop+newtimesMid+newtimesBottom
        #print(times)
        dictCsv={'timestamp':times,
                 'value':df[df.columns[i]]}
        #print(dictCsv)
        dfToCsv=pd.DataFrame(dictCsv,columns=['timestamp','value'])
        #print(dfToCsv)
        dfToCsv.to_csv(fileName,index=None,mode='w')
        print( sheet.title+'_'+df.columns[i]+' done')
#print(fileName)
#print(df[df.columns[3]])
