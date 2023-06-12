# -*- coding: utf-8 -*-
"""
Created on Sat May 20 11:14:58 2023

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
    't_external': 298,
    't_cond':308,
    't_internal_f':250,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R410A',
    'variacao_titulo_f':0.6,
    'subcooling':5,
    'superheating':5,
    'approach_HX':5,
    'r':1.5
}



def COP_Evap_Serie(cycle_inputs):
    
    P_Evap = PropsSI("P","T",cycle_inputs['t_internal_f'],"Q",1,cycle_inputs['refrigerant'])
    
    #Pós Condensador
    point_3 = {'Q':0,'T':cycle_inputs['t_cond']-cycle_inputs['subcooling'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_3)
    
    #print("Pressão dos Evaporadores, Pressão de Condensação:",P_Evap,point_3['P'])
    
    
    #Pós HX
    point_4a = {'T':point_3['T']-cycle_inputs['approach_HX'],'P':point_3['P'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_4a)
    
    point_4b = {'T':point_3['T']-cycle_inputs['approach_HX'],'P':point_3['P'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_4b)
    
    #Dispositivo de Expansão 1 e Evaporador da Geladeira
    point_5a = {'P':P_Evap,'HMASS':point_4a['HMASS'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_5a)
    #print('temp. 5a',point_5a['T'])
    #print('titulo 5a',point_5a['Q'])
    
    point_6a = {'P':P_Evap,'Q':point_5a['Q']+cycle_inputs['variacao_titulo_f'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_6a)
    #print('temp. 6a',point_6a['T'])
    
    
    
    #Descobrindo vazão mássica m2
    m2 = cycle_inputs['Q_ETB']/(point_6a['HMASS'] - point_5a['HMASS'])
    m3 = m2 / cycle_inputs['r']
    m1 = m2 + m3
    #print(m1,m2,m3)
    
        
    #Dispositivo de Expansão 2
    point_5b = {'P':P_Evap,'HMASS':point_4b['HMASS'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_5b)
    #print('temp 5b',point_5b['T'])

    
    #Evaporador do Freezer
    h7 = (m3*point_5b['HMASS'] + m2*point_6a['HMASS'])/m1
    
    point_7 = {'P':P_Evap,'H':h7,'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_7)
    
    #print('temp. 7',point_7['T']) #praticamente igual a T5b
    
    point_8 = {'T':point_7['T'] + cycle_inputs['superheating'],'P':P_Evap,'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_8) 
    #print('titulo 8',point_8['Q'])
    #print('temp. 8',point_8['T'])
    
    #Compressor
    point_1 = {'T':point_8['T'] + cycle_inputs['approach_HX'],'P':point_6a['P'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_1)
    #print('titulo 1',point_1['Q'])
        
    point_2s = {'P':point_3['P'],'SMASS':point_1['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2s)
    
    point_2 = {'P':point_3['P'],'HMASS':point_1['HMASS'] + ((point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent']),'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2)
    
    
    #Descobrindo potência da geladeira
    
    Q_ETI = m1*(point_8['HMASS'] - point_7['HMASS'])
    #print(Q_ETI)
    
    #Descobrindo potência do compressor
    
    work = m1*(point_2['HMASS'] - point_1['HMASS'])
    #print(work)
    
    #Descobrindo COP
    
    COP = (Q_ETI + cycle_inputs['Q_ETB'])/work
    
    print("COP",COP)
    return COP


    
    
    
    
    

    


COP_Evap_Serie(input_values)
    
    