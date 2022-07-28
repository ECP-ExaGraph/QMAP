#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:03:25 2018

@author: khan242
"""

import os
import sys
import math
import QMap
import time


dataFolder=""
resFolder="/files0/home/khan242/quantum/results/"


nbody=int(sys.argv[1])
layout=str(sys.argv[2])

print(type(nbody),type(layout))

    
if nbody==1:
    dataFolder="../data/one/"
else:
    dataFolder="../data/two/"
        
print(dataFolder)
for fileName in os.listdir(dataFolder):
    
    nInteractions=0
    nVer=0
    flag=0
    if fileName.endswith(".txt"):
        print("---------------------------------------\n")
        print("Processing: "+fileName,"\n")
        
        
        flag=0
        if "n2" in fileName:
            flag==1
            #continue
        else:
            flag=0
            #continue
        

        outFile=fileName
        outFile=outFile.split(".")
        problemName=fileName
        outFile=outFile[0]+outFile[1]
        
        fileName=dataFolder+fileName
        
        f=open(fileName,"r")
        
        
        listofInteractions=[{},{},{},{},{}]
        k=[]
        for line in f:
            line=line.strip("\n")
            line=line.split(" ")
            k=[]
            for s in line:
                if s.isnumeric():
                    k.append(int(s)-1)
                    
            
            if nbody == 1:
                if len(k) > 2:
                    k.pop()
            
            if nbody == 2:
                if len(k) > 4:
                    k.pop()
            
            tk=set(k)
            tk=tuple(tk)
            tk=sorted(tk)
            lInter=len(tk)
            if lInter >=2:
                listofInteractions[lInter][tuple(tk)]=0
            
            nInteractions=nInteractions+1
            if len(tk) > 0 and max(tk) > nVer:
                nVer=max(k)
        
        f.close()
        
        nVer=nVer+1
        
        uInter=len(listofInteractions[2])+len(listofInteractions[3])+len(listofInteractions[4])
        print("Number of Orbitals: ",nVer,"\n")
        print("Number of Interactions: ",nInteractions,"\n")
        print("Number of Unique Interactions: ", uInter,"\n")
        
########################### Creating the gates ###################      
        gates={}
        
        if layout=="1D":
            if nbody==1:
                for i in range(nVer-1):
                    gates[(i,i+1)]=1
            else:
                side=math.pow(nbody,2)
                for i in range(nVer-int(side)+1):
                    gates[(i,i+1,i+2,i+3)]=1
        
        if layout == "2D":
            if nbody==1:
                side=math.ceil(math.sqrt(nVer))
                qbits=side*side
                #print(side,qbits)
                for i in range(qbits):
                    if i-1 >=0:
                        gates[(i-1,i)]=1
                    if i+1 < side:
                        gates[(i,i+1)]=1
                    if i-side >=0:
                        gates[(i-side,i)]=1
                    if i+side < side:
                        gates[(i,i+side)]=1
            else:
                side=math.ceil(math.sqrt(nVer))
                qbits=side*side
                #print(side,qbits)
                for i in range(qbits):
                    t=[]
                    t.append(i)
                    
                    if i-1 >=0:
                        t.append(i-1)
                    if i+1 < side:
                        t.append(i+1)
                    if i-side >=0:
                        t.append(i-side)
                    if i+side < side:
                        t.append(i+side)
                    
                    t=set(t)
                    t=tuple(t)
                    t=sorted(t)
                    
                    gates[tuple(t)]=1
                
        #if layout == "ARB":
 
###############################################################
           
        start = time.time()
       
        #print(gates)
        #print(listofInteractions)
        totSwaps=0
        totDepth=0
        ts=0
        td=0
        for i in range(len(listofInteractions)):
            if len(listofInteractions[i]) > 2:
                print(str(i),"-electron interactions: ",len(listofInteractions[i]))
                (ts,td)=QMap.nBodyInteractions(listofInteractions[i],nVer,layout,gates,verbose=True)
                totSwaps=totSwaps+ts
                totDepth=totDepth+td
        #break
        
        end = time.time()
        print("Summary: ",problemName,",",nVer,",",nInteractions,",",totSwaps,",",totDepth)
        print("Time: ",end - start)
