# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:54:57 2019

@author: kartik
"""

from pyke import knowledge_engine
from pyke import goal

engine = knowledge_engine.engine(".\pyke")

jn = goal.compile('try.junction_number($num)')

#a = my_goal.prove_1(engine)

#a = engine.prove_1_goal('try.junction_category($lanes)')
#print(a[0]['lanes'])

#b = engine.prove_1_goal('try.junction_number($num)')
#print(b[0]['num'])

#junctions = int(input("Enter the number of junctions: "))

temp = engine.prove_1_goal('try.junction_number($num)')
junctions = temp[0]['num']



lanes = []   
c = []
cars_str = []
cars_rt = []

for i in range(1, junctions + 1):
    print("For junction "+ str(i) +" ")
    engine = knowledge_engine.engine("C:\\pyke")
    sl = goal.compile('try.straight_lane($sl)')
    temp = sl.prove_1(engine)
    a = temp[0]['sl']
    #int(input("For junction "+ str(i) +", Enter number of straight lanes: "))
    for j in range(0,a):
        print("For straight lane " + str(j+1) + ": ")
        engine = knowledge_engine.engine("C:\\pyke")
        csl = goal.compile('try.cars_straight_lane($csl)')
        temp = csl.prove_1(engine)
        temp1 = temp[0]['csl']
        
        
        #c.append(int(input("Enter cars in Straight lane " + str(j+1) + ": ")))
        c.append(temp1)
    cars_str.append(c)
    c = [] 
    engine = knowledge_engine.engine("C:\\pyke")
    rl = goal.compile('try.right_lane_there($yn)')
    temp = rl.prove_1(engine)
    r = temp[0]['yn']
    if r == "Y" or r == "y":
    	engine = knowledge_engine.engine("C:\\pyke")
    	crl = goal.compile('try.cars_right_lane($crl)')
    	temp = crl.prove_1(engine)
    	temp1 = temp[0]['crl']
    	#c.append(int(input("Enter cars in Right lane : ")))
    	c.append(temp1)
    	cars_rt.append(c)
    	c = []
    	b = 1
    else:
        b = 0
        c.append(0)
        cars_rt.append(c)
        c = []
    lanes.append((a,b))


b1 = 25
b2 = 25
b3 = 15
m = 3.5

total_cars = []

for i in range(0,len(cars_str)):
    tc = sum(cars_str[i])+ sum(cars_rt[i])
    total_cars.append(tc)

for i in range(0,len(cars_str)):
    max_cars = max(cars_str[i])    
    if len(cars_str[i]) >= 3:
        penalty = (sum([x for k,x in enumerate(total_cars) if k!=i])/
                   (sum([len(x) for k,x in enumerate(cars_str) if k!=i])+
                    sum([len(x) for k,x in enumerate(cars_rt) if k!=i and x[0]!=0])))
        bias = 25
        t = (max_cars*m + bias) - penalty 
        print("Time : ",round(t,2))
       # print(penalty)
    else:
        penalty = 5
        bias = 15
        t = (max_cars*m + bias) - penalty 
        print("Time : ",round(t,2))
        #print(penalty)
        
