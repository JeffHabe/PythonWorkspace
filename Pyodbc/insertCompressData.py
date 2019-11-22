# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:48:45 2018

@author: Jeff PC
"""
from os import walk
import csv
import os.path as pth 
import time
import pypyodbc
import datetime as dt
from datetime import datetime
import numpy as np
import os
import pandas as pd
import win32com.client as win32
#from os.path import isfile,join 
mypath ='D:\PythonWorkspace\PyExp\Data_csv\SlidingWindow\Chebyshev\Mean\Worst compressing data2019'
# =============================================================================
# onlyfiles=[f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
# =============================================================================
t={'index':'date'}
n=0
start_day=1514764800
Sec_perday=86400

class MysqlUtil():  
    def __init__(self):  
        pass  

    def getConnect(self):
        #print ("Begin ACCESS ODBC connect.....")
        DBfile = 'D:\\PythonWorkspace\\Pyodbc\\Access DB\\LFSDBdata_Compressed.accdb'
        db = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir=D:/KengWoNCHUFile/AccessDB;DBQ='+DBfile)
        #print("Successfully established connection....")
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
    
    def SQLdelete(self):
        sqlUtil=MysqlUtil()
        db = sqlUtil.getConnect()
        cursor = db.cursor()
        SQLdel=""" 
        delete from Record
        """
        #where [timestamp_started]>= #2025/07/29 00:00:00#
# =============================================================================
#         SQLdel=""" 
#         delete from Recording_data 
#         where 
#         [timestamp_started]>= #2027/11/1 00:00:00#
#         """
# =============================================================================
        cursor.execute(SQLdel)
        db.commit()
        cursor.close()
        db.close()  
#        try:
#            cursor.execute(SQLdel)
#            db.commit()
#            cursor.close()
#        except Exception as e:
#            cursor.close()
#            db.close()  
#            print(e)
#        
#            pass
#        finally:
#            cursor.close()
#            db.close()  
        print('Delect successfully') 

    def SQLsDatainsert(self,val):
        sqlUtil=MysqlUtil()
        db = sqlUtil.getConnect()
        
        cursor = db.cursor()
        SQLin ="""
        INSERT INTO Record ([rec_id],[conn_id],[timestamp_started],[timestamp_ended],[delta],
                                    [coeff_5],[coeff_4],[coeff_3],[coeff_2],[coeff_1],[coeff_0]) 
        VALUES (?,?,?,?,?,
                ?,?,?,?,?,?) 
        """
# =============================================================================
#         INSERT INTO Recording_data ([node_id],[sensor_id],[timestamp_started],[timestamp_ended],[delta],
#                                     [coeff_5],[coeff_4],[coeff_3],[coeff_2],[coeff_1],[coeff_0]) 
#         VALUES (?,?,?,?,?,
#                 ?,?,?,?,?,?) 
#         """
# =============================================================================
        #t=[(dataCSV[1][0],str(dataCSV[1][1]),dataCSV[1][2]),(dataCSV[2][0],str(dataCSV[2][1]),dataCSV[2][2])]
        #print(t)
        try:
            tStart = time.time()#計時開始
            cursor.executemany(SQLin,val)
            db.commit()
            tEnd = time.time()#計時結束
        except Exception as e:
            db.close()  
            print(e)
            tEnd = time.time()
            pass
        finally:
            timer=tEnd-tStart
            db.close()  
        print('process time',round(timer,2))
        return timer

def insertDate(yr=2018,mth=1,d=1):
    month=0
    leapY=0
    for m in range(mth-1,0,-1):
        if(m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12):
            Sec_perMth=2678400
        elif(m==2):
            Sec_perMth=2419200
        elif(m==4 or m==6 or m==9 or m==11):
            Sec_perMth=2592000
        else:
            Sec_perMth=0
        month+=Sec_perMth
    if (yr>2018):
        year=(yr-2018)*31536000
    else:
        year=0
    day=(Sec_perday)*(d-1)
    for y in range(2018,yr+1):
        if(y%4==0 and y%100!=0)or(y%400==0):
            leapY+=1
    leapDay=leapY*Sec_perday
    time=int(start_day)+year + month + day  +leapDay
    return str(datetime.utcfromtimestamp(time).date())


