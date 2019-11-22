# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 00:19:45 2018

@author: Jeff PC
"""

from os import walk
import insertCompressData as iCD
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


#==============squared_error==========
def squared_error(ys_orig,ys_line):
    return sum((ys_line-ys_orig)**2)
#==============coeff_of_determination==========
def coeff_of_determination(ys_orig, ys_line,startPt=0,endPt=0):
    y_mean=np.mean(ys_orig)
    y_mean_line = [y_mean for y in ys_orig]## 生成一個值為y_mean,長度為ys_orig的陣列
    squared_error_regr = round(squared_error(ys_orig,ys_line),4)
    squared_error_y_mean = round(squared_error(ys_orig,y_mean_line),4)
    if(squared_error_y_mean==0):
        #print(startPt,'-',endPt)
        return 1
    else:    
        R2= 1 - ( squared_error_regr / squared_error_y_mean)
        return R2
    
#==============least_square==========
def least_square(fuc,ys_orig,m,n,x):
    ys_line=np.polyval(fuc,x)
    err=squared_error(ys_orig,ys_line)
    lsq=err/(m-n-1)
    return lsq
def sqlselect(datestart,dateend):
    ##查詢結果
    sqlUtil=iCD.MysqlUtil()
    db = sqlUtil.getConnect()
    cursor = db.cursor()
    SQL="""
    select *
    from Compressed_data
    where [timestamp_started]>=#"""+datestart+"""# and
    [timestamp_started]<= #"""+dateend+"""# and 
    [sensor_id] = 1 and [node_id]=1 
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

WCDpath ='D:\PythonWorkspace\PyExp\Data_csv\SlidingWindow\Chebyshev\Worst compressing data'
if __name__=="__main__":

  
# =============================================================================
#     for n in range(len(filenames)):
#         print(n,':',filenames[n][:-4])
# =============================================================================
    
                
       

    #print(len(data[0]))
# =============================================================================
#     for i in range(len(data[0])):
#         print(type(data[0][i]),':',data[0][i])
# =============================================================================


#=======  DB Select begining =================
    import traceback
    from plotly.offline import plot
    import plotly.graph_objs as go
    RMSDDC1Data=[]
    RMSDDC1Coeff=[]
    RMSDRAWnDBdata=[]
    RMSDDC12XlxsCoeff=[]
    RMSDXlxsData=[]
    RMSDXlxsCoeff=[]
    RMSDRAWnDCdata=[]
    lenDC1Data=[]
    fileIdx=0
    #print(data[0][2])
    for (dirpath, dirnames, filenames) in walk(WCDpath):
        f=list(filenames[i][:-4]for i in range(len(filenames)))    
        idx=list(i for i in range(len(filenames)))    

    cnt=0
## Get Xlsx Data and Coeff
    xlsxData=[]
    xlsxCoeff=[]
    while(cnt<2):
        cnt+=1
    #for day in range(startDay,startDay+730):  
        data=[]
        with open(WCDpath+'\\'+filenames[fileIdx],newline='')as datafile:
            spamreader =csv.reader(datafile,delimiter=' ',quotechar='|')
            next(spamreader)
            i=0
            for row in spamreader:
                strData=','.join(row).split(',')
                if (fileIdx%2==0):
                    xlsxData.append(np.float64(strData[2]))
                else:
                    for i in range(5,len(strData)):## 4 是多項式系數的常數項
                        xlsxCoeff.append(float(strData[i]))
                i+=1
        #print(rawData)
        fileIdx+=1

    dateStart='2018/01/18 00:00:00'
    dateEnd='2019/01/19 00:00:00'
    #print(dateStart,'-',dateEnd)
    data=sqlselect(dateStart,dateEnd)
    print(len(data))

    #print(data)
    pltData=[]
    sumX=0
    allX=[]
    dbData=[]
    coeffDBAll=[]
    print('Decompressing Data From DB')
    for t in range(len(data)):
        x=[]
        datetime_start = data[t][2]
        datetime_end = data[t][3]
        timedelta=((datetime_end-datetime_start)/data[t][4])
        datetime_ary=[]
        datetime_ary.append(datetime_start.strftime('%Y-%m-%d %H:%M:%S'))
        coeffDB=[]
        #print(datetime_start,'-',datetime_end)
        #print(type(data[t][4]))
        for i in range(data[t][4]):
            idx=sumX+i
            allX.append(idx)
            x.append(idx)
            datetime_ary.append((datetime_start+timedelta*(i+1)).strftime('%Y-%m-%d %H:%M:%S'))
            #(datetime_ary[i])
        sumX+=data[t][4]
        #print(x)
        #print(data[t][5])
        for i in range(len(data[t])-1,4,-1):## 4 是多項式系數的常數項
            coeffDB.append(data[t][i])
        coeffDBAll.extend(coeffDB)
        #print(coeffRaw)
        #print(np.poly1d(coeffRaw))
        try:
            ys_lineDB=chy.chebval(x,coeffDB)   
            dbData.extend(ys_lineDB)
        except:
            #print(coeffRaw)
            traceback.print_exc()  

        #print(type(coeffRaw[0]))
        #print(len(x))
        
        isOpen=True
        pltData +=[
        go.Scatter(
            x=datetime_ary, # assign x as the dataframe column 'x'
            y=ys_lineDB,
            mode='lines',
            marker=dict(
                    size=5,
                    color='rgba(255,0,0,0.9)'
                    )
            )]
        strtitle=' Plot-'+str(len(x))
    #print(len(allX))
    layout=go.Layout(title=strtitle)
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    fig=go.Figure(data=pltData,layout=layout)
    plot(fig,filename="test.html",auto_open=isOpen)

    #print(len(dbData))

    
    #=======  DB Select ending =================
    
    
    ##coeff compare
    cntCoeffRight=0
    cntDataRight=0
    
    # =============================================================================
    #     sumEroCoeff=0
    #     for n in range(len(coe fDBAll)): 
    #         print(coeffDBAll[n],':',coeffRaw[n])
    #         if(coeffDBAll[n]==coeffRaw[n]):
    #             cntCoeffRight+=1
    #         #print(coeffRaw[n]-coeffDBAll[n])
    #         sumEroCoeff+=np.round((coeffRaw[n]-coeffDBAll[n])**2,2)
    #     print(type(sumEroCoeff))
    #     RMSDCoeff=math.sqrt(sumEroCoeff/len(coeffDBAll))
    #     print('RMSD:',RMSDCoeff)
    # 
    #     
    # =============================================================================
    print()
    mypath ='excelFolder\\'
    fileName=fT.getFileName(mypath)
    #print(fileName[2])
    testList=[6,21,26,27,30,35,40,41,48,52,53,55,56,60,61,69,
                70,73,78,84,85,91,98,101,104,110,117,118,137,147]        

