# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 19:05:35 2023

@author: Ramon
"""

import copy
import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI
from Ef_Ex_LM import Ef_Ex_LM




    



def derivada_approach(cycle_inputs,delta = 10e-3):
   
    current_x = cycle_inputs['approach_HX']
    cycle_inputs_x = copy.copy(cycle_inputs)
    cycle_inputs_x['approach_HX'] += delta
    current_cycle_x = Ef_Ex_LM(cycle_inputs)
    new_cycle_x = Ef_Ex_LM(cycle_inputs_x)
    dx = (new_cycle_x - current_cycle_x)
    gradient = dx/delta
    
    print(dx)
    print(gradient)
    return dx
  




def SD_approach(cycle_inputs, delta = 10e-4, tol=10e-6, gama = 5):
    deriv = derivada_approach(cycle_inputs)
    while np.abs(deriv) > tol:
        
            x_new = cycle_inputs['approach_HX'] + gama*(deriv/delta)
            cycle_inputs['approach_HX'] = x_new
            deriv = derivada_approach(cycle_inputs)
            print(x_new)
            if cycle_inputs['approach_HX'] > 10:
                break
    return x_new



def derivada_titulo(cycle_inputs,delta = 10e-3):
   
    current_y = cycle_inputs['tit_evap_f']
    current_cycle_y = Ef_Ex_LM(cycle_inputs)
    cycle_inputs_y = copy.copy(cycle_inputs)
    cycle_inputs_y['tit_evap_f'] += delta    
    new_cycle_y = Ef_Ex_LM(cycle_inputs_y)
    
    dy = (new_cycle_y - current_cycle_y)
    gradient = dy/delta
    
    print(dy)
    print(gradient)
    return dy



def SD_titulo(cycle_inputs, delta = 10e-3, tol=10e-04, gama = 0.01):
    deriv = derivada_titulo(cycle_inputs)
    while np.abs(deriv) > tol:
        y_new = cycle_inputs['tit_evap_f'] + gama*(deriv/delta)
        cycle_inputs['tit_evap_f'] = y_new
        deriv = derivada_titulo(cycle_inputs)
        print(y_new)
        
        if cycle_inputs['tit_evap_f'] > 0.55:
            break

    #print(np.abs(func(y_new,cycle_inputs) - 3.8000508794454135))
    return(y_new)    
   

def derivada_superheating(cycle_inputs,delta = 10e-3):
   
    current_z = cycle_inputs['superheating']
    cycle_inputs_z = copy.copy(cycle_inputs)
    cycle_inputs_z['superheating'] += delta
    current_cycle_z = Ef_Ex_LM(cycle_inputs)
    new_cycle_z = Ef_Ex_LM(cycle_inputs_z)
    dz = (new_cycle_z - current_cycle_z)
    gradient = dz/delta
    
    #print(dz)
    #print(gradient)
    return (dz)

def SD_superheating(cycle_inputs, delta = 0.1, tol=10e-12, gama = 50):
    deriv = derivada_superheating(cycle_inputs)
    while np.abs(deriv) > tol:
        
            z_new = cycle_inputs['superheating'] + gama*(deriv/delta)
            cycle_inputs['superheating'] = z_new
            deriv = derivada_superheating(cycle_inputs)
            print(z_new)
            #print(Ef_Ex_LM(cycle_inputs))
            if cycle_inputs['superheating'] > 10:
                break
    return z_new

def derivada_subcooling(cycle_inputs,delta = 10e-3):
   
    current_w = cycle_inputs['subcooling']
    cycle_inputs_w = copy.copy(cycle_inputs)
    cycle_inputs_w['subcooling'] += delta
    current_cycle_w = Ef_Ex_LM(cycle_inputs)
    new_cycle_w = Ef_Ex_LM(cycle_inputs_w)
    dw = (new_cycle_w - current_cycle_w)
    gradient = dw/delta
    
    print(dw)
    print(gradient)
    return (dw)

def SD_subcooling(cycle_inputs, delta = 10e-3, tol=10e-5, gama = 5):
    deriv = derivada_subcooling(cycle_inputs)
    while np.abs(deriv) > tol:
        
            w_new = cycle_inputs['subcooling'] + gama*(deriv/delta)
            cycle_inputs['subcooling'] = w_new
            deriv = derivada_subcooling(cycle_inputs)
            print(w_new)
            if cycle_inputs['subcooling'] < 5:
                break
    return w_new



input_values ={
    't_external':298,
    't_cond': 308,
    't_internal_f':250,
    'Q_ETB':35200, #71 TR
    'N_isent': 0.7,
    'refrigerant':'R410a',
    'tit_evap_f':0.55,
    'subcooling':10,
    'superheating':1,
    'approach_HX':10
}

#(Ef_Ex_LM(input_values))

#derivada_approach(input_values)
#SD_approach(input_values)
#derivada_titulo(input_values)
#SD_titulo(input_values)
#derivada_superheating(input_values)
SD_superheating(input_values)
#derivada_subcooling(input_values)
#SD_subcooling(input_values)