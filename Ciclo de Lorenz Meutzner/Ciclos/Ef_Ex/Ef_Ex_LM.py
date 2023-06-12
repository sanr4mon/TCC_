# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:52:12 2023

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
    'tit_evap_f':0.5,
    'subcooling':5,
    'superheating':5,
    'approach_HX':5
}

def Ef_Ex_LM(cycle_inputs):
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

    print("temp.ponto 6 =",point_6['T'])
 
    
    point_7 = {'P':P_Evap,'Q':cycle_inputs['tit_evap_f'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_7)
    
    print('temp.7 = ',point_7['T'])
    print('pressao 7 = ',point_7['P'])
    
    
    
    #Pós TCBT - aquecendo
    point_8 = {'P':P_Evap,'T':point_7['T'] + cycle_inputs['approach_HX'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_8)
    print('temp.8 =',point_8['T'])
    
    #Evaporador da Geladeira
    
    point_9 = {'P':P_Evap,'T':point_8['T']+cycle_inputs['superheating'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_9)
    
    print('temp. 9',point_9['T'])
    
    #Compressor
    
    point_1 = {'T':point_9['T'] + cycle_inputs['approach_HX'],'P':P_Evap,'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_1)
    print('titulo 1:',point_1['Q'])
    print('temp. 1 =',point_1['T'])
    
    point_2s = {'P':point_3['P'],'SMASS':point_1['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2s)
    
    point_2 = {'P':point_3['P'],'HMASS':point_1['HMASS'] + ((point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent']),'refrigerant':cycle_inputs['refrigerant']}
    propriedades(point_2)
    
    #Descobrindo vazão mássica
    
    m = cycle_inputs['Q_ETB']/(point_7['HMASS'] - point_6['HMASS'])
    print(m)
    #Descobrindo potência da geladeira
    
    Q_ETI = m*(point_9['HMASS'] - point_8['HMASS'])
    
    #Descobrindo trabalho do compressor
    
    work =  m*(point_2['HMASS'] - point_1['HMASS'])
    
    print("work",work)
    
    #Calculando taxa de destruição de exergia de cada componente]
    #1. Compressor
    delta_A_comp = (point_2['HMASS'] - point_1['HMASS']) - cycle_inputs['t_external']*(point_2['SMASS'] - point_1['SMASS'])
    Ad_comp = work - m*delta_A_comp
    print("Ad_comp",Ad_comp)
    
    #2. Condensador
    Q_cond = m*(point_2['HMASS'] - point_3['HMASS'])
    delta_A_cond = (point_2['HMASS'] - point_3['HMASS']) - cycle_inputs['t_external']*(point_2['SMASS'] - point_3['SMASS'])
    Ad_cond = m*delta_A_cond
    print("Ad_cond",Ad_cond)
    
    #3. TCAT
    delta_A_superior_TCAT = (point_3['HMASS'] - point_4['HMASS'] - cycle_inputs['t_external']*(point_3['SMASS'] - point_4['SMASS']))
    delta_A_inferior_TCAT = (point_1['HMASS'] - point_9['HMASS'] - cycle_inputs['t_external']*(point_1['SMASS'] - point_9['SMASS']))
    Ad_TCAT = m*(delta_A_superior_TCAT - delta_A_inferior_TCAT)
    print("Ad_TCAT",Ad_TCAT)
    
    #4. TCBT
    delta_A_superior_TCBT = (point_4['HMASS'] - point_5['HMASS'] - cycle_inputs['t_external']*(point_4['SMASS'] - point_5['SMASS']))
    delta_A_inferior_TCBT = (point_8['HMASS'] - point_7['HMASS'] - cycle_inputs['t_external']*(point_8['SMASS'] - point_7['SMASS']))
    Ad_TCBT = m*(delta_A_superior_TCBT - delta_A_inferior_TCBT)
    print("Ad_TCBT",Ad_TCBT)

    
    #5. Dispositivo de Expansão 1
    delta_A_DE = -cycle_inputs['t_external'] * (point_5['SMASS'] - point_6['SMASS'])
    Ad_DE = m * delta_A_DE
    print("Ad_DE",Ad_DE)
    
    #6. Evaporador do Freezer
    delta_A_ETB = point_6['HMASS'] - point_7['HMASS'] - cycle_inputs['t_external']*(point_6['SMASS'] - point_7['SMASS'])
    Ad_ETB = m*delta_A_ETB + (1 - (cycle_inputs['t_external']/(cycle_inputs['t_internal_f']+5))) * cycle_inputs['Q_ETB']
    print("Ad_ETB",Ad_ETB)
    
    #7. Evaporador da Geladeira
    delta_A_ETI = point_8['HMASS'] - point_9['HMASS'] - cycle_inputs['t_external']*(point_8['SMASS'] - point_9['SMASS'])
    Ad_ETI = m*delta_A_ETI + (1 - (cycle_inputs['t_external']/(point_9['T']+5))) * Q_ETI
    print("Ad_ETI",Ad_ETI)
    
    Ad_total = Ad_comp + Ad_cond + Ad_DE + Ad_ETI + Ad_ETB +Ad_TCAT + Ad_TCBT
    
    ef_ex = 1 - (Ad_total/work)
    
    print(ef_ex)
    
    return ef_ex
    
#COP_LM(input_values)
Ef_Ex_LM(input_values)