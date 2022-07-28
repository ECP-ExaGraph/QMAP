#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:03:25 2018

@author: khan242
"""

import os



    










dataFolder="../data/"
resFolder="../results/"

for fileName in os.listdir(dataFolder):
    if fileName.endswith(".2bi"):
        print("---------------------------------------\n")
        print("Processing: "+fileName,"\n")
        #fileName="vsp_bump2.mtx"

        outFile=fileName
        outFile=outFile.split(".")
        outFile=outFile[0]+outFile[1]
        problemName=outFile
        
        fileName=dataFolder+fileName
        
        f=open(fileName,"r")
        interactions={}
        for line in f:
            line=line.strip("\n")
            line=line.split(" ")
            idx=0
            k=[0,0,0,0]
            for s in line:
                if s.isnumeric():
                     k[idx]=int(s)-1
                     idx=idx+1
            
            interactions[tuple(k)]=0
            
        
        f.close()
        
        print("Number of Interactions: ",len(interactions),"\n")
        
        nVer=max(set(max(interactions)))+1
        twoBodyInteractions(interactions,nVer)
       