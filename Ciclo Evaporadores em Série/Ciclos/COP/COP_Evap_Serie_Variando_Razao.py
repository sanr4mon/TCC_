# -*- coding: utf-8 -*-
"""
Created on Sun May 28 18:54:21 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI

Q_ETI = []
cop = []
work = []
Ad_comp = []
Ad_cond = []
Ad_DE1 = []
Ad_DE2 = []
Ad_ETI = []
Ad_ETB = []
Ad_HX = []
Ad_total = []
Ef_Ex = []


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
    'variacao_titulo_f':0.2,
    'subcooling':5,
    'superheating':5,
    'approach_HX':5,
    'r':[1.0,1.25,1.5,1.75,2.0]
}



def COP_Evap_Serie(cycle_inputs):
    
    for razao in cycle_inputs['r']:
    
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
        m3 = m2 / razao
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
    
        q_ETI = m1*(point_8['HMASS'] - point_7['HMASS'])
        Q_ETI.append(q_ETI)
    #print(Q_ETI)
    
    #Descobrindo potência do compressor
    
        WORK = m1*(point_2['HMASS'] - point_1['HMASS'])
        work.append(WORK)
    #print(work)
    
    #Descobrindo COP
    for i in range(len(work)):
        cop.append((Q_ETI[i] + cycle_inputs['Q_ETB'])/work[i])
        i+=1
    

            #Calculando taxa de destruição de exergia de cada componente]
    #1. Compressor
        Sger_comp = m1*(point_2['SMASS']-point_1['SMASS'])
        ad_comp = cycle_inputs['t_cond']*Sger_comp
        Ad_comp.append(ad_comp)
        
    
    
    #2. Condensador
        Q_cond = m1*(point_2['HMASS'] - point_3['HMASS'])
        Sger_cond = m1*(point_3['SMASS'] - point_2['SMASS']) + Q_cond/cycle_inputs['t_cond']
        ad_cond = cycle_inputs['t_cond'] * Sger_cond
        Ad_cond.append(ad_cond)
    
    
    
    #3. Trocador de Calor
        Sger_HX = m1*(-point_4a['SMASS'] - point_1['SMASS'] + point_8['SMASS'] + point_3['SMASS'])
        ad_HX = cycle_inputs['t_cond'] * Sger_HX
        Ad_HX.append(ad_HX)
    
    
    #4. Dispositivo de Expansão 1
        Sger_DE1 = m2*(point_5a['SMASS'] - point_4a['SMASS'])
        ad_DE1 = cycle_inputs['t_cond']*Sger_DE1
        Ad_DE1.append(ad_DE1)
        
    #5. Dispositivo de Expansão 2
        Sger_DE2 = m3*(point_5b['SMASS'] - point_4b['SMASS'])
        ad_DE2 = cycle_inputs['t_cond'] * Sger_DE2 
        Ad_DE2.append(ad_DE2)
    
    
    #6. Evaporador do Freezer
        Sger_ETI = np.zeros(len(Q_ETI))
        for i in range(len(Q_ETI)):
            Sger_ETI[i] = m1*(point_6a['SMASS']-point_5a['SMASS']) - (Q_ETI[i]/point_8['T'])
        #Ad_ETI = cycle_inputs['t_cond'] * Sger_ETI

        print("Sger_ETI",Sger_ETI)
    
    
    
    
    #7. Evaporador da Geladeira
        Sger_ETB = m2*(point_8['SMASS']-point_7['SMASS']) - (cycle_inputs['Q_ETB']/point_7['T'])
        ad_ETB = cycle_inputs['t_cond'] * Sger_ETB
        Ad_ETB.append(ad_ETB)
  
    
    for i in range(len(Ad_comp)):
        Ad_total.append(Ad_comp[i] +  Ad_cond[i] + Ad_HX[i] + Ad_DE1[i] + Ad_DE2[i] + Ad_ETI[i] + Ad_ETB[i])
        Ef_Ex.append(1 - (Ad_total[i]/work[i]))
        i+=1
    
    
    
    #print("Ad_comp",Ad_comp)
    #print("Ad_cond",Ad_cond)
    #print("Ad_HX",Ad_HX)
    #print('Ad_DE1',Ad_DE1)
    #print('Ad_DE2',Ad_DE2)
    #print("Ad_ETI",Ad_ETI)
    #print("Ad_ETB",Ad_ETB)
    
    #print(cop)
    #print(Ef_Ex)
    
    
    return cop
    return Ef_Ex

COP_Evap_Serie(input_values)