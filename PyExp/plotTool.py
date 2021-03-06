# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 13:57:22 2018

@author: Jeff PC
"""
from plotly.offline import plot
from plotly.offline import iplot

import folderTool as fT
import cufflinks as cf

import plotly.graph_objs as go
cf.go_offline()

def PlotLy(t,wdsize_percent,min_r2,polyIndex,fileName,pltData,isOpen=False):
    strtitle=fileName+' Plot-'+str(len(t))
    layout=go.Layout(title=strtitle)
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    filePath=".\Plot_html\\SlidingWindow\\"+'wdsize_percent='+str(wdsize_percent)+'\\min_r2='+str(min_r2)+'\\pIndex='+str(polyIndex)+'\\' 
    fT.mkfolder(filePath)
    fig=go.Figure(data=pltData,layout=layout)
    plot(fig,config=dict(showSendToCloud=True),filename=filePath+fileName+".html",auto_open=isOpen)
