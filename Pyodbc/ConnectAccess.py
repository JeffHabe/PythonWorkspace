# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 06:59:06 2018

@author: Jeff PC
"""

import pypyodbc
import getFileDetail as getFD
import time
import makeData as mkData
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import win32com.client as win32
from PIL import Image
mypath ='D:/PythonWorkspace/excelFolder/'

class MysqlUtil():  
    def __init__(self):  
        pass  

    def getConnect(self):
        print ("Begin ACCESS ODBC connect.....")
        DBfile = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb'
        db = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir=D:/KengWoNCHUFile/AccessDB;DBQ='+DBfile)
        print("Successfully established connection....")
        return db

def SQLselect(TableName):
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()  
    tStart = time.time()
    cursor = db.cursor()
    SQL = 'select * from '+TableName+';'
    cursor.execute(SQL)
    for row in cursor.execute(SQL):                  # cursors are iterable
        print (row)
    tEnd = time.time()#計時結束
    timer=tEnd-tStart
    print(timer)
    db.commit
    cursor.close()

def SQLupdate(TableName):
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()
    
    cursor = db.cursor()
    SQLin ="""
    update SENSOR set sensor_name ='SMEC300' 
    where sensor_type='EC'
    """
    #t=[(dataCSV[1][0],str(dataCSV[1][1]),dataCSV[1][2]),(dataCSV[2][0],str(dataCSV[2][1]),dataCSV[2][2])]
    #print(t)
    try:
        tStart = time.time()#計時開始
        cursor.executemany(SQLin)
        db.commit()
        tEnd = time.time()#計時結束
    except Exception:
        pass
    finally:
        timer=tEnd-tStart
        db.close()  
    print(timer)
    return timer

def SQLselectwhere(TableName,p):
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    tStart = time.time()
    SQL = 'select '+ p +' from '+TableName+';'
    #cursor.execute(SQL)
    for row in cursor.execute(SQL):                  # cursors are iterable
        print (row)
    tEnd = time.time()#計時結束
    timer=tEnd-tStart
    print(timer)
    db.commit
    cursor.close()
    db.close()


def SQLsDatainsert(val):
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()
    
    cursor = db.cursor()
    SQLin ="""
    INSERT INTO Recording_data ([node_id],[sensor_id],[timestamp],[value]) 
    VALUES (?,?,?,?) 
    """
    #t=[(dataCSV[1][0],str(dataCSV[1][1]),dataCSV[1][2]),(dataCSV[2][0],str(dataCSV[2][1]),dataCSV[2][2])]
    #print(t)
    try:
        tStart = time.time()#計時開始
        cursor.executemany(SQLin,val)
        db.commit()
        tEnd = time.time()#計時結束
    except Exception:
        db.close()  
        pass
    finally:
        timer=tEnd-tStart
        db.close()  
    print('process time',round(timer,2))
    return timer

    
def SQLdelete():
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    SQLdel=""" 
    delete from Recording_data 
    """
# =============================================================================
#     SQLdel=""" 
#     delete from Recording_data 
#     where 
#     [timestamp_started]>=#2020/1/1 00:00:00# and [timestamp_started]<#2029/5/1 00:00:00#;
#     """
# =============================================================================
    cursor.execute(SQLdel)
    db.commit()
    cursor.close()
    db.close()  
    print('Delect successfully')


def Ploty():
    
    import  plotly
    from  plotly.graph_objsplotly.g  import Scatter, Layout
    plotly.offline.init_notebook_mode(connected=True)
    plotly.offline.iplot({
        "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
        "layout": Layout(title="hello world")
    })
    
def compactAccessDB():
    ##compact DB 
    srcDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb'
    destDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed_Test.accdb'
    oApp = win32.Dispatch('Access.Application')
    oApp.compactRepair(srcDB, destDB)
    print('...')
    time.sleep(0.01)
    os.remove(srcDB)
    time.sleep(0.01)
    print('...')
    oApp = win32.Dispatch('Access.Application')
    srcbkDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed_Test.accdb'
    destDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb'
    oApp.compactRepair(srcbkDB, destDB)
    time.sleep(0.01)
    print('...')
    os.remove(srcbkDB)
    time.sleep(0.01)
    print('...')
    oApp.Application.Quit()
    oApp = None 
    print('done Compaction')
    path = "D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb"
    if os.path.isfile(path):
        print('LFSDBdata_double exist ')
    
