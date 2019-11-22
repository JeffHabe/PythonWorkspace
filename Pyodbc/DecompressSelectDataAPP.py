# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 19:43:31 2019

@author: Jeff PC
"""
    

from os import walk
import ConnectAccess as CAcss
import time
import datetime as dt
from datetime import datetime
import numpy as np
import csv
from numpy.polynomial import chebyshev as chy
import math
import folderTool as fT
import CompressAlgorithm as CA
import pandas as pd
def compare_listcomp(x, y):
    return [i for i, j in zip(x, y) if i == j]


def sqlselect(datestart,dateend,c_id):
    ##查詢結果
    sqlUtil=CAcss.MysqlUtil()
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    SQL="""
    select *
    from Record
    where [timestamp_started]>#"""+datestart+"""# and
    [timestamp_started]< #"""+dateend+"""# and
    conn_id='"""+c_id+"""'
    """            
    #where [timestamp_started]>= #2028/12/29 00:00:00# and 
    #[timestamp_started]< #2029/1/30 00:00:00#
    tStart = time.time()#計時開始
    data=[]     
    for row in cursor.execute(SQL):                  # cursors are iterable
        data.append(row)
        #print(row)
        
    cursor.commit()
    #print(data)
    cursor.close()
    db.close()
    tEnd = time.time()#計時結束
    timer=tEnd-tStart
    
    print('執行時間：',timer,'。data 總數 ',len(data))
    return data

if __name__=="__main__":
    
    import traceback
    from plotly.offline import plot
    import plotly.graph_objs as go
    sqlUtil=CAcss.MysqlUtil()
    
    
    
##查詢結果
    strdate=str(dt.datetime.utcfromtimestamp(1514764800))
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    SQL="""
    select DISTINCT rec_id ,c.conn_id,s.sensor_id,f.location ,timestamp_started  ,timestamp_ended ,delta ,coeff_0 ,coeff_1,coeff_2,coeff_3,coeff_4,coeff_5   
    from Record as r,Connect as c, FIELD as f,NODE as n,node_deployed as nd  ,SENSOR as s        
    where [timestamp_started]>= #2018/1/1 00:00:00 # and 
    [timestamp_started]< #2018/1/31 00:00:00# and 
    c.conn_id=r.conn_id and 
    c.sensor_id='S002' and 
    c.sensor_id=s.sensor_id and
    c.node_id= 'Nd001' and 
    c.node_id=n.node_id and 
    f.field_id='F001' and 
    f.field_id=nd.field_id
    """ 
    tStart = time.time()#計時開始
    data=[]
    timestamp=[] 
    cursor.execute(SQL)
    result_set = cursor.fetchall()
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1
    #print(results)
    field_name = [field[0] for field in cursor.description]
    #for f_n in range(len(field_name)):     
        #print(field_name[f_n],' ', end='')
    #print()
# =============================================================================
#     for row in result_set:
#         print ('(',row[0],row[1],row[2],row[3],
#                  row[4],row[5],row[6],row[7],row[8],row[9],row[10],')')
#     print()
# =============================================================================
    for row in cursor.execute(SQL):                  # cursors are iterable
        data.append(row)
        ptData=()
        for cnt in range(len(row)):
            if(cnt>=4 and cnt<=5):
                ptData=ptData+((row[cnt]).strftime("%Y/%m/%d %H:%M:%S"),)
            elif(cnt>=7):
                rdRow=round(row[cnt],3)
                ptData = ptData + ((rdRow),)
            else:
                ptData=ptData+(row[cnt],)
        print("    ".join(str(i) for i in ptData))
        
    cursor.commit()
    #print(data)
    cursor.close()
    db.close()
    tEnd = time.time()#計時結束    
    timer=tEnd-tStart
    #print('執行時間：',timer,'。data 總數 ',len(data))


    dateStart='2018/12/27 '
    dateEnd='2018/12/28 '
    c_id='C001'
    #print(dateStart,'-',dateEnd)
    #data=sqlselect(dateStart,dateEnd,c_id)
    #print(len(data))


#解壓縮查詢結果
    #print(data)
    pltData=[]
    sumX=0
    allX=[]
    dbData=[]
    dbDate=[]
    coeffDBAll=[]
    startDate=data[0][4].strftime('%Y-%m-%d')
    endDate=data[len(data)-1][4].strftime('%Y-%m-%d')
    print(startDate,' - ',endDate)
    print('Decompressing Data From DB')
    for t in range(len(data)):
        x=[]
        datetime_start = data[t][4]
        datetime_end = data[t][5]

        timedelta=((datetime_end-datetime_start)/data[t][6])
        #print(data[t][4])
        datetime_ary=[]
        #datetime_ary.append(datetime_start.strftime('%Y-%m-%d %H:%M:%S'))
        coeffDB=[]
        #print(datetime_start,'-',datetime_end)
        #print(type(data[t][4]))
        
        #接下For 作用為將分段轉換成原始數據時間序
        for i in range(data[t][6]):
            idx=sumX+i
            allX.append(idx)
            x.append(idx)
            datetime_ary.append((datetime_start+timedelta*(i)).strftime('%Y-%m-%d %H:%M:%S'))
            #print(datetime_ary[i])
        
        sumX+=data[t][6]
        #print(x)
        #print(data[t][5])
        
        #以下For 作用為將壓縮數據的多項式系數載入於LIST ，再將List放入Chebval 轉譯為數據序
        n=6 ## n 是多項式系數的個數
        for i in range(len(data[t])-1,n,-1):
            coeffDB.append(data[t][i])
        coeffDBAll.extend(coeffDB)
        #print(coeffRaw)
        #print(np.poly1d(coeffRaw))
        try:
            ys_lineDB=chy.chebval(x,coeffDB)   
            
            #print(ys_lineDB)
        
        except:
            #print(coeffRaw)
            traceback.print_exc()  
        dbData.extend(ys_lineDB)
        dbDate.extend(datetime_ary)
        #print(datetime_end.hour,":",datetime_end.minute,data[t][6])
# =============================================================================
#         if(datetime_end.hour>=23 and datetime_end.minute>58 and datetime_end.second>55):
#            print(datetime_end.hour,":",datetime_end.minute,data[t][6])
#            sumX=0
# =============================================================================
        if(t!=len(data)-1):
            if(data[t][4].day < data[t+1][4].day):
               print(datetime_end.hour,":",datetime_end.minute,data[t][6])
               sumX=0
        #print(type(coeffRaw[0]))
        #print(len(x))
        #print(len(dbDate),':',len(dbData))
# =============================================================================
#         for i in range(int(len(datetime_ary)*0.95),(len(datetime_ary))-1):
#                 print(datetime_ary[i],":",round(ys_lineDB[i],3))
# =============================================================================
        isOpen=True      
# =============================================================================
#         isOpen=True
#         pltData +=[
#         go.Scatter(
#             x=datetime_ary, # assign x as the dataframe column 'x'
#             y=ys_lineDB,
#             mode='lines',
#             marker=dict(
#                     size=5,
#                     color='rgba(255,0,0,0.9)'
#                     )
#             )]
# =============================================================================
       
    pltData =[
    go.Scatter(
            x=dbDate, # assign x as the dataframe column 'x'
            y=dbData,
            mode='lines',
            marker=dict(
                    size=5,
                    color='rgba(255,0,0,0.9)'
                    )
            )]
    #print(len(dbDate),':',len(dbData))
    #print(dbDate)
    strtitle= startDate+'~'+endDate+ '的趨勢'
    layout=go.Layout(title=strtitle)
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    fig=go.Figure(data=pltData,layout=layout)
    plot(fig,filename="test.html",auto_open=isOpen)

    print("當天最小值：",round(min(dbData),2))
    print("當天最大值：",round(100.0,2))
    print("當天平均值：",round(np.mean(dbData),2))