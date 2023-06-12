# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:21:58 2023

@author: Ramon
"""

import copy
import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI
from COP_Evaporadores_Paralelo import COP_Evap_Paralelo

input_values ={
    't_external': 298,
    't_cond':308,
    't_internal_f':250,
    't_internal_g':273,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R600A',
    'subcooling':5,
    'superheating':5,
    'approach_HX':5,
    'r':1.5,
    'tit_evap_f':0.6
}


def func_fx(x,y,cycle_inputs):
    cycle_inputs[y] = x
    fx = COP_Evap_Paralelo(cycle_inputs)
    #print (fx)
    return(fx)

def check_pos(x1,x2):
    if x2<x1:
        label='right'
    else:
        label=''
    
    #print(label)
    return(label)


def update_interior(xl,xu):
    D = 0.618*(xu-xl)
    x1 = xl + D
    x2 = xu - D
    
    #print(x1,x2)
    return(x1,x2)

def find_max(cycle_inputs,xl,xu,x1,x2,y,label):
    fx1 = func_fx(x1,y,cycle_inputs)
    fx2 = func_fx(x2,y,cycle_inputs)
    
    if fx2>fx1  and label =='right':
        xl = xl
        xu = x1
        new_x  = update_interior(xl,xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x2
    
    else:
        xl = x2
        xu = xu
        new_x = update_interior(xl,xu)
        x1 = new_x[0]
        x2 = new_x[1]
        xopt = x1
    
    #print(xl,xu,xopt)
    return(xl,xu,xopt)
    
def golden(cycle_inputs,xl,xu,y,et):
    it = 0
    e=1
    
    while e>et:
        new_x = update_interior(xl,xu)
        x1 = new_x[0]
        x2 = new_x[1]
        fx1 = func_fx(x1,y,cycle_inputs)
        fx2 = func_fx(x2,y,cycle_inputs)
        label = check_pos(x1,x2)
        
        new_boundary = find_max(cycle_inputs,xl,xu,x1,x2,y,label)
        
        xl = new_boundary[0]
        xu = new_boundary[1]
        xopt = new_boundary[2]
        cycle_inputs[y] = xopt
        
        it+=1
        #print(it)
        R = 0.618
        e = ((1-R)*(np.abs((xu-xl)/xopt)))
        #print(e)
        print(xopt)
        #print(it)


#golden(input_values,0.35,0.65,'tit_evap_f',0.0001)
#golden(input_values,1,10,'subcooling',0.0001)
#golden(input_values,1,10,'superheating',0.0001)
golden(input_values,1,2,'r',0.0001)