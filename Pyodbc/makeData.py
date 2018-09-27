# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:20:58 2018

@author: Jeff PC
"""
import matplotlib.pyplot as pl
import numpy as np
import datetime as dt

start_day=1514764800
Sec_perday=86400


def f(data):
    x = np.linspace(1, len(data), len(data))
    y= np.around(np.sin(x) + np.random.normal(scale=1, size=len(x)),decimals=2)
    return y


def add1DpS(yr=2018,mth=1,d=1):
    month=0
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
    time=int(start_day)+year + month + day  
    t=[]
    for _ in range(1440):
       t.append(dt.datetime.utcfromtimestamp(time))
       time+=60
    return t
    
    
    
if __name__=="__main__":
    x = np.linspace(0, 1440,1440)
    for day in range(1):
        date=add1DpS(yr=2019,mth=7,d=day+1)
        print(date[0])
        print(f(date))
        pl.plot(date, f(date))