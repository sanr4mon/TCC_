# -*- coding: utf-8 -*-
"""
Created on Sun May 28 20:08:26 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI

Q_ETI = []
cop = []
work = []

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
    't_internal_g':273,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R600A',
    'subcooling':[1,2,3,4,5,6,7,8,9,10],
    'superheating':5,
    'approach_HX':5,
    'r':1.75,
    'tit_evap_f':0.6
}

def COP_Evap_Paralelo(cycle_inputs):
    for subcooling in cycle_inputs['subcooling']:
    
        P_ETB = PropsSI("P","T",cycle_inputs['t_internal_f'],"Q",1,cycle_inputs['refrigerant'])
        P_ETI = PropsSI("P","T",cycle_inputs['t_internal_g'],"Q",1,cycle_inputs['refrigerant'])
    
        #Pós Condensador
        point_3 = {'Q':0,'T':cycle_inputs['t_cond']-subcooling,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_3)
    
    
    
        #Pós HX
        point_4a = {'T':point_3['T']-cycle_inputs['approach_HX'],'P':point_3['P'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_4a)
    
        point_4b = {'T':point_3['T']-cycle_inputs['approach_HX'],'P':point_3['P'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_4b)
    
        #Evaporador da Geladeira e Disp. de Expansão 1
        point_6a = {'P':P_ETI,'T':cycle_inputs['t_internal_g'] + cycle_inputs['superheating'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_6a)
        #print("Temp. 6a = ",point_6a['T'])
        #print('Titulo 6a:',point_6a['Q'])
    
    
    
    
        point_5a = {'HMASS':point_4a['HMASS'],'P':P_ETI,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_5a)
        #print("Temp.5a = ",point_5a['T'])
    
        #VRP
        point_7a = {'HMASS':point_6a['HMASS'],'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_7a)
        #print("Temp.7a = ",point_7a['T'])
    
    
    
        #print(point_7a['Q'],point_7a['T'])
    
        #Dispositivo de Expansão 2 e Evaporador do Freezer
    
        point_5b = {'HMASS':point_4b['HMASS'],'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_5b)
        #print("temp. 5b = ",point_5b['T'])
        #print("titulo 5b",point_5b['Q'])
    
    
    
    
        point_6b = {'Q':cycle_inputs['tit_evap_f'],'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_6b)
        #print("temp.6b =",point_6b['T'])
        #print("titulo 6b = ",point_6b['Q'])
    
        #print(point_6b['P'],P_ETB)
    
    
        #Descobrindo vazões mássicas
    
        m3 = cycle_inputs['Q_ETB']/(point_6b['HMASS']-point_5b['HMASS'])
    
        m2 = m3 * cycle_inputs['r']
    
        m1 = m2+m3
    
        #print("m1, m2, m3 = ", m1,m2,m3)
    
        #Entrada do trocador
    
        h8 = (m2*point_7a['HMASS'] + m3*point_6b['HMASS'])/m1
    
        point_8 = {'HMASS':h8,'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_8)
        #print("temp. 8 = ",point_8['T'])
    
        #Compressor
        point_1 = {'P':P_ETB,'T':point_8['T']+cycle_inputs['approach_HX'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_1)
        #print('titulo 1 =',point_1['Q'])
    
        point_2s = {'P':point_3['P'],'SMASS':point_1['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2s)
    
    
        point_2 = {'P':point_3['P'],'HMASS':point_1['HMASS'] + ((point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent']),'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2)
    
        #Descobrindo potência da geladeira
    
        q_ETI = m2*(point_6a['HMASS'] - point_5a['HMASS'])
        Q_ETI.append(q_ETI)
    
    
    #Descobrindo potência do compressor
    
        WORK = m1*(point_2['HMASS'] - point_1['HMASS'])
        work.append(WORK)
    
    #Descobrindo COP
    
    for i in range(len(work)):
        cop.append((Q_ETI[i] + cycle_inputs['Q_ETB'])/work[i])
        i+=1
    
    print(cop)
    
    plt.figure(figsize=(6, 4))
    plt.scatter(cycle_inputs['subcooling'],cop)
    plt.xlabel('Subresfriamento no Condensador')
    plt.ylabel('COP')
    plt.grid(True)
    
    return cop


COP_Evap_Paralelo(input_values)