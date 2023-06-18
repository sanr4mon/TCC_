# -*- coding: utf-8 -*-
"""
Created on Wed May 31 08:48:17 2023

@author: Ramon
"""

import copy
import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI
from COP_Duplo_Estagio import COP_Duplo_Estagio



def func(x,cycle_inputs):
    cycle_inputs['t_internal_g'] = x
    
    return COP_Duplo_Estagio(cycle_inputs)
    



def derivada_T(cycle_inputs,delta = 10e-3):
   
    current_x = cycle_inputs['t_internal_g']
    cycle_inputs_x = copy.copy(cycle_inputs)
    cycle_inputs_x['t_internal_g'] += delta
    current_cycle_x = COP_Duplo_Estagio(cycle_inputs)
    new_cycle_x = COP_Duplo_Estagio(cycle_inputs_x)
    dx = (new_cycle_x - current_cycle_x)
    gradient = dx/delta
    
    print(dx)
    print(gradient)
    return dx
  




def SD_T(cycle_inputs, delta = 10e-3, tol=10e-5, gama = 5):
    deriv = derivada_T(cycle_inputs)
    while deriv > tol:
        
            x_new = cycle_inputs['t_internal_g'] + gama*(deriv/delta)
            cycle_inputs['t_internal_g'] = x_new
            deriv = derivada_T(cycle_inputs)
            print(x_new)
            if cycle_inputs['t_internal_g'] > 278:
                break
    return x_new



def derivada_titulo(cycle_inputs,delta = 10e-3):
   
    current_y = cycle_inputs['tit_evap_g']
    current_cycle_y = COP_Duplo_Estagio(cycle_inputs)
    cycle_inputs_y = copy.copy(cycle_inputs)
    cycle_inputs_y['tit_evap_g'] += delta    
    new_cycle_y = COP_Duplo_Estagio(cycle_inputs_y)
    
    dy = np.abs((new_cycle_y - current_cycle_y))
    gradient = dy/delta
    
    print(dy)
    print(gradient)
    return dy


Y = []
COP_opt = []

def SD_titulo(cycle_inputs, delta = 10e-3, tol=10e-03, gama = 0.001):
    deriv = derivada_titulo(cycle_inputs)
    while deriv > tol:
        #while cycle_inputs['Tit_evap_g'] < 0.65:
        y_new = cycle_inputs['tit_evap_g'] + gama*(deriv/delta)
        cycle_inputs['tit_evap_g'] = y_new
        deriv = derivada_titulo(cycle_inputs)
        print(y_new)
        
        if cycle_inputs['tit_evap_g'] > 0.65:
            break

    #print(np.abs(func(y_new,cycle_inputs) - 3.8000508794454135))
    return(y_new)    
   

def derivada_superheating(cycle_inputs,delta = 10e-3):
   
    current_z = cycle_inputs['superheating']
    cycle_inputs_z = copy.copy(cycle_inputs)
    cycle_inputs_z['superheating'] += delta
    current_cycle_z = COP_Duplo_Estagio(cycle_inputs)
    new_cycle_z = COP_Duplo_Estagio(cycle_inputs_z)
    dz = (new_cycle_z - current_cycle_z)
    gradient = dz/delta
    
    print(dz)
    print(gradient)
    return (dz)

def SD_superheating(cycle_inputs, delta = 10e-3, tol=10e-6, gama = 10):
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
    current_cycle_w = COP_Duplo_Estagio(cycle_inputs)
    new_cycle_w = COP_Duplo_Estagio(cycle_inputs_w)
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
            if cycle_inputs['subcooling'] > 10:
                break
    return w_new



input_values = {
    't_external': 293,
    't_cond': 303,
    't_internal_g': 270,
    't_internal_f': 250,
    'Q_ETB': 35200,  # 10 TR
    'N_isent': 0.7,
    'refrigerant': 'R717',
    # 'P_ETB':100000,#100 kPa
    'tit_evap_g': 0.35,
    'subcooling': 5,
    'superheating': 5
}


#derivada_T(input_values)
#SD_T(input_values)
#derivada_titulo(input_values)
#SD_titulo(input_values)
#derivada_superheating(input_values)
#SD_superheating(input_values)
#derivada_subcooling(input_values)
#SD_subcooling(input_values)