# =============================================================================
#     orgrawData,times=fT.readCSV(mypath+fileName[testList[testTime-1]])
# 
#     print('Compressing Data And Dcompressing Data to Compared')
#     coef_ary1,decompData1=CA.CompressAlg().Seg2poly(mypath+fileName[testList[testTime-1]])
# =============================================================================
    #print(decompData1)
    n=0
    testTime=0
    coeffAry=[]
    deCompData=[]
    aYearCoeffAry=[]
    aYeardeCompData=[]
    for testTime in range(30):
        orgrawData,times=fT.readCSV(mypath+fileName[testList[testTime]])
        coef_ary1,decompData1=CA.CompressAlg().Seg2poly(mypath+fileName[testList[testTime]])
        coeffAry.extend(coef_ary1)
        deCompData.extend(decompData1)
    print(len(deCompData))
    for m in range(12):
        aYearCoeffAry.extend(coeffAry)
        aYeardeCompData.extend(deCompData)
        print(len(aYeardeCompData))
    print(len(aYeardeCompData))

    for testTime in range(5):
        orgrawData,times=fT.readCSV(mypath+fileName[testList[testTime]])
        coef_ary1,decompData1=CA.CompressAlg().Seg2poly(mypath+fileName[testList[testTime]])
        aYearCoeffAry.extend(coef_ary1)
        aYeardeCompData.extend(decompData1)

    print(len(deCompData))
    print('Comparing Compressing Data And Dcompressing Data ')
        
    
    print('Orig Raw Data:',len(orgrawData))
    print('DC data:',len(decompData1))
    print('DC Coeff :',len(coef_ary1))
    print('xlsx data:',len(xlsxData))
    print('xlsx coeff :',len(xlsxCoeff))
    print('DB data:',len(dbData))
    print('coeffDB :',len(coeffDBAll))

        
    
    
    