def get_FileSize():
    filePath = "D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb"
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)    
    
if __name__=="__main__":
     # print 
    fileName=getFD.getFileName(mypath)
    #print(fileName)
    
    # if print row it will return tuple of all fields
    #use below conn if using with Access 2007, 2010 .accdb file
    #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
    #SQLselect('SENSOR_DATA','[sensor_type]')

  
    
   #Delete 
    SQLdelete()
    compactAccessDB()
    print()
    
#     compactAccessDB()
# =============================================================================
    
# =============================================================================
#  ##Insert Into test sensor data for test limited db capacity 
#     usetime=[] 
#     startYear=2018
#     startDay=1
#     startMth=1
#     stDate=dt.datetime(startYear,startMth,startDay).date().strftime("%m-%d")
#     for day in range(startDay,startDay+1):    
#         date=mkData.add1DpS(yr=startYear,mth=startMth,d=day)
#         value=mkData.f(date)
#         print(date[0])
#         data=[]      
#         for sensor_id in range(1,8):
#             for node_id in range(1,17):               
#                 for i in range(len(date)):
#                     #print(len(value))    
#                     t=(node_id,sensor_id,date[i],value[i])
#                     #print(t)
#                     data.append(t)
#                 #print(data[0][:2],'-',data[len(data)-1][:2])
#         try:
#             thisDate=(dt.datetime.fromtimestamp(date[0].timestamp()-86400))
#             edDate=thisDate.date().strftime("%m-%d")
#             usetime.append(SQLsDatainsert(data))
#         except Exception:
#             break
#     rawfilesize=get_FileSize()
#     compactAccessDB()
#     compfilesize=get_FileSize()
#     print('Mean: ',round(np.mean(usetime),2),'輸入完大小',rawfilesize,'壓縮後大小',compfilesize)
#     record=[{'time':round(np.mean(usetime),2),
#               'start_Date':stDate,
#               'end_Date':edDate,
#               'Compact Size':compfilesize}]
#     print("record",record)
#     df=pd.DataFrame(record,index=None)   
#     df.to_csv('Insertinto_detailData.csv',mode='a',columns=['time','start_Date','end_Date','Compact Size'],index=False)
#         #finally:
#             #pd.DataFrame(dictTime).to_csv('Insertinto_spend_Time.csv',mode='a',header=None)        
#   
# =============================================================================
    
    

    

