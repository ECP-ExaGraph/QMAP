#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:40:09 2018

@author: khan242
"""

import random
import networkx as nx
import math
import hypergraph as hyp
from networkx.utils import reverse_cuthill_mckee_ordering

from multiprocessing import Pool
from functools import reduce
from functools import partial
from itertools import repeat

nProc=32
pool=Pool(nProc)

def reverse_map(rcm):
    temp=list(range(len(rcm)))
    for i in range(len(rcm)):
        j=rcm[i]
        temp[j]=i
     
    return temp  


def kendall_tau_distance(a, b):
    a=list(range(len(b)))
    l = len(a)

    distance = 0

    for m in range(l):
        # Start the range at m, so we don't recheck pairs
        for n in range(m, l):
            if (a[m] < a[n]) != (b[m] < b[n]):
                distance += 1

    return distance

#def kendall_tau_distance(order_b):
#    
#    
#    order_a=list(range(len(order_b)))
#    pairs = itertools.combinations(range(len(order_b)), 2)
#    distance = 0
#    for x, y in pairs:
#        a = order_a.index(x) - order_a.index(y)
#        b = order_b.index(x) - order_b.index(y)
#        if a * b < 0:
#            distance += 1
#    return distance

def JW_ordering_cost(rcm):
    
    prod=1.0
    for i in range(len(rcm)):
        temp=abs(i-rcm[i])
        if temp>0:
            prod=prod*temp
    
    #print(prod)
    prod=math.log(prod,2)
    return prod

def oddEvenSort_distance(rcm,verbose=True): 
    # Initially array is unsorted 
    arr=rcm.copy()
    n=len(arr)
    isSorted = 0
    iteration=0
    
    #print("Swaps:")
    while isSorted == 0: 
        
        isSorted = 1
        temp = 0
        odd=[]
        for i in range(1, n-1, 2): 
            if arr[i] > arr[i+1]: 
                arr[i], arr[i+1] = arr[i+1], arr[i] 
                odd.append((i,i+1))
                isSorted = 0
        
        even=[]  
        for i in range(0, n-1, 2): 
            if arr[i] > arr[i+1]: 
                arr[i], arr[i+1] = arr[i+1], arr[i] 
                even.append((i,i+1))
                isSorted = 0
        
        iteration=iteration+1   
        
        verbose=False
        if verbose:
            if len(odd)>0:
                print(odd)
            if len(even)>0:
                print(even)
    
    
    return iteration

def evaluate_permutation_parallel(interactions,rcm,DM):
   
    dist=0
    #print(interactions)
    #print(rcm)
    #print(D)
    """
    new_interactions=[]
    for keys in interactions.keys():
        
        new_keys=[]
        for i in range(len(keys)):
            new_keys.append(rcm[keys[i]])
        
        new_keys=tuple(set(new_keys)) 
        
        new_interactions.append(new_keys)
    """
    hyp_distance=partial(hyp.induce_hyperedge_distance, rcm = rcm, D = DM)
    #hyp_distance=partial(hyp.induce_hyperedge_distance, D = DM)
    
    new_interactions=[*interactions]
    chunk=int(math.ceil(len(new_interactions)/nProc*1.0))
    results=pool.map(hyp_distance,new_interactions,chunksize=chunk)
    
    dist1=sum(results)
    
    if len(interactions)>0:
        return dist1/len(interactions)
    else:
        return 0


def evaluate_permutation(interactions,rcm,D):
   
    dist=0
    #print(interactions)
    #print(rcm)
    #print(D)
    for keys in interactions.keys():
        
        new_keys=[]
        for i in range(len(keys)):
            new_keys.append(rcm[keys[i]])
        
        new_keys=tuple(set(new_keys)) 
        
        dist=dist+hyp.induce_hyperedge_distance(new_keys,D)

    
    if len(interactions)>0:
        dist=dist/len(interactions)
    else:
        dist=0

    return dist


def create_cycle_graph(interactions,nVer):
    G=nx.Graph()
    G.add_nodes_from(range(nVer))
    
    for tkeys in interactions.keys():
        
        keys=set(tkeys)
        keys=tuple(keys)
        keys=sorted(keys)
        
        
        if len(keys)<=1:
            continue
        if len(keys) > 2:
            for i in range(len(keys)):
                j=(i+1)%len(keys)
                G.add_edge(keys[i],keys[j],weight=1)
        else:
            G.add_edge(keys[0],keys[1],weight=1)
            
        
    
    return G

######################## create weight based on the hyperedges distance

def reorder_hyperedges(interactions, rcm, D):
    
    temp={}
    new_keys=()
    weight=1.0
    diameter=oddEvenSort_distance(rcm)
    JW=JW_ordering_cost(rcm)
    
    for keys in interactions.keys():
        
        lkeys=len(keys)
        
        if lkeys == 4:
            new_keys=(rcm[keys[0]],rcm[keys[1]],rcm[keys[2]],rcm[keys[3]])
                       
            
        if lkeys == 3:
            new_keys=(rcm[keys[0]],rcm[keys[1]],rcm[keys[2]])    
            
        
        if lkeys == 2:
            new_keys=(rcm[keys[0]],rcm[keys[1]])    
            
        base=hyp.induce_hyperedge_distance(keys,rcm,D)
        
        #if (max(new_keys)-min(new_keys))> diameter:
            #diameter= (max(new_keys)-min(new_keys))
        
        if base<=1:
            base=0
        if base > 1:
            base=2
        
        
        weight=base+random.uniform(0, 1)
        
        temp[new_keys]=weight
        
    
    #return [temp, diameter]
    return [temp, JW]


def reorder_hyperedges_parallel(interactions, rcm, D):
    
    temp={}
    new_keys=()
    weight=1.0
    diameter=oddEvenSort_distance(rcm)
    JW=JW_ordering_cost(rcm)
    
    hyp_distance=partial(hyp.induce_hyperedge_distance, rcm = rcm, D = D)
    #hyp_distance=partial(hyp.induce_hyperedge_distance, D = DM)
    
    new_interactions=[*interactions]
    chunk=int(math.ceil(len(new_interactions)/nProc*1.0))
    results=pool.map(hyp_distance,new_interactions,chunksize=chunk)
    
    count=0
    for keys in interactions.keys():
        
        #keys=new_interactions[i]
        lkeys=len(keys)
        
        if lkeys == 4:
            new_keys=(rcm[keys[0]],rcm[keys[1]],rcm[keys[2]],rcm[keys[3]])
                       
            
        if lkeys == 3:
            new_keys=(rcm[keys[0]],rcm[keys[1]],rcm[keys[2]])    
            
        
        if lkeys == 2:
            new_keys=(rcm[keys[0]],rcm[keys[1]])    
            
        base=results[count]
        
        if base<=1:
            base=0
        if base > 1:
            base=2
        
        
        weight=base+random.uniform(0, 1)
        
        #interactions[new_keys]=interactions.pop(keys)
        #interactions[new_keys]=weight
        temp[new_keys]=weight
        
        count=count+1
    
    #return [interactions,diameter]
    #return [temp, diameter]
    return [temp, JW]

def siman(G,interactions,nVer,D,maxcount=10,maxtemp=3):
    
    bestsol=[]
    sol=[]
    tsol=[]
    
    iteration=nVer*math.log(nVer,2)
    
    if iteration < maxcount:
        maxcount=iteration
    
      
    temp=0
    
    
    #print("Graph: ",G.edges())
    sol=list(reverse_cuthill_mckee_ordering(G))  #rmap
    #print("sol: ",sol)
    
    
    bestsol=reverse_map(sol)  #rcm
    sol=bestsol.copy()
    
    prevDist=evaluate_permutation_parallel(interactions,sol,D)
    #prevDist=evaluate_permutation(interactions,sol,D)
    
    count=0
    while True:

        i=random.randint(0,len(sol)-1)
        j=random.randint(0,len(sol)-1)
        
#        if i<(len(sol)-2):
#            j=i+2
#        else:
#            j=i-2
#        
        tt=sol[i]
        sol[i]=sol[j]
        sol[j]=tt
        
        
        curDist= evaluate_permutation_parallel(interactions,sol,D)
        #curDist= evaluate_permutation(interactions,tsol,D)
        
        gain=prevDist-curDist
        
        if gain >=0 :
            prevDist=curDist
            bestsol=sol.copy()
            if gain > 0:
                count = 0
            else:
                temp=temp+1
            #print(sol, evaluate_etotal(interactions,sol), "\n" )
            #print(bestsol, evaluate_etotal(interactions,bestsol), "\n\n" )
        else:
            #print(count, maxcount)
            count=count+1
        
        if count >= maxcount or temp>=maxtemp :
            break   
    
    return bestsol #rcm
        
    

def HyperAlign(hyperedges,nVer,D,rmap_prev=[]):
    
    G=create_cycle_graph(hyperedges,nVer)
    
    return siman(G,hyperedges,nVer,D)

