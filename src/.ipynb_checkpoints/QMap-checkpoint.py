#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 15:35:29 2018

@author: khan242
"""

import math
import linar
import hypergraph as hyp
import os
import sys
import time
import json
import networkx as nx
import numpy as np
from networkx.utils import reverse_cuthill_mckee_ordering

def layout_to_gates(layout,nbody,nVer):
    
    gates={}

    if layout=="1D":
        if nbody==1:
            for i in range(nVer-1):
                gates[(i,i+1)]=1
        
        if nbody==2:
            for i in range(nVer-1):
                gates[(i,i+1)]=1
            #for i in range(nVer-2):
                #gates[(i,i+1,i+2)]=1
            #for i in range(nVer-3):
                #gates[(i,i+1,i+2,i+3)]=1
    #print(gates)
    
    elif layout == "2D":
        if nbody==1:
            side=int(math.ceil(math.sqrt(nVer)))
            qbits=side*side
            #print(side,qbits)
            for i in range(qbits):
                if i-1 >=0:
                    if int((i-1)/side) == int(i/side):
                        gates[(i-1,i)]=1
                if i+1 < qbits:
                    if int((i+1)/side) == int(i/side):
                        gates[(i,i+1)]=1
                if i-side >=0:
                    #if int((i-side)/side) == int(i/side):
                    gates[(i-side,i)]=1
                if i+side < qbits:
                    #if int((i+side)/side) == int(i/side):
                    gates[(i,i+side)]=1
        else:
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
    
    elif layout == "Rigetti":
        mapping={}
        rings=8
        for i in range(rings):
            mapping[i]=[(i+1)%rings]
            mapping[i+rings]=[((i+1)%rings)+rings]


        t=mapping[0]
        t.append(rings)
        mapping[0]=t
        t=mapping[1]
        t.append(1+rings)
        mapping[1]=t
        
        gates=connectivity_to_gates(mapping,nbody,nVer)
        
    elif layout == "Google":
        mapping={}
        k=72
        for i in range(k):
            nbors=[]
            if (i//6)%2 ==0:
                for offset in (-7,-6,5,6):
                    if ((0 <= i+offset <  k) and (((i+offset) // 6)%2 != (i // 6)%2)):
                        nbors.append(i+offset)
            else:
                for offset in (-6,-5,6,7):
                    if ((0 <= i+offset <  k) and (((i+offset) // 6)%2 != (i // 6)%2)):
                        nbors.append(i+offset)

            mapping[i]=nbors
        

        gates=connectivity_to_gates(mapping,nbody,nVer)
    
    else:
        print("Layout: ",layout)
        gates=edgelist_to_gates(layout,nbody,nVer)
    
    return gates

def findPaths(G,u,k):
    if k==0:
        return [[u]]
    paths = []
    for neighbor in G.neighbors(u):
        for path in findPaths(G,neighbor,k-1):
            if u not in path:
                paths.append([u]+path)
    return paths

def edgelist_to_gates(fileName,nBody,nVer):
    
    ########## Create Graph from the connectivity Map####
    G=nx.Graph()
    edges=[]
    
    f=open(fileName,"r")

    k=[]
    for line in f:
        line=line.strip("\n")
        line=line.split(" ")
        k=[]
        for s in line:
            if s.isnumeric():
                k.append(int(s)-1)
        edges.append(tuple(k))
    
    G.add_edges_from(edges)
    
    SG=greedy_dense(G,2*nVer)
    SG=greedy_dense(SG,nVer)
    
    return graph2gates(SG)
                
def connectivity_to_gates(connectivity_map,nBody,nVer):
    
    ########## Create Graph from the connectivity Map####
    G=nx.Graph()
    edges=[]
    for i in connectivity_map.keys():
        t=connectivity_map[i]
        
        for j in t:
            edges.append((i,j))

    
    G.add_edges_from(edges)
    
    SG=greedy_dense(G,2*nVer)
    SG=greedy_dense(SG,nVer)
    
    return graph2gates(SG)
    
def greedy_dense(G,nVer):   
    
    if G.number_of_nodes()<= nVer:
        return G
    #print(G.nodes,G.edges)
    #### Now pick a dense subgraph of size nVers from connectivity graph
    k=nVer
    k1=int(math.ceil(k/2.0))
    k2=k-k1
    t=sorted(G.degree, key=lambda x: x[1], reverse=True)
    topk=[]
    for i in range(k1):
        topk.append(t[i][0])

    botk=[1]*G.number_of_nodes()
    
    for i in G.nodes:
        if i in topk:
            botk[i]=0
        else:
            nbors=set(G.neighbors(i))
            count=len(nbors.intersection(set(topk)))
            botk[i]=count

    botk=list(np.argsort(botk))
    botk=botk[-k2:]
    topk=sorted(topk+botk)
    
    
    SG=nx.Graph()
    nodes=range(len(topk))
    SG.add_nodes_from(nodes)

    G1=G.subgraph(topk)
    edges=[]
    for (i,j) in G1.edges:
        edges.append((topk.index(i),topk.index(j)))
    
    SG.add_edges_from(edges)
    rcm=list(reverse_cuthill_mckee_ordering(SG))
    A=nx.adjacency_matrix(SG,nodelist=rcm)
    TG=nx.from_scipy_sparse_matrix(A)
    return TG
    
    
def graph2gates(SG):    #### Now create the gates out of the subgraph
    gates={}
    
    k=1
    for l in range(1,k+1): 
        for u in SG.nodes:
            paths=findPaths(SG,u,l)
            for p in paths:
                t=set(p)
                t=tuple(t)
                t=sorted(t)
                gates[tuple(t)]=1
    return gates

def nBodyInteractions(interactions,nVer,layout,gates,verbose=False,paralle=False):
    
    qbits=nVer
    if layout=="1D":
        qbits=nVer
    
    if layout=="2D":
        side=math.ceil(math.sqrt(nVer))
        qbits=side*side
     
    if layout=="Google":
        qbits=nVer
    
    if layout=="Rigetti":
        if nVer > 16:
            return (0,0,0)
        qbits=nVer
    
    D=hyp.all_pair_shortest_path(gates,qbits)
    
    rcm=linar.HyperAlign(interactions,nVer,D)
    #rmap=linar.reverse_map(rcm)
    
    #print("Moves: ",rcm)
    #print("Inverse: ", rmap)
    
    origOrder={}
    for i in range(nVer):
        origOrder[i]=rcm[i]
        
    #if verbose:
        #print("Initial Assignmet: " ,rmap)
        #print("Assignment 1: " ,[x for x in rmap])
    
    [newOrder, diam]=linar.reorder_hyperedges_parallel(interactions,rcm,D)
    
    #print("Orbital position: ",origOrder)
    
    [swaps, depth, qeff] = iterative_mapping(newOrder,origOrder,nVer,rcm,D,verbose=verbose)
    
    #if verbose==False:
    #print("Total Swap = ",swaps, ", Total Depth = ",depth, ", Utilization = ",qeff,"\n")
    
    
    oSwap=0
    """
    if nVer % 2 == 0:
        oSwap = int((nVer/2)**2 + (nVer/2 -1)**2)
    else:
        oSwap = int((int(nVer/2))*nVer)
    if verbose:
        print("Original Swaps = ", oSwap,", Original Depth = ",nVer,"\n")
    """
    return (swaps,depth,qeff)


def iterative_mapping(interactions,origOrder,nVer,rcm,D,verbose=False,parallel=False):
    count=0
    iteration=1
    hyperedges=interactions.copy()
    #rmap_prev=linar.reverse_map(rcm)
    
    qEff=1.0 
    
    interN=0
    
    while True:
        
        m,qcount=hyp.hypergraph_matching(hyperedges,nVer)
        
        if len(m) >0:
            qEff=(qEff*qcount)/nVer
            #print(qEff)        
            interN=interN+len(m)
            if verbose:
                #print("Iteration ",iteration,":", len(m)," ",qcount,"\n")
                origM=[]
                for i in range(len(m)):
                    temp=[]
                    for j in m[i]:
                        for orb, rcm in origOrder.items():
                            if rcm == j:
                                temp.append(orb)
                    origM.append(tuple(temp))
                #print("Interaction number: ",interN,"\n")
                print("Iteration ",iteration,":",origM,"\n")
            iteration=iteration+1
        
        for i in range(len(m)):
            hyperedges.pop(m[i])
            
        #print("hyperedges:", len(hyperedges))
        if len(hyperedges)==0:
            
            if verbose:
                print("Bringing back:")
                print("Here are the final positions of the orbitals: ",origOrder)
            
            rcm=[-1]*nVer
            for i in range(nVer):
                rcm[origOrder[i]]=i
            
            #print(origOrder)
            #print(rcm)
            #print(linar.reverse_map(rcm))
            linar.oddEvenSort_distance(rcm)
            
            break
        
        rcm=linar.HyperAlign(hyperedges,nVer,D)
        #rmap=linar.reverse_map(rcm)
        
        #print("Moves: ",rcm)
        #print("Inverse: ",rmap)
        
        for i in range(nVer):
            val=origOrder[i]
            origOrder[i]=rcm[val]
#    
        [newOrder,diam]=linar.reorder_hyperedges_parallel(hyperedges,rcm,D)
        hyperedges=newOrder.copy()
        #print("Orbital position: ",origOrder)
        if len(m) > 0:
            #curSwap=linar.kendall_tau_distance(rmap_prev,rmap)
            curSwap=diam
            #if verbose:
                #print("Assignmet ",iteration ,rmap, ", Swaps = ",curSwap)
                #print("Assignmet ",iteration,":",rmap)
            
        #rmap_prev=rmap.copy()   
#        curSwap=0;
#        for i in range(len(rcm)):
#           if i != rcm[i]:
#               curSwap=curSwap+2
#        print("Assignmet ",iteration ,rcm, ", Swaps = ",curSwap,"\n")
           
    
        
       
        count= count+curSwap
    
    if iteration > 1: 
        return [count, iteration-1, qEff**(1.0/(iteration-1)) ]
    else:
        return [count, iteration-1, qEff]
                

def main(fname,nbody=2,layout="1D",jsonfile=True,verbose=False,parallel=False):
    
    nInteractions=0
    listofInteractions=[{},{},{},{},{}]
    
    if jsonfile:
        with open(fname) as json_file:
            data = json.load(json_file)
            nVer=data['constants']['nSpinOrbitals']

            for p in data['terms']:
                k=p['targets']

                tk=set(k)
                tk=tuple(tk)
                tk=sorted(tk)
                lInter=len(tk)
                if lInter >=2:
                    listofInteractions[lInter][tuple(tk)]=0

                nInteractions=nInteractions+1
    else:
        if nbody==1:
            dataFolder="../data/test/one/"
        else:
            dataFolder="../data/test/two/"

        nInteractions=0
        nVer=0
        flag=0
        if fname.endswith(".txt"):
            if verbose:
                print("---------------------------------------\n")
                print("Processing: "+fname,"\n")

            outFile=fname
            outFile=outFile.split(".")
            problemName=fname
            outFile=outFile[0]+outFile[1]

            fileName=dataFolder+fname

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
        

    uInter=len(listofInteractions[1])+len(listofInteractions[2])+len(listofInteractions[3])+len(listofInteractions[4])
        
    if verbose:
        print("Number of (spin) Orbitals: ",nVer,"\n")
        print("Number of Interactions: ",nInteractions,"\n")
        print("Number of Unique Interactions: ", uInter,"\n")

    ########################### Creating the gates ###################      
    

    if layout == "Rigetti":
        if nVer > 16:
            return
    
    gates=layout_to_gates(layout,nbody,nVer)
    #print(gates)
    ###############################################################
    
    start = time.time()

    #print(nVer,layout)
    #print("Gates: ",gates)
    #print("interaction: ",listofInteractions)
    totSwaps=0
    totDepth=0
    ts=0
    td=0
    
    motherlist={}
    for i in range(2,len(listofInteractions)):
        if len(listofInteractions[i]) >= 1:
            print(str(i),"-electron interactions: ",list(listofInteractions[i].keys()))
            print("Layout: ",list(gates.keys()),"\n")
            motherlist.update(listofInteractions[i])

    (ts,td,qeff)=nBodyInteractions(motherlist,nVer,layout,gates,verbose=verbose)
    totSwaps=totSwaps+ts
    totDepth=totDepth+td
            #break

    end = time.time()
    
    line="Summary,"+fname+","+str(nVer)+","+str(nInteractions)+","+str(uInter)+","+str(totSwaps)+","+str(totDepth)+","+str(qeff)+","+str(end-start)+"\n"
    f=open("out.csv",'a+')
    f.write(line)
    f.close()
    #print("Summary,",fname,",",nVer,",",nInteractions,",",uInter,",",totSwaps,",",totDepth,",",qeff,",",end-start)
    #print("Time:",end - start)
    
if __name__ == '__main__':
    
    fname=str(sys.argv[1])
    nbody=int(sys.argv[2])
    layout=str(sys.argv[3])
    
    if fname == "All":
        if nbody==1:
            dataFolder="../data/test/one/"
        else:
            dataFolder="../data/test/two/"

        print(dataFolder)
        for fileName in os.listdir(dataFolder):
            print(fileName)
            main(fileName,nbody,layout,False,True)

    else:       
        print(fname)
        main(fname,nbody,layout,True,True)
    
