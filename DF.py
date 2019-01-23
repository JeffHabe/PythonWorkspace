# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 19:39:41 2018

@author: Jeff PC
"""

import pandas as pd
import numpy as np
ary=[]

df = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
#print(df.index[df['sex'][:][0]=='M'])
print(df['sex'][4][0])
print(len(df))
for i in range(0,len(df)):10
    checkChar=df['sex'][i][0]
    if (checkChar=='M'):
        print (i,df.iloc[i]['total_bill'])
        ary.append(df.iloc[i]['total_bill'])
    

print(np.mean(ary))