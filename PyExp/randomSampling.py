# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:14:45 2018

@author: Jeff PC
"""
import random
import numpy as np


def calfactorial(n):
    sum = 1
    for i in range(1, n + 1):
        sum *= i       
    return sum        
def Combin(n,k):
    return calfactorial(n)/(calfactorial(k)*calfactorial(n-k))
def rndSample(COUNT):
    ck=True
    resultList=[]
    A=0
    B=5
    while(ck):
        i=random.randint(A,B)#不重複
        if(len(resultList)<COUNT):
            if( i not in resultList):#檢查當前己經生成的臨時隨機數是否存在
                resultList.append(i)
        else:
            ck=False
            
    return sorted(resultList)

            
def Sampling(RANGE,COUNT,splist=[]):#隨機抽樣
    LstObj=[]
    A=0
    B=RANGE 
    tf=True
    #resultList=sorted(random.sample(range(A,B+1),COUNT))
    while(tf):    
        #resultList=rndSample(COUNT)
        LstTarget=splist
        LstObj=sorted(random.sample(range(A,B),COUNT))
        # sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素。上面的方法写了那么多，其实Python一句话就完成了
        #print(len(splist))
        n=0
        if(len(splist)!=0)and(len(LstTarget)<int(Combin(B+1,COUNT))):
            while( n <len(LstTarget)):
                sTgt = set(LstTarget[n])
                sObj = set(LstObj)
                #print(len(list(s1.intersection(s2))))
                if(len(list(sTgt.intersection(sObj)))==COUNT):
                    n=0
                    LstObj=sorted(random.sample(range(A,B),COUNT))
                elif(len(list(sTgt.intersection(sObj)))!=COUNT)and(n==len(LstTarget)-1):
                    n+=1
                    tf=False
                else:
                    n+=1                
        else:
            tf=False
    #print(Combin(B,COUNT))
    if (len(LstTarget)==Combin(B,COUNT)):                         
        return []     
    else:
        return sorted(LstObj)
if __name__=="__main__":
    tf=True
    Oldsplist=[]
    cut=0
    
# =============================================================================
#     while(cut<10):
#         ary=Sampling(5,Oldsplist)
#         print(ary)
#         Oldsplist.append(ary)
#         cut+=1
#         
#     print(Oldsplist)        
# =============================================================================
# =============================================================================
#     while(tf):
#         ary=Sampling(3,Oldsplist)
#         print(ary)
#         if(len(ary)==0) or (cut==10):
#             tf=False
#         else:
#             Oldsplist.append(ary)
#             cut+=1
#     print(Oldsplist)
#     
# =============================================================================
   # print(Combin(158,30))
    
    
##集合比對
# =============================================================================
#     Lst1 = [[1,3,2],[4,2,1], [1,2,5]]
#     Lst2 = [1,5,4]
#     for i in Lst1:
#         s1 = set(i)
#         s2 = set(Lst2)
#         print(len(list(s1.intersection(s2))))
#         
# =============================================================================
# =============================================================================
#     Lst= [[1,2,3],[4,2,1],[1,2,5]]
#     test=['1,2,3']
#     n=test[0].split(",")
#     testNum=[int(x) for x in n]
#     print((Lst>test)-(Lst<test))
#     print(testNum)
#     a=np.array(Lst)
#     b=np.array(test)
#     print((a==b).any())
# =============================================================================
