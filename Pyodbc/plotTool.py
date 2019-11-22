# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 13:57:22 2018

@author: Jeff PC
"""
from plotly.offline import plot
import folderTool as fT
import cufflinks as cf
import plotly.graph_objs as go
cf.go_offline()

def PlotLy(t,wdsize_percent,min_interval_percent,polyIndex,fileName,pltData,isOpen=False):
    strtitle=fileName[12:-7]+' Plot-'+str(len(t))
    layout=go.Layout(title=strtitle,
                     xaxis=dict(
                             #title='AXIS TITLE',
                             titlefont=dict(
                                         #family='Arial, sans-serif',
                                         size=20,
                                         color='lightgrey'
                                         ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                    #family='Old Standard TT, serif',
                                    size=35,
                                    color='black'
                                            ),
                                    exponentformat='e',
                                    showexponent='all'
                                             ),      
                    yaxis=dict(
                            #title='AXIS TITLE',
                            titlefont=dict(
                                    #family='Arial, sans-serif',
                                    size=20,
                                    color='lightgrey'
                                    ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                    #family='Old Standard TT, serif',
                                    size=35,
                                    color='black'
                                    ),
                            exponentformat='e',
                            showexponent='all'
                            ),
                    showlegend=False)
    #plot(pltData,layout,image='png',image_filename=fileName,filename=".\Plot_html\\"+fileName+".html")
    #filePath=".\Plot_html\\SlidingWindow\\"+'wdL '+str(SGwd_length)+'\\max angle '+str(angle)+'\\'
    filePath=".\Plot_html\\"
    fT.mkfolder(filePath)
    fig=go.Figure(data=pltData,layout=layout)
    #print(fileName)
    plot(fig,filename=filePath+fileName[12:]+".html",auto_open=isOpen)