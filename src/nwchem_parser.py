#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:50:23 2018

@author: khan242
"""

import sys
import os


oneFolder="/home/khan242/quantum/data/one/"
twoFolder="/home/khan242/quantum/data/two/"
dataFolder=sys.argv[1]

#dataFolder="/Users/khan242/PNNL/QCAT/data/test/H2O_PES/"
#oneFolder="/Users/khan242/PNNL/QCAT/data/test/H2O_PES/"
#twoFolder="/Users/khan242/PNNL/QCAT/data/test/H2O_PES/"


for fileName in os.listdir(dataFolder):
    
    outFile=fileName
    outFile=outFile.split(".")
    problemName=outFile[0]+"."+outFile[1]
    
    #print(dataFolder+fileName, problemName)   
    
    #if fileName.endswith(".nw"):
        #continue
    
    f=open(dataFolder+fileName,"r")
    
    nbody=0
    
    for line in f:
            
        skip=0    
        
            
        if "begin_one_electron_integrals" in line:
            nbody=1
            skip=1
            fout=open(oneFolder+problemName+".txt","w")
        
        if "end_one_electron_integrals" in line:
            nbody=0
            skip=0
            fout.close()
        
        if "begin_two_electron_integrals" in line:
            nbody=2
            skip=1
            fout=open(twoFolder+problemName+".txt","w")
        
        if "end_two_electron_integrals" in line:
            nbody=0
            skip=0
            fout.close()
            
        if nbody==0:
            continue
        else:
            if skip==1:
                skip=0
                continue
        
        fout.write(line)
        
        
    
    f.close()
