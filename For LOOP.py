# -*- coding: utf-8 -*-
"""
Created on Sat May  5 06:09:55 2018

@author: User
"""
x=[1,2,3,4,5,6,7,8,9,0,1,2,3]
start=4
print(len(x))
print()
end=12
t=9
delta=end-start
for i in range(end,start-1,-1):
    print (x[i],' ',i)
for w in range(0,5,1):
    t-=1
    print(t/100)