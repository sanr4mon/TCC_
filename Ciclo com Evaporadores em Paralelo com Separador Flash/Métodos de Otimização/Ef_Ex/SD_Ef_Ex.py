# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 21:59:42 2023

@author: Ramon
"""

import copy
import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI
from Ef_Ex_Paralelo_Separador import Ef_Ex_Paralelo_Sep



def func(x,cycle_inputs):
    cycle_inputs['r'] = x
    
    return Ef_Ex_Paralelo_Sep(cycle_inputs)
    



def derivada_razao(cycle_inputs,delta = 10e-3):
   
    current_x = cycle_inputs['r']
    cycle_inputs_x = copy.copy(cycle_inputs)
    cycle_inputs_x['r'] += delta
    current_cycle_x = Ef_Ex_Paralelo_Sep(cycle_inputs)
    new_cycle_x = Ef_Ex_Paralelo_Sep(cycle_inputs_x)
    dx = (new_cycle_x - current_cycle_x)
    gradient = dx/delta
    
    print(dx)
    print(gradient)
    return dx
  




def SD_razao(cycle_inputs, delta = 10e-3, tol=10e-6, gama = 1):
    deriv = derivada_razao(cycle_inputs)
    while np.abs(deriv) > tol:
        
            x_new = cycle_inputs['r'] + gama*(deriv/delta)
            cycle_inputs['r'] = x_new
            deriv = derivada_razao(cycle_inputs)
            print(x_new)
            if cycle_inputs['r'] > 2:
                break
    return x_new



def derivada_T(cycle_inputs,delta = 10e-3):
   
    current_y = cycle_inputs['t_internal_g']
    cycle_inputs_y = copy.copy(cycle_inputs)
    cycle_inputs_y['t_internal_g'] += delta
    current_cycle_y = Ef_Ex_Paralelo_Sep(cycle_inputs)
    new_cycle_y = Ef_Ex_Paralelo_Sep(cycle_inputs_y)
    dy = (new_cycle_y - current_cycle_y)
    gradient = dy/delta
    
    print(dy)
    print(gradient)
    return dy
  



def SD_T(cycle_inputs, delta = 10e-3, tol=10e-05, gama = 5):
    deriv = derivada_T(cycle_inputs)
    while np.abs(deriv) > tol:
        y_new = cycle_inputs['t_internal_g'] + gama*(deriv/delta)
        cycle_inputs['t_internal_g'] = y_new
        deriv = derivada_T(cycle_inputs)
        print(y_new)
        
        if cycle_inputs['t_internal_g'] < 268:
            break
    
        

    #print(np.abs(func(y_new,cycle_inputs) - 3.8000508794454135))
    return(y_new)    
   

def derivada_superheating(cycle_inputs,delta = 10e-2):
   
    current_w = cycle_inputs['superheating']
    cycle_inputs_z = copy.copy(cycle_inputs)
    cycle_inputs_z['superheating'] += delta
    current_cycle_z = Ef_Ex_Paralelo_Sep(cycle_inputs)
    new_cycle_z = Ef_Ex_Paralelo_Sep(cycle_inputs_z)
    dz = (new_cycle_z - current_cycle_z)
    gradient = dz/delta
    
    print(dz)
    print(gradient)
    return (dz)

def SD_superheating(cycle_inputs, delta = 10e-3, tol=10e-5,gama = 5):
    deriv = derivada_superheating(cycle_inputs)
    while np.abs(deriv) > tol:
        
            z_new = cycle_inputs['superheating'] + gama*(deriv/delta)
            cycle_inputs['superheating'] = z_new
            deriv = derivada_superheating(cycle_inputs)
            print(z_new)
            if cycle_inputs['superheating'] < 1:
                break
    return z_new

def derivada_subcooling(cycle_inputs,delta = 10e-3):
   
    current_w = cycle_inputs['subcooling']
    cycle_inputs_w = copy.copy(cycle_inputs)
    cycle_inputs_w['subcooling'] += delta
    current_cycle_w = Ef_Ex_Paralelo_Sep(cycle_inputs)
    new_cycle_w = Ef_Ex_Paralelo_Sep(cycle_inputs_w)
    dw = (new_cycle_w - current_cycle_w)
    gradient = dw/delta
    
    print(dw)
    print(gradient)
    return (dw)

def SD_subcooling(cycle_inputs, delta = 10e-3, tol=10e-6, gama = 5):
    deriv = derivada_subcooling(cycle_inputs)
    while np.abs(deriv) > tol:
        
            w_new = cycle_inputs['subcooling'] + gama*(deriv/delta)
            cycle_inputs['subcooling'] = w_new
            deriv = derivada_subcooling(cycle_inputs)
            print(w_new)
            if cycle_inputs['subcooling'] > 10:
                break
    return w_new



input_values ={
    't_external':298,
    't_cond': 308,
    't_internal_f':250,
    't_internal_g':278,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R410A',
    'r':1.5,
    'subcooling':5,
    'superheating':5
}



#derivada_razao(input_values)
#SD_razao(input_values)
#derivada_T(input_values)
#SD_T(input_values)
#derivada_superheating(input_values)
#SD_superheating(input_values)
#derivada_subcooling(input_values)
SD_subcooling(input_values)