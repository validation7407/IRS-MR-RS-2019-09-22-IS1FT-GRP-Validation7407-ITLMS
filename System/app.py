# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:54:57 2019

@author: kartik
"""

from pyke import knowledge_engine
from flask import Flask
from flask import request
from flask import render_template
        
from pyeasyga import pyeasyga
import numpy as np
import numpy.random as random

import os

abspath = os.path.abspath("app.py")
dname = os.path.dirname(abspath)
os.chdir(dname)

# Rule Based Timing Assignment
#.................................................................................
engine = knowledge_engine.engine(".\pyke1")

def junc(infunc = engine.prove_1_goal):
    junctions = infunc('try.junction_number($num)')
    return junctions


def str_lane(infunc = engine.prove_1_goal):
    st_lanes = infunc('try.junction_number($num)')
    return st_lanes

def str_lane_cars(infunc = engine.prove_1_goal):
    st_lane_cars = infunc('try.straight_lane($sl)')
    return st_lane_cars

def rt_lane(infunc = engine.prove_1_goal):
    rt_lanes = infunc('try.right_lane_there($yn)')
    return rt_lanes

def rt_lane_cars(infunc = engine.prove_1_goal):
    rt_lane_cars = infunc('try.cars_right_lane($crl)')
    return rt_lane_cars

def junction_rules(lanes):
     if lanes <=2:
          junction_size = 'small'
     else:
          junction_size = 'big'
     if junction_size == 'small':
          bias = 15
     else:
          bias = 25
     return(junction_size,bias)


def calculate(result):
    lanes = []   
    c = []
    cars_str = []
    cars_rt = []
    if result['jlist']=='4way':
        junctions = junc(lambda prompt : 4) #FETCHED VALUE FROM HTML
        pre = 'd'
    else:
        junctions = junc(lambda prompt : 3)
        pre = 'td'
    for i in range(1, junctions+1):
        #print("For junction "+ str(i) +" ")
        engine = knowledge_engine.engine(".\pyke1")
        lanes_st = str_lane(lambda prompt : result[pre +str(i)+'lanes']) #FETCHED VALUE FROM HTML
        
        cars = result[pre+str(i)+'cars'].split(',')
        #print(cars)
        
        for j in range(0,int(lanes_st)):
            
            engine = knowledge_engine.engine(".\pyke1")
            temp1 = str_lane_cars(lambda prompt : int(cars[j])) #FETCHED VALUE FROM HTML
            
            c.append(temp1)
            
        cars_str.append(c)
        c = [] 
        engine = knowledge_engine.engine(".\pyke1")
        r = rt_lane(lambda prompt : result[pre+str(i)+'right']) #FETCHED VALUE FROM HTML
        if r != 0:
            engine = knowledge_engine.engine(".\pyke1")
            temp1 = rt_lane_cars(lambda prompt : result[pre+str(i)+'right']) #FETCHED VALUE FROM HTML
            c.append(int(temp1))
            cars_rt.append(c)
            c = []
            lanes_rt = 1
        else:
            lanes_rt = 0
            c.append(0)
            cars_rt.append(c)
            c = []
        lanes.append((lanes_st,lanes_rt))
    
    
    
    m = 3.5
    
    total_cars = []
    
    for i in range(0,len(cars_str)):
        tc = sum(cars_str[i])+ sum(cars_rt[i])
        total_cars.append(tc)
        
    
    st_time = []
    #print(len(cars_str))
    for i in range(0,len(cars_str)):
        
        max_cars = max(cars_str[i])
        res = junction_rules(int(result[pre + str(i+1) + 'lanes']))
        #print(res)
        if res[0] == 'big':
            penalty = (sum([x for k,x in enumerate(total_cars) if k!=i])/
                       (sum([len(x) for k,x in enumerate(cars_str) if k!=i])+
                        sum([len(x) for k,x in enumerate(cars_rt) if k!=i and x[0]!=0])))
            bias = res[1]
            ts = (max_cars*m + bias) - penalty
            st_time.append(ts)
            
        elif res[0] == 'small':
            penalty = 5
            bias = res[1]
            ts = (max_cars*m + bias) - penalty
            
            st_time.append(ts)
            
    rt_time = []
    
    #print(st_time)
    if junctions == 3:
        print(junctions)
        tr = 0
        i = 0
        if st_time[i] < st_time[i+1]:
            tr = cars_rt[i][0]*m
            rt_time.append(tr)
        elif st_time[i] >= st_time[i+1] and cars_rt[i][0]*m!=0:
            if cars_rt[i][0]*m < st_time[i] - st_time[i+1]: 
                tr = st_time[i] - st_time[i+1]
            else:
                tr = (cars_rt[i][0] - (st_time[i] - st_time[i+1])/m)*m
            rt_time.append(tr)
        
        print("Time Straight: ",round(max(st_time[0],st_time[1]),2),"Time Right: ",round(rt_time[0],2))
        print("Time Straight: ",round(st_time[2],2),"Time Right: ",round(0,2))
        
        return (st_time,rt_time,junctions)
       
    
    elif junctions == 4:
        print(junctions)
        for i in range(0,len(st_time),2):
            tr = 0
            max_rcars = max(cars_rt[i][0],cars_rt[i+1][0])
            if st_time[i] < st_time[i+1]:
                tr = max_rcars*m
                rt_time.append(tr)
            elif st_time[i] >= st_time[i+1] and cars_rt[i][0]*m!=0:
                if max_rcars*m < st_time[i] - st_time[i+1]: 
                    tr = st_time[i] - st_time[i+1]
                else:
                    tr = (max_rcars - (st_time[i] - st_time[i+1])/m)*m
                rt_time.append(tr)
                
        print("Time Straight: %4.2f" % round(max(st_time[0],st_time[1]),2),"Time Right: %4.2f" % round(rt_time[0]))
        print("Time Straight: %4.2f" % round(max(st_time[2],st_time[3]),2),"Time Right: %4.2f" % round(rt_time[1]))
        
        return (st_time,rt_time,junctions)

#.................................................................................
#
# Genetic Algorithm Functions

def get_data(result):
    junction_type = 4 if result['jlist'] == "4way" else 3
    
    rates_t = ['td1rate','td2rate','td3rate']
    
    cars_t = ['td1cars','td2cars','td1right','td2right',
            'td3cars','td3right']    
    
    rates = ['d1rate','d2rate','d3rate','d4rate']
    
    cars = ['d1cars','d2cars','d1right','d2right',
            'd3cars','d4cars','d3right','d4right']
    
    if junction_type == 3:
        arr = [float(result.get(key)) for key in rates_t].append(0)
        data = [result.get(key).split(',') for key in cars_t]
        data.insert(5,[0])
        data.insert(7,[0])
    else:
        arr = [float(result.get(key)) for key in rates]
        data = [result.get(key).split(',') for key in cars]
    temp = []
    for i in data:
        d = 0
        for j in i:
            d += int(j)
        temp.append(d)
    data = np.array(temp)
    
    return (data,arr,junction_type)

def create_individual(data):
    # individuals are list of timings for each direction in each junction, 
    # since traffic in one direction share the same traffic light timing
    
    temp = [random.randint(5, 80) for _ in range(int(len(data[0])/2))]
    return temp

def flow(data,individual,road,arr,junction_type):
    if road ==0: 
        switch = 1
        a1,a1r,a2,a2r = arr
    else: 
        switch = -1
        a2,a2r,a1,a1r= arr
        
    phase_1 = individual[road][0] / \
                    (np.max(data[road][0]) + a1*individual[road][0])*3.5
    
    phase_2 = individual[road][1] / \
                    (np.max(data[road][1]) + a1r*individual[road][0])*3.5 
    
    phase_3 = individual[road+switch][0] / \
                    (np.max(data[road+switch][0]) + a2*sum(individual[road]))*3.5
                    
    if junction_type == 4:                
        phase_4 = individual[road+switch][1] / \
                        (np.max(data[road+switch][1]) + a2r*(np.max(individual[road])+individual[road+switch][1]+individual[road+switch][0]))*3.5 
        value = np.mean(abs(np.diff([phase_1,phase_2,phase_3,phase_4]))**2)
    else:
        value = np.mean(abs(np.diff([phase_1,phase_2,phase_3]))**2)       
    
    if np.min(individual) <= 5:
        value = 1000
        
    return value

def fitness(individual, data):
    """
        For final value function,
        
        road = 0 if direction1 (EW) goes first, 1 if direction2 (NS) goes first
    """
    values = 0
    arr = data[1]
    junction_type = data[2]
    data = data[0]
    data = data.reshape((2,2,2))
    individual = np.array(individual).reshape((2,2))
    values = flow(data,individual,0,arr,junction_type) 
    return values

def run_ga(data):    
    ga = pyeasyga.GeneticAlgorithm(data,
                                   population_size=100,
                                   generations=200,
                                   crossover_probability=0.8,
                                   mutation_probability=0.05,
                                   elitism=True,
                                   maximise_fitness=False)

    ga.create_individual = create_individual
    
    ga.fitness_function = fitness               # set the GA's fitness function
    ga.run()                                    # run the GA
    result = ga.best_individual()
    
    t1 = result[1][0]
    t2 = result[1][1]
    t3 = result[1][2]
    t4 = result[1][3]
    
    print(result)                 # print the GA's best solution
    return(t1,t2,t3,t4)

#.................................................................................



app = Flask(__name__)

@app.route('/')
def my_form():
#	colnames = temp.columns
	return render_template("index.html")


@app.route('/',methods=['POST'])
def generate():
    print("SUBMITTED")
    result = request.form
    
    st_time, rt_time, junctions = calculate(result)
    
    data = get_data(result)
    
    t1,t2,t3,t4 = run_ga(data)
    
    if junctions == 4:
        print(st_time, rt_time, junctions)
        return render_template("result.html",time_1 = round(max(st_time[0],st_time[1]),2), time_2 = round(rt_time[0]),
                           time_3 = round(max(st_time[2],st_time[3]),2), time_4 = round(rt_time[1]),
                           tga_1=t1,tga_2=t2,tga_3=t3,tga_4=t4,junctions=junctions) 
    else:
         print(st_time, rt_time, junctions)
         return render_template("result.html",time_1 = round(max(st_time[0],st_time[1]),2), time_2 = round(rt_time[0]),
                           time_3 = round(st_time[2],2),tga_1=t1,tga_2=t2,tga_3=t3,junctions=junctions)    

@app.route('/result.html',methods=['POST'])
def return_home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
    