# =============================================================================
# ##查詢結果
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()
#     SQL="""
#     select distinct date_started,f.field_id,location,plant_name
#     from [Sowing] as s , [FIELD] as f , [PLANT] as p
#     where  s.plant_id= 1 and date_started = #2018-09-19# 
#     """            
#     tStart = time.time()#計時開始
#     data=[]
#     timestamp=[]      
#     print ('(','date_started',' ','field_id',' ','location','  plant_name',')')
#     for row in cursor.execute(SQL):                  # cursors are iterable
#         print(row)
#         #print ('(',dt.datetime.date(row[0]),'    ',row[1],'       ',row[2],'   ',row[3],')')
#         #data.append(float(row[0]))
#         #timestamp.append(row[1])
#     cursor.commit()
#     #print(data)
#     cursor.close()
#     db.close()
#     tEnd = time.time()#計時結束
#     timer=tEnd-tStart
# # =============================================================================
# #     fig,ax1=plt.subplots()
# #     ax2=ax1.twinx()
# #     ax1.plot(timestamp,data,'r-')
# #     plt.gcf().autofmt_xdate()
# #     plt.show()
# # =============================================================================
#     print('執行時間：',timer,'。data 總數 ',len(data))
# 
# =============================================================================




 
# =============================================================================
#     ##比對原始數據與資料庫數據
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()
#     SQL="""
#     select value, timestamp
#     from recording_data
#     where [timestamp] >= #2018/1/1 00:00:00# and
#     [timestamp] <= #2018/1/2 00:00:00# and 
#     [node_id] = 1 and 
#     [sensor_id] = 2
#     """
# # =============================================================================
# # 
# #     SQL = """select value , timestamp
# #          from recording_data 
# #          where [timestamp] >= #2019/3/29 00:00:00# and
# #          [timestamp] <= #2019/4/ 00:00:00# 
# # 
# #         """        
# # =============================================================================
#          #insertinto Test for LFSDBdata_doubleBK
#     tStart = time.time()#計時開始
#     data=[]
#     timestamp=[]      
#     for row in cursor.execute(SQL):                  # cursors are iterable
#         #print (row[0])
#         data.append(float(row[0]))
#         timestamp.append(row[1])
#    # print(data)
#     cursor.commit()
#     #print(data)
#     cursor.close()
#     db.close()
#     tEnd = time.time()#計時結束
#     timer=tEnd-tStart
#     df={'timestampe':timestamp,
#         'data':data}
#     fileNum=0
#     dataCSV=getFD.readCSV(fileName[fileNum])
#     #print(dataCSV)
#     sum=0
#     pltData=[]
#     for i in range(len(dataCSV)):
#         pltData.append(dataCSV[i][3])
#         if(data[i]==dataCSV[i][3]):
#             sum+=1
#     
#     print('準確率:',(sum/len(dataCSV))*100)              
#  
#     fig,ax1=plt.subplots()
#     #ax2=ax1.twinx()
#     ax1.plot(timestamp,data,'r-')
#     ax1.set_xlabel('time')
#     ax1.set_ylabel('db data value', color='r')
#     plt.gcf().autofmt_xdate()
#     plt.savefig('testplot1.pdf')
#     #Image.open('testplot1.png').save('testplot1.jpg','JPEG')
#     
#     fig,ax2=plt.subplots()
#     ax2.plot(timestamp,pltData,'g')
#     ax2.set_ylabel('raw data value', color='g')
#     ax2.set_xlabel('time')
#     plt.gcf().autofmt_xdate()
#     plt.savefig('testplot2.pdf')
#     
#     fig,ax3=plt.subplots()
#     ax4=ax3.twinx()
#     #fig,ax2=plt.subplots()
#     ax3.plot(timestamp,data,'r-')
#     ax4.plot(timestamp,pltData,'g:')
#     ax3.set_xlabel('time')
#     ax3.set_ylabel('db data value', color='r')
#     ax4.set_ylabel('raw data value', color='g')
#     plt.gcf().autofmt_xdate()
#     #plt.show()
#     plt.savefig('testplot3.pdf')
#     print('執行時間：',timer,'。data 總數 ',len(data))
#     print()
#     
# =============================================================================
    
