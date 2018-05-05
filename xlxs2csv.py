# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:08:28 2018

@author: Jeff
"""

import pandas as pd
import itertools as itetls
from openpyxl import load_workbook

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
    
    for i in range(1,df.shape[1]):
        fileName=filePath+ sheet.title+"_"+df.columns[i] +".csv"    
        dictCsv={'時間':df['時間'],
                 '值':df[df.columns[i]]}
        #print(dictCsv)
        dfToCsv=pd.DataFrame(dictCsv,columns=['時間','值'])
        #print(dfToCsv)
        dfToCsv.to_csv(fileName,index=False,mode='w')
        print( sheet.title+'_'+df.columns[i]+' done')
#print(fileName)
#print(df[df.columns[3]])