def IDstr(num):
    if(num < 10):
        strNum="00"+str(num)
    elif(num>=10 and num<=99):
        strNum="0"+str(num)
    else:
        strNum=str(num)
    return strNum


    
    
if __name__=="__main__":
    sqlUtil=MysqlUtil()
    
        

    
    for (dirpath, dirnames, filenames) in walk(mypath):
        f=list(filenames[i][:-4]for i in range(len(filenames)))    
        idx=list(i for i in range(len(filenames)))    
# =============================================================================
#     for n in range(len(filenames)):
#         print(n,':',filenames[n][:-4])
# =============================================================================
    
# =============================================================================
#     with open(mypath+'\\'+filenames[1],newline='')as datafile:
#         spamreader =csv.reader(datafile,delimiter=' ',quotechar='|')
#         next(spamreader)
#         try:
#             for row in spamreader:
#                 strData=','.join(row).split(',')
#                 print(strData[0]+' '+strData[1])
#                 value=[]
#                 datetime_start = datetime.strptime(strData[0]+' '+strData[1], '%Y-%m-%d %H:%M:%S')
#                 datetime_end = datetime.strptime(strData[0]+' '+strData[3], '%Y-%m-%d %H:%M:%S')
#                 print(datetime_start)
#                 print(datetime_end)
#                 delta=int(strData[4])
#                 print(delta)
#         finally:
#                 datafile.close()
#     datetime_start = datetime.strptime(strData[0]+' '+strData[1], '%Y-%m-%d %H:%M:%S')
#     datetime_end = datetime.strptime(strData[2]+' '+strData[3], '%Y-%m-%d %H:%M:%S')
#     
#     print(datetime_start)
#     print(datetime_end)
#     for i in range(4,len(strData)):
#         print(float(strData[i]))
#     
# =============================================================================
        
        
        
# =============================================================================
#     sqlUtil.SQLdelete()
#     sqlUtil.compactAccessDB()
# =============================================================================
   
    
    
    ##insert CompressData 從每日已壓縮好的Data一直存入DB 中
    #print(filenames[0][6:-15]=="H1")
    usetime=[] 
    startYear=2018
    startMth=1
    startDay=1
    fileIdx=0
    cnt=0
    num_id=0
    cntDay=0
    edDate=""
    #stDate=dt.datetime(startYear,startMth,startDay).date().strftime('%Y-%m-%d')
    #print(stDate[1])
    #while(cntDay<=len(filenames)):
    isStartLoop=True
    while(startDay<32): 
        fName=filenames[fileIdx][6:-15]
        if(fName=="H1" ):
    #for day in range(startDay,startDay+730):  
            date=insertDate(yr=startYear,mth=startMth,d=cntDay)
            stDate=dt.datetime(startYear,startMth,startDay).date().strftime('%Y-%m-%d')
            #print(cntDay)
# =============================================================================
#             print(stDate)
#             print(startDay)
# =============================================================================
            data=[]
            with open(mypath+'\\'+filenames[fileIdx],newline='')as datafile:
                spamreader =csv.reader(datafile,delimiter=' ',quotechar='|')
                next(spamreader)
                try:
                    for row in spamreader:
                        strData=','.join(row).split(',')
                        #print(strData)
                        value=[]
                        #print(type(strData[1]))
                        datetime_start = datetime.strptime(stDate+' '+strData[1], '%Y-%m-%d %H:%M:%S')
                        datetime_end = datetime.strptime(stDate+' '+strData[3], '%Y-%m-%d %H:%M:%S')
# =============================================================================
#                         datetime_start = datetime.strptime(strData[0]+' '+strData[1], '%Y-%m-%d %H:%M:%S')
#                         datetime_end = datetime.strptime(strData[2]+' '+strData[3], '%Y-%m-%d %H:%M:%S')
# =============================================================================
                        num_id+=1