# =============================================================================
#  
# #==========一般Select================================================#   
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()
# # =============================================================================
# #     SQL="""
# #     select DISTINCT location , plant_name , date_started, date_ended
# #     from Sowing as s  , PLANT as p , FIELD as f
# #     where plant_name like '小%' and f.field_id like 'A';
# #     """    
# # =============================================================================
# 
#     SQL="""
#     select DISTINCT location , p.plant_name , p.fertilizer,s.sowing_date, s.harvest_date
#     from  PLANT as p , Sowing as s, FIELD as f , FIELDWORK as fw
#     where f.field_id='f001'and p.plant_id=s.plant_id  and s.field_id=f.field_id and fw.field_id=s.field_id
#     """         
#     SQL5="""
#     SELECT PLANT.plant_name, FIELD.location, Sowing.sowing_date, Sowing.harvest_date, Sowing.output, Sowing.price, [price]*[output]*1.6 AS 總售價
#     FROM FIELD INNER JOIN (PLANT INNER JOIN Sowing ON PLANT.[plant_id] = Sowing.[plant_id])
#     ON FIELD.[field_id] = Sowing.[field_id]
#     WHERE Sowing.[harvest_date]=>#2018/9/1# and Sowing.[harvest_date]<=#2018/10/30#;
#     """  
#     SQL15="""
#     SELECT p.plant_name, f.location, s.sowing_date, s.harvest_date, s.output, s.price, round([price]*[output]*1.6,2)AS 總售價
#     FROM FIELD as f,PLANT as p, Sowing as s
#     WHERE f.field_id=s.field_id and p.plant_id=s.plant_id and s.harvest_date>=#2018/9/1# and s.harvest_date<=#2018/10/30# 
#     ORDER BY p.plant_name ASC;
#     """  
#     
#     SQL6="""
#     SELECT round(avg(s.output),2) as 平均產量,Round(avg(s.price),2)  as 平均售價
#     FROM FIELD as f,PLANT as p, Sowing as s
#     WHERE f.field_id=s.field_id and p.plant_id=s.plant_id and s.harvest_date>=#2018/9/1# and s.harvest_date<=#2018/10/30# 
#     ;
#     """  
#     tStart = time.time()#計時開始
# 
#     timestamp=[]      
#     datalst=()
# # =============================================================================
# #     for row in cursor.execute(SQL):  # cursors are iterable
# #         #print(len(row))
# #         #print(row)
# #         cnt=0
# #         data=()
# #         for cnt in range(len(row)):
# #             if(cnt>2 and row[cnt]!=None ):
# #                 data=data+((row[cnt]).strftime("%Y/%m/%d"),)
# #             else:
# #                 data=data+(row[cnt],)
# #         datalst=datalst+(data,)
# # 
# #     print(datalst)
# # =============================================================================
#     
#     cursor.execute(SQL15)
#     result_set = cursor.fetchall()
#     results = {}
#     column = 0
# # =============================================================================
# #     for d in cursor.description:
# #         results[d[0]] = column
# #         column = column + 1
# #     print(results)
# # =============================================================================
#     field_name = [field[0] for field in cursor.description]
#     for f_n in range(len(field_name)):     
#         print(field_name[f_n],'  ', end='')
#     print()
#     for row in result_set:
#         #print(row)
#         data=()
#         for cnt in range(len(row)):
#             if(cnt>=2 and cnt<=3):
#                 data=data+((row[cnt]).strftime("%Y/%m/%d"),)
#             else:
#                 data=data+(row[cnt],)
#         print("      ".join(str(i) for i in data)) 
# # =============================================================================
# #         datalst=datalst+(data,)
# # 
# #     print(datalst)
# # =============================================================================
# # =============================================================================
# #         print ('(',row[0],row[1],row[2],row[3],
# #                  row[4],row[5],row[6],row[7],row[8],row[9],row[10],')')
# # =============================================================================
#     print()
#     cursor.commit()
#     #print(data)
#     cursor.close()
#     db.close()
#     tEnd = time.time()#計時結束
#     timer=tEnd-tStart
#     
#     print('執行時間：',timer,'。data 總數 ',len(result_set))
#     print()
#     
#     
#     
# =============================================================================
    
    
    ## Update 
# =============================================================================
#     TableName='SENSOR'
#     SQLselect(TableName)
#     print()
#     SQLupdate(TableName)
#     SQLselect(TableName)
# =============================================================================
    
    

    
    
   
    
    
    
    
    
    
    
    
# ========================================================
#     for i in range(len(fileName)):
#         dataCSV=getFD.readCSV(fileName[i])
#         SQLsDatainsert(dataCSV)
#         print("Successfully ",fileName[i],"times Insert Into")
#     #print(str(dataCSV[0][1]))
# =============================================================================
            
            
    ## all sensor data file insert into DB 
# =============================================================================
#     for i in range(len(fileName)):
#          dataCSV=getFD.readCSV(fileName[i])
#          #print(str(dataCSV[0][1]))
#          print(dataCSV[0])
#          #SQLsDatainsert(dataCSV)
#          print("Successfully ",fileName[i],"times Insert Into")
# =============================================================================
    
# =============================================================================
#    ##儲存原始感測數據(excel to db) 
#     fileNum=0
#     dataCSV=getFD.readCSV(fileName[fileNum])
#     print(fileName[fileNum],':',dataCSV[0])
#     SQLsDatainsert(dataCSV)
#     print("Successfully Insert Into")
#     
# =============================================================================
    