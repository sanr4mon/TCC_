# -*- coding: utf-8 -*-
"""
Created on Sat May 20 10:04:49 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI



#Cálculo das Propriedades Termodinâmicas

def propriedades(ponto):
    variaveis=['T','P','HMASS','SMASS','Q','C']
    input_var=list(ponto.keys())
    output_var=[variable for variable in variaveis if variable not in input_var]
    outputs=PropsSI(output_var,input_var[0],ponto[input_var[0]],input_var[1],ponto[input_var[1]],ponto['refrigerant'])

    for index,variable in enumerate(output_var):
        ponto[variable]=outputs[index]
        
input_values ={
    't_external':298,
    't_cond': 308,
    't_internal_f':250,
    'Q_ETB':35200, #71 TR
    'N_isent': 0.7,
    'refrigerant':'R410A',
    'tit_evap_f':0.55,
    'subcooling':10,
    'superheating':10,
    'approach_HX':10
}


def COP_LM(cycle_inputs):
    
    #Pós Condensador
    
    P_Evap = PropsSI("P","Q",1,"T",250,cycle_inputs['refrigerant'])
    
    point_3 = {'Q':0,'T':cycle_inputs['t_cond'] - cycle_inputs['subcooling'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_3)
    
    #Pós TCAT - resfriando
    point_4 = {'P':point_3['P'],'T':point_3['T'] - cycle_inputs['approach_HX'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_4)
    
    #Pós TCBT - resfriando
    point_5 = {'P':point_3['P'],'T':point_4['T'] - cycle_inputs['approach_HX'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_5)
    
    
    #Evap. Freezer
    
    point_6 = {'HMASS':point_5['HMASS'],'P':P_Evap,'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_6)

    #print("temp.ponto 6 =",point_6['T'])
 
    
    point_7 = {'P':P_Evap,'Q':cycle_inputs['tit_evap_f'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_7)
    
    #print('temp.7 = ',point_7['T'])
    #print('pressao 7 = ',point_7['P'])
    
    
    
    #Pós TCBT - aquecendo
    point_8 = {'P':P_Evap,'T':point_7['T'] + cycle_inputs['approach_HX'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_8)
    #print('temp.8 =',point_8['T'])
    
    #Evaporador da Geladeira
    
    point_9 = {'P':P_Evap,'T':point_8['T'] + cycle_inputs['superheating'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_9)
    
    #print('temp. 9',point_9['T'])
    
    #Compressor
    
    point_1 = {'T':point_9['T'] + cycle_inputs['approach_HX'],'P':P_Evap,'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_1)
    #print('titulo 1:',point_1['Q'])
    #print('temp. 1 =',point_1['T'])
    
    point_2s = {'P':point_3['P'],'SMASS':point_1['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2s)
    
    point_2 = {'P':point_3['P'],'HMASS':point_1['HMASS'] + ((point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent']),'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2)
    
    #Descobrindo vazão mássica
    
    m = cycle_inputs['Q_ETB']/(point_7['HMASS'] - point_6['HMASS'])
    #print(m)
    #Descobrindo potência da geladeira
    
    Q_ETI = m*(point_9['HMASS'] - point_8['HMASS'])
    
    #Descobrindo trabalho do compressor
    
    work =  m*(point_2['HMASS'] - point_1['HMASS'])
    
    #Calculando COP
    
    COP = (cycle_inputs['Q_ETB'] + Q_ETI)/work
    
    print("COP",COP)
    return COP
    


    
COP_LM(input_values)