## RMSD Calculater     
    print()
    testTime = 0 
    DataStt=0
    cnt=0
    sumDC1Data=0
    sumDC1Coef=0
    sumRAWnDBdata=0
    sumRAWnDCdata=0
    while(cnt<365):
        if(testTime<30):
            orgrawData,times=fT.readCSV(mypath+fileName[testList[testTime]])
        else:
            testTime=0


        DataLgh=len(orgrawData)
        
        print(len(orgrawData))
        #print(len(sumDC1Data))
        for n in range(DataStt,DataLgh):
    ## to compare decompress Alg data and Decompress DB data
            sumDC1Data+=(np.round(dbData[n],5)-np.round(aYeardeCompData[n],5))**2
    ## to compare decompressed Alg Coeff and Decompressed DB Coeff
            sumDC1Coef+=(coeffDBAll[n]-aYearCoeffAry[n])**2
    ##compare original raw data and decompress db coeff data
            sumRAWnDBdata+=(np.round(aYeardeCompData[n],5)-np.round(orgrawData[n],5))**2        
    ##compare original raw data and decompress coeff data
            sumRAWnDCdata+=(np.round(dbData[n],5)-np.round(orgrawData[n],5))**2
            #print(sumDC1Data)
        RMSDDC1Data.append(float(np.round(math.sqrt(sumDC1Data/len(orgrawData)),5)))
        RMSDDC1Coeff.append(float(np.round(math.sqrt(sumDC1Coef/len(orgrawData)),5)))
        RMSDRAWnDBdata.append(float(np.round(math.sqrt(sumRAWnDBdata/len(orgrawData)),5)))
        RMSDRAWnDCdata.append(float(np.round(math.sqrt(sumRAWnDCdata/len(orgrawData)),5)))
        testTime+=1
        DataStt+=len(orgrawData)
        lenDC1Data.append(len(orgrawData))
        print('DC Data1 RMSD:',np.round(RMSDDC1Data[cnt],5))
        print('DC Coeff1 RMSD:',np.round(RMSDDC1Coeff[cnt],5))
        print('Orig Raw Data RMSD:',np.round(RMSDRAWnDBdata[cnt],5))
        print('Orig Raw Data RMSD:',np.round(RMSDRAWnDCdata[cnt],5))
        print('end')
        print()
        cnt+=1
# =============================================================================
# ## to compare  Decompressed Alg Coeff and Decompressed Alg  Coeff in xlsx 
#     cntDataRight=0
#     sumEroCoeff=0
#     for n in range(len(coeffDBAll)):
#         if(xlsxCoeff[n]==coef_ary1[n]):
#             cntDataRight+=1
#         if(np.abs(xlsxCoeff[n]-coef_ary1[n])>=1):
#             print('n:',n)
#             print(xlsxCoeff[n],':',coef_ary1[n])
#         sumEroCoeff+=(xlsxCoeff[n]-coef_ary1[n])**2
#     RMSDDC12XlxsCoeff.append(float(np.round(math.sqrt(sumEroCoeff/len(coef_ary1)),4)))
#     print('Xlsx cp DC Coeff1 RMSD:',np.round(RMSDDC12XlxsCoeff[testTime-1],4))
#     print(xlsxCoeff[0],':',coef_ary1[0])
#     print('Xlsx cp DC Coeff1 Right time:',cntDataRight)
#     print()
#     
#     
#     
# ## to compare  Decompress DB data and decompress Alg  data in xlsx 
#     cntDataRight=0
#     sumEroData=0
#     for n in range(len(xlsxData)):
#         if(dbData[n]==xlsxData[n]):
#             cntDataRight+=1
#         sumEroData+=(np.round(dbData[n],5)-np.round(xlsxData[n],5))**2
#     RMSDXlxsData.append(float(np.round(math.sqrt(sumEroData/len(xlsxData)))))
#     print('ExcelData RMSD:',np.round(RMSDXlxsData[testTime-1],4))
#     print(dbData[0],':',xlsxData[0])
#     print('ExcelData Right time:',cntDataRight)
#     print()
#     
# ## to compare  Decompress DB Coeff and decompress Alg  Coeff in xlsx 
#     cntDataRight=0
#     sumEroCoeff=0
#     for n in range(len(coeffDBAll)):
#         if(coeffDBAll[n]==xlsxCoeff[n]):
#             cntDataRight+=1
#         sumEroCoeff+=(coeffDBAll[n]-xlsxCoeff[n])**2
#     RMSDXlxsCoeff.append(float(np.round(math.sqrt(sumEroCoeff/len(xlsxCoeff)),4)))
#     print('DC Coeff1 RMSD:',np.round(RMSDXlxsCoeff[testTime-1],4))
#     print(coeffDBAll[0],':',xlsxCoeff[0])
#     print('DC Coeff1 Right time:',cntDataRight)
#     print()
#     
# =============================================================================
    
    
# =============================================================================
#           'DC12Xlxs Coeff':RMSDDC12XlxsCoeff,
#           'xlxs2DB Data':RMSDXlxsData,
#           'xlxs2DB Coeff':RMSDXlxsCoeff,
# =============================================================================
#                   'length Xlsx Data':lenXlsxdata,
#           'length Xlsx Coeff':lenXlsxcoeff,
# =============================================================================
# =============================================================================
        
    NRMSD={'DC12DB Data':RMSDDC1Data,
          'DC12DB coeff':RMSDDC1Coeff,
          'RAW2DB Data':RMSDRAWnDBdata,
          'RAW2DC Data':RMSDRAWnDCdata,
          'length DC1 Data':lenDC1Data,
            }
    dfRMSD=pd.DataFrame(NRMSD,index=None)
    dfRMSD.to_csv('AyearRMSD '+datetime.now().strftime('%Y-%m-%d')+'.csv',mode='w',index=None)
    print(datetime.now().strftime('%Y-%m-%d'),' Compressing done')