# =============================================================================
#                         print(datetime_start)
#                         print(datetime_end)
# =============================================================================
                        delta=int(strData[4])
                        for i in range(5,len(strData)):
                            #print(float(strData[i]))
                            value.append(float(strData[i]))
                        conn_id=2
                        
                        #print(value)
                        ##for sensor_id in range(1,2):##  7 sensor 
                            ##for node_id in range(1,2): ## 16 node               
                                 #print(len(value))    
    # =============================================================================
    #                              t=(node_id,sensor_id,datetime_start,datetime_end,
    #                                 delta,value[0],value[1],value[2],value[3],value[4],value[5])
    # =============================================================================
                        t=(num_id,("C"+IDstr(conn_id)),datetime_start,datetime_end,delta,value[0],value[1],value[2],value[3],value[4],value[5])
                         #print(t)
                        data.append(t)
                                 #print(data[0][:2],'-',data[len(data)-1][:2])
                        #print(data)
                    try:
                        #print(type(date))
                        #print(len(data))                    
                        edDate=datetime.strptime(date,'%Y-%m-%d').date().strftime('%Y-%m-%d')
                        print(stDate,'using data is',fileIdx,':',filenames[fileIdx][:-15])
                        #print(strData[0],'using data is',fileIdx,':',filenames[fileIdx][:-15])
                        usetime.append(sqlUtil.SQLsDatainsert(data))
                        fileIdx+=1
                        cntDay+=1
                        cnt+= 1
                        startDay+=1
                        print(startDay)
                        #print("1",fileIdx)
# =============================================================================
#                         if(fileIdx>=len(filenames)-1):
#                             fileIdx=0
#                             cnt+= 1
#                             print("2",fileIdx)
# =============================================================================
                    
                    except Exception as e:
                        print(e)
                        break
                finally:
                    datafile.close()
        else:   
            fileIdx+=1
            if(fileIdx>=len(filenames)-1):
                fileIdx=0
                print('end loop')
                isStartLoop=False

           
                
    rawfilesize=sqlUtil.get_FileSize()
    sqlUtil.compactAccessDB()
    compfilesize=sqlUtil.get_FileSize()
    
    print('Mean: ',round(np.mean(usetime),2),'輸入完大小',rawfilesize,'壓縮後大小',compfilesize,'天數',cntDay)
    record=[{'time':round(np.mean(usetime),2),
              'start_Date':stDate,
              'end_Date':edDate,
              'Compact Size':compfilesize,
              'total days':cntDay-startDay,
              'file index:':fileIdx,
              'count':cnt,
              'count Day':cntDay,
              'fileIdx':fileIdx,
              'filenames':filenames[fileIdx-2][:-15]
              }]
    print("record",record)
    df=pd.DataFrame(record,index=None)  
    dfcolumns=['time','start_Date','end_Date','Compact Size','total days','count','count Day','fileIdx','filenames']
    if (pth.isfile('./Insertinto_Compressed_detailData.csv')!=True):  
        df.to_csv('Insertinto_Compressed_detailData190621.csv',mode='w',
                  columns=dfcolumns,
                  index=False)
    else:
        df.to_csv('Insertinto_Compressed_detailData190621.csv',mode='a',columns=dfcolumns,header=None,index=False)



# =============================================================================
# 
# 
# ##查詢結果
#     strdate=str(dt.datetime.utcfromtimestamp(1514764800))
#     sqlUtil=MysqlUtil()
#     db = sqlUtil.getConnect()
#     cursor = db.cursor()
#     SQL="""
#     select *
#     from Record            
#     where [timestamp_started]>= #2019/01/1 00:00:00# and 
#     [timestamp_started]< #2019/01/1 00:50:00#
#     """ 
#     tStart = time.time()#計時開始
#     data=[]
#     timestamp=[]      
#     for row in cursor.execute(SQL):                  # cursors are iterable
#         data.append(row)
#         print ('(',row[0],row[1],row[2],row[3],
#                  row[4],row[5],row[6],row[7],row[8],row[9],row[10],')')
#         
#         
#     cursor.commit()
#     #print(data)
#     cursor.close()
#     db.close()
#     tEnd = time.time()#計時結束    
#     timer=tEnd-tStart
#     print('執行時間：',timer,'。data 總數 ',len(data))
# =============================================================================




