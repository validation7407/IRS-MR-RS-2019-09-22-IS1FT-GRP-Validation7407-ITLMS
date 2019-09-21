
# -*- coding: utf-8 -*-
"""
    Genetic algorithm for traffic light optimization at a single junction.
    
    Single Junction Model.

"""
from pyeasyga import pyeasyga
import numpy as np
import numpy.random as random

direction = 2

start_d = 0 # Define the direction to given green light first 0 = direction 1 , 1 = direction 2

arr = [0.5,0,0.5,0] # Arrival Rates for direction 1 and direction 2

data = np.array([[[25,25],[5,5]], # direction 1 (East-West) [straight traffic, right turning]
                [[15,15],[2,2]]]) # direction 2 (North-South) [straight traffic, right turning]

data = data.flatten()

ga = pyeasyga.GeneticAlgorithm(data,
                               population_size=100,
                               generations=200,
                               crossover_probability=0.8,
                               mutation_probability=0.01,
                               elitism=True,
                               maximise_fitness=False)


def create_individual(data):
    # individuals are list of timings for each direction in each junction, 
    # since traffic in one direction share the same traffic light timing
    
    temp = [random.randint(10, 100) for _ in range(int(len(data)/2))]
#    a = random.randint(0,2)
#    temp.append(a)
    return temp

ga.create_individual = create_individual

def flow(data,individual,road,arr):
    if road ==0: 
        switch = 1
        a1,a1r,a2,a2r = arr
#        a1 = arr_0
#        a2 = arr_1
#        a1r = 0
#        a2r = 0
    else: 
        switch = -1
        a2,a2r,a1,a1r= arr
#        a1 = arr_1
#        a2 = arr_0
#        a1r = 0
#        a2r = 0        
    phase_1 = individual[road][0] / \
                    (sum(data[road][0]) + a1*individual[road][0])*3.5 
    
    phase_2 = individual[road][1] / \
                    (sum(data[road][1]) + a1r*individual[road][0])*3.5 
    
    phase_3 = individual[road+switch][0] / \
                    (a2*sum(individual[road]) + sum(data[road+switch][0]))*3.5
                    
    phase_4 = individual[road+switch][1] / \
                    (sum(data[road+switch][1]) + a2r*(sum(individual[road])+individual[road+switch][1]+individual[road+switch][0]))*3.5 
                    
    if np.min(individual) <= 10:
        value = 1000
    else:
        value = np.sum(abs(np.diff([phase_1,phase_2,phase_3,phase_4])))
    return value

def fitness(individual, data):
    """
        For final value function,
        
        road = 0 if direction1 (EW) goes first, 1 if direction2 (NS) goes first
    """
    values = 0
    data = data.reshape((direction,2,2))
    individual = np.array(individual).reshape((direction,2))
    values = flow(data,individual,start_d,arr) 
    return values

ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
result = ga.best_individual()
print(result)                 # print the GA's best solution

t1 = result[1][0]
t2 = result[1][1]
t3 = result[1][2]
t4 = result[1][3]

#start_d = result[1][2]

start = "Direction 1 (EW)" if start_d == 0 else "Direction 2 (NS)"

print(start,"is given green light first.")
print("Direction 1 (EW) - Straight Timing: ",t1)
print("Direction 1 (EW) - Right-Turn Timing: ",t2)
print("Direction 2 (NS) - Straight Timing: ",t3)
print("Direction 2 (NS) - Right-Turn Timing: ",t4)
