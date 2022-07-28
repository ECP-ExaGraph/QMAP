#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 15:28:45 2018

@author: khan242
"""

import networkx as nx
import numpy as np
from itertools import permutations

def hypergraph_matching(interactions,nVer):
    
     
    hEdges=sorted(interactions, key=interactions.__getitem__)
    hVers=[0]*nVer
    m=[]
    qcount=0
    for i in range(len(hEdges)):
        edge=hEdges[i]
        l=len(edge)
        flag=0
        for j in range(l):
            if hVers[edge[j]]==1:
                flag=1
                break
        if flag == 1:
            continue
        else:
            if interactions[edge]<=2:
                m.append(edge)
                for j in range(l):
                    hVers[edge[j]]=1
                qcount=qcount+l
    return m,qcount

def create_clique_graph(hyperedges, nVer):
    
    G=nx.Graph()
    G.add_nodes_from(range(nVer))
    
    for tkeys in hyperedges.keys():
        
        keys=set(tkeys)
        keys=tuple(keys)
        keys=sorted(keys)
        
        
        if len(keys)<=1:
            continue
        if len(keys) > 2:
            for i in range(len(keys)):
                for j in range((i+1),len(keys)):
                    G.add_edge(keys[i],keys[j],weight=1)
        else:
            G.add_edge(keys[0],keys[1],weight=1)
             
    
    return G

def all_pair_shortest_path(hyperedges,nVer):
    D=np.ones((nVer,nVer))*nVer*5
    
    G=create_clique_graph(hyperedges,nVer)
    
    path=dict(nx.all_pairs_shortest_path_length(G))
    
    
    for i in range(len(path)):
        for j in path[i].keys():
            D[i][j]=path[i][j]
    
    #print(D)
    return D

    
def get_distance(hyperedge,D):
    
    dist=0
    length=len(hyperedge)
    pairs=(length*(length-1))/2
    
    #print(hyperedge)
    
    if length == 2:
        dist=D[hyperedge[0]][hyperedge[1]]
        
        
    if length == 3:
        dist=dist+D[hyperedge[0]][hyperedge[1]]
        dist=dist+D[hyperedge[1]][hyperedge[2]]
        dist=dist+(D[hyperedge[0]][hyperedge[2]])/2
        
        
    if length == 4:
        dist=dist+D[hyperedge[0]][hyperedge[1]]
        dist=dist+D[hyperedge[1]][hyperedge[2]]
        dist=dist+D[hyperedge[2]][hyperedge[3]]
        dist=dist+(D[hyperedge[0]][hyperedge[2]])/2
        dist=dist+(D[hyperedge[1]][hyperedge[3]])/2
        dist=dist+(D[hyperedge[0]][hyperedge[3]])/3 
             
    #print(dist/pairs)
    return dist/pairs


def induce_hyperedge_distance(hyperedge,rcm,D):
    
    new_edge=[]
    hyperedge=tuple(set(hyperedge))
    
    for e in hyperedge:
        new_edge.append(rcm[e])
    
    hyperedge=tuple(set(new_edge))
    
    permute=list(permutations(hyperedge))
    dist=[]
    
    for p in permute:
        dist.append(get_distance(p,D))
    
    return min(dist)
    

