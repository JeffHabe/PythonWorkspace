# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 03:29:09 2019

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
    
    def get_FileSize(self):
        filePath = "D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb"
        fsize = os.path.getsize(filePath)
        fsize = fsize/float(1024*1024)
        return round(fsize,2) 
    
    def compactAccessDB(self):
        ##compact DB 
        srcDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb'
        destDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_CompressedTest.accdb'
        oApp = win32.Dispatch('Access.Application')
        oApp.compactRepair(srcDB, destDB)
        print('...')
        time.sleep(0.01)
        os.remove(srcDB)
        time.sleep(0.01)
        print('...')
        oApp = win32.Dispatch('Access.Application')
        srcbkDB = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_CompressedTest.accdb'
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
            print('LFSDBdata_Compressed exist ') 
        return 0

    

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
    update SENSOR set sensor_name ='Analog EC Meter SKU DFR0300' 
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
    delete from Record
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
    
def SQLdeleteRow(TableName,whereStr):
    sqlUtil=MysqlUtil()
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    SQLdel = 'delete  from '+TableName+' where '+whereStr+';'
    print(SQLdel)
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
    
def IDstr(num):
    if(num < 10):
        strNum="00"+str(num)
    elif(num>=10 and num<=99):
        strNum="0"+str(num)
    else:
        strNum=str(num)
    return strNum


if __name__=="__main__":
     # print 
    #print(fileName)
    
    # if print row it will return tuple of all fields
    #use below conn if using with Access 2007, 2010 .accdb file
    #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
    #SQLselect('SENSOR_DATA','[sensor_type]')

# =============================================================================
#     sqlUtil=MysqlUtil()
#     TableName="Record"
#     whereSTR="[conn_id] = 'C016'"
#     #SQLselect(TableName)
#     SQLdeleteRow(TableName,whereSTR)
#     sqlUtil.compactAccessDB()
#     print()  
#     #SQLselect(TableName)
#     
# =============================================================================
    
    
    #Delete 
    sqlUtil=MysqlUtil()
    SQLdelete()
    sqlUtil.compactAccessDB()
    print()
    


    
 ##Insert Into Connect Id
# =============================================================================
#      cid=25 #start num of conn_id
#      for n_cnt in range(4,10):
#         for i in range(1,9):
#             sqlUtil=MysqlUtil()
#             db = sqlUtil.getConnect()
#             cursor = db.cursor()
#             SQLin ="""
#             INSERT INTO Connect ([conn_id],[node_id],[sensor_id]) 
#             VALUES (?,?,?) 
#             SELECT '111', '100' FROM DUAL WHERE NOT EXISTS(SELECT cardno FROM card WHERE cardno = '111');
#             """
#             #t=[(dataCSV[1][0],str(dataCSV[1][1]),dataCSV[1][2]),(dataCSV[2][0],str(dataCSV[2][1]),dataCSV[2][2])]
#             #print(t)
#             C_id="C"+IDstr(cid)
#             N_id="Nd"+IDstr(n_cnt)
#             S_id="S"+IDstr(i)
#             print("C =",C_id," N = ",N_id," S = ",S_id)
#             data=[]
#             data.append((C_id,N_id,S_id))
#             cursor.executemany(SQLin,data)
#             db.commit()
#             db.close()
#             cid+=1
#         cid+=1
# =============================================================================
        
# =============================================================================
#   ##Insert Into Node Id
#      for i in range(6,10):
#         sqlUtil=MysqlUtil()
#         db = sqlUtil.getConnect()
#         cursor = db.cursor()
#         SQLin ="""
#         INSERT INTO NODE ([node_id],[Hardware_id],[IPAddress],[MAC],[num_sensor],[communication],[analog_bit],[node_Other]) 
#         VALUES (?,?,?,?,?,?,?,?) 
#         """
#         #t=[(dataCSV[1][0],str(dataCSV[1][1]),dataCSV[1][2]),(dataCSV[2][0],str(dataCSV[2][1]),dataCSV[2][2])]
#         #print(t)
# 
#         N_id="Nd"+IDstr(i)
#         H_id="H"+IDstr(str(1))
#         IPAdr="192.168.124."+str(i)
#         MAC="ff:ff:ff:ff:ff:ff"
#         n_s=7
#         commun="Line"
#         a_bit=8
#         n_Other=""
#         
#         data=[]
#         data.append((N_id,H_id,IPAdr,MAC,n_s,commun,a_bit,n_Other))
#         cursor.executemany(SQLin,data)
#         db.commit()
#         db.close()
# =============================================================================

    
# =============================================================================
#     ## Update 
#     TableName='SENSOR'
#     SQLselect(TableName)
#     print()
#     SQLupdate(TableName)
#     SQLselect(TableName)
# =============================================================================


