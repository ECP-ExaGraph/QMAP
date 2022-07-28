#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 21:19:55 2018

@author: khan242
"""

import random
import statistics
import matplotlib.pyplot as plt
import os
import scipy as sp
import networkx as nx
from networkx.utils import reverse_cuthill_mckee_ordering
from scipy import io
import community
import matplotlib.pylab as pl
import numpy as np
import math
import itertools

population = []
progress_list = []
# Used to track the iterations
hall_of_fame = []
#contains the best arrangements from each generation



def kendall_tau_distance(order_b):
    order_a=list(range(len(order_b)))
    pairs = itertools.combinations(range(len(order_b)), 2)
    distance = 0
    for x, y in pairs:
        a = order_a.index(x) - order_a.index(y)
        b = order_b.index(x) - order_b.index(y)
        if a * b < 0:
            distance += 1
    return distance




def evaluate_etotal(interactions,rcm):
    etotal = 0
    maxtotal=0
    ktotal=kendall_tau_distance(rcm)
    for keys in interactions.keys():
        
        #new_keys=(rcm[keys[0]],rcm[keys[1]],rcm[keys[2]],rcm[keys[3]])
        new_keys=(rcm[keys[0]],rcm[keys[1]])
        dist=abs(min(new_keys)-max(new_keys))
        if dist > maxtotal:
            maxtotal=dist
            
        etotal=etotal+ dist
    
    
    etotal=0.2*etotal+0.7*maxtotal+0.1*ktotal
    
    return etotal  


def generate_population(network_size, population_size):
    test_phenotype = []

    for i in range(network_size ):
        test_phenotype.append(i)
    for i in range(1,population_size):
        random.shuffle(test_phenotype)
        population.append(list(test_phenotype))
    
    population.append(list(range(network_size)))
    #print(population)
    
def survive_and_reproduce(interactions, network_size, end=False):
    population_fitness = []

    for phenotype in population:
        phenotype_fitness = evaluate_etotal(interactions,phenotype)
        population_fitness.append(phenotype_fitness)

    if len(progress_list) > 0:
        if min(population_fitness) < min(progress_list):
        
            progress_list.append(min(population_fitness))
            min_location = population_fitness.index(min(population_fitness))
            hall_of_fame.append(population[min_location])
            #print(population[min_location],min(population_fitness))
            #print(hall_of_fame)
    else:
            progress_list.append(min(population_fitness))
            min_location = population_fitness.index(min(population_fitness))
            hall_of_fame.append(population[min_location])
            #print(population[min_location],min(population_fitness))
            #print(hall_of_fame)
    # Add the generation’s champion to the progress_list

    if end:
        champion_location = progress_list.index(min(progress_list))
        #print("The optimal arrangement is: ",hall_of_fame[champion_location],", with an etotal of: ",kendall_tau_distance(hall_of_fame[champion_location]))
        return hall_of_fame[champion_location]
        # We print the overall best arrangement, and its etotal.
    
    median = statistics.median(population_fitness)
    #print(median)
    elements_to_remove = []

    for i in range(0, len(population)):
        if population_fitness[i] > median:
            elements_to_remove.append(i)
    
    
    survivors = [i for j, i in enumerate(population) if j not in elements_to_remove]
    number_removed = len(elements_to_remove)
    next_generation = survivors
    
    for i in range(0, number_removed):
        parent = random.choice(survivors)
        estranged_father = parent[int(network_size / 2):network_size]
        random.shuffle(estranged_father)
        child = parent[0:int(network_size / 2)] + estranged_father
        next_generation.append(child)

    return next_generation


def mutate(generation,network_size):
    mutation_rate = 0.05
    
    for i in range(0, len(generation)):
        if random.random() < mutation_rate:
            to_swap = random.sample(range(network_size), 2)
            a, b = to_swap[0], to_swap[1]
            generation[i][b], generation[i][a] =  generation[i][a], generation[i][b]



def HOLA(interactions, num_orbitals,plotting=False):
    
    network_size=num_orbitals
    
    population_size=network_size ** 2
    gen_number = 20 # the number of iterations
    population = []
    
    generate_population(network_size, population_size)

    for i in range(0, gen_number + 1):
        if i != gen_number:
            next_generation = survive_and_reproduce(interactions,network_size)
            mutate(next_generation,network_size)
            population = next_generation
        else:
            rcm=survive_and_reproduce(interactions,network_size,True)
        # On the last iteration, we print the overall winner

    if plotting:
        
        plt.plot(progress_list)
        plt.title("Evolution of etotal")
        plt.xlabel("Generation number")
        plt.ylabel("r’$\epsilon$ total")
        plt.axis([0, gen_number, 0, 1.3*min(progress_list)])
        #plt.savefig(’etotal_graph.png’)
    
    return rcm