# =============================================================================
# 
# 
# ##查詢結果
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()     
#     SQL="""
#     select distinct sowing_date,f.field_id,location,p.plant_name
#     from [Sowing] as s , [FIELD] as f , [PLANT] as p 
#     where p.plant_id= s.plant_id and f.field_id=s.field_id and p.plant_name= '小白菜' and sowing_date = #2018-09-19#
#     """  
#     
#     SQL1="""
#     select *
#     from  [PLANT] as p 
#     where p.season= '秋季'
#     """  
#     SQL2="""
#     select distinct s.sowing_date, f.field_id, f.location, p.plant_name, fw.FW_TypeID ,fwT.FW_Type, fw.FW_started, fw.FW_ended
#     from  [Sowing] as s ,  [FIELDWORK] as fw ,  [FWType]as fwT , [PLANT] as p  , [FIELD] as f
#     where f.location = 'L1000' and s.sowing_date=#2018/9/1# 
#     and  p.plant_id= s.plant_id and f.field_id=s.field_id and fw.FW_TypeID=FwT.FW_TypeID
#     """  
#     SQL3="""
#     SELECT  distinct re.error_date,f.field_id,f.location,re.node_id,e.error_id,e.message
#     FROM [NODE] as n, [FIELD] as f, [node_deployed]as nd, [ERROR] as e, [Recording_error] as re
#     WHERE re.node_id='Nd002' and re.node_id = n.node_id and n.node_id=nd.node_id and f.field_id=nd.field_id and  e.error_id=re.error_id 
#     """
#     
#     tStart = time.time()#計時開始
#     data=[]
#     timestamp=[]      
#     #print ('(','date_started',' ','field_id',' ','location','  plant_name',')')
#     cursor.execute(SQL3)
#     result_set = cursor.fetchall()
#     results = {}
#     column = 0
#     for d in cursor.description:
#         results[d[0]] = column
#         column = column + 1
#     #print(results)
#     field_name = [field[0] for field in cursor.description]
#     for f_n in field_name:
#         print('  ',f_n,'  ', end='')
#     print()
#     for row in result_set:
#         for r in row:
#             print(r,'       ',end='' )
#         print()
# # =============================================================================
# #     for row in result_set:
# #         print ('(',dt.datetime.date(row[0]),'    ',row[1],'       ',row[2],'   ',row[3],')')
# # # =============================================================================
# # =============================================================================
# #     for row in cursor.execute(SQL):                  # cursors are iterable
# #         print ('(',dt.datetime.date(row[0]),'    ',row[1],'       ',row[2],'   ',row[3],')')
# #         #data.append(float(row[0]))
# # =============================================================================
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
# 
# ##查詢壓縮數據結果
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()
#     SQL="""
#     select *
#     from Record            
#     where [timestamp_started]>= #2019/06/24 00:00:00# and 
#     [timestamp_started]< #2019/06/24 12:00:00#
#     and C001
#     """ 
#     tStart = time.time()#計時開始
#     data=[]
#     timestamp=[] 
#     cursor.execute(SQL)
#     result_set = cursor.fetchall()
#     results = {}
#     column = 0
#     for d in cursor.description:
#         results[d[0]] = column
#         column = column + 1
#     field_name = [field[0] for field in cursor.description]
#     for f_n in field_name:
#         print('  ',f_n,'  ', end='')
#     print()    
#     for row in result_set:                  # cursors are iterable
#         data.append(row)
#         print ('(',row[0],row[1],row[2],row[3],
#                  row[4],row[5],row[6],row[7],row[8],row[9],row[10],')')
#         
#     cursor.commit()
#     #print(data)
#     cursor.close()
#     db.close()
#     tEnd = time.time()#計時結束    
#     timer=tEnd-tStart
#     print('執行時間：',timer,'。data 總數 ',len(data))
# 
# 
# 
# 
# =============================================================================
