# -*- coding: utf-8 -*-
"""
Created on Sun May 28 18:18:10 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI

Q_ETI =[]
W_CAP = []
W_CBP = []
work = []
cop = []

#Cálculo das Propriedades Termodinâmicas

def propriedades(ponto):
    variaveis=['T','P','HMASS','SMASS','Q','C']
    input_var=list(ponto.keys())
    output_var=[variable for variable in variaveis if variable not in input_var]
    outputs=PropsSI(output_var,input_var[0],ponto[input_var[0]],input_var[1],ponto[input_var[1]],ponto['refrigerant'])

    for index,variable in enumerate(output_var):
        ponto[variable]=outputs[index]
        
input_values ={
    't_external': 293,
    't_cond':303,
    't_internal_g':[268,269,270,271,272,273,274,275,276,277,278],
    't_internal_f':250,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R600A',
    #'P_ETB':100000,#100 kPa
    'tit_evap_g':0.6,
    'subcooling':5,
    'superheating':5
}

def COP_Duplo_Estagio(cycle_inputs):
    
    for temp in cycle_inputs['t_internal_g']:
    
        P_ETB = PropsSI("P","Q",1,"T",cycle_inputs['t_internal_f'],cycle_inputs['refrigerant'])
    
        #Pós - Condensador (propriedades do ponto 3)
        point_3 = {'Q':0,'T':cycle_inputs['t_cond'] - cycle_inputs['subcooling'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_3)
    
    
    
        #Evaporador da Geladeira
        point_5 = {'Q':cycle_inputs['tit_evap_g'],'T':temp,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_5)
    
    
        P_int = point_5['P']
    
        point_4 = {'HMASS':point_3['HMASS'],'P':P_int,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_4)
    
        #print("temp.4",point_4['T'])
    
    
        #Compressor de Alta Pressão
        point_1 = {'Q':1,'P':P_int, 'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_1)
        #print(point_5['HMASS'],point_1['HMASS'])
    
        point_2s = {'SMASS':point_1['SMASS'],'P':point_3['P'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2s)
    
        point_2 = {'P':point_3['P'],'HMASS':point_1['HMASS'] + ((point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent']),'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2)
    
   
    
   
        #Pós Separador Flash (propriedades ponto 6)
        point_6 = {'Q':0,'P':P_int,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_6)
    
    
        #Evaporador do Freezer
        point_7 = {'HMASS':point_6['HMASS'],'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_7)
    
        #print("temp.7 = ",point_7['T'])
    
    
        point_8 = {'P':P_ETB,'T':int(point_7['T'])+cycle_inputs['superheating'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_8)
        #print('titulo 8 = ',point_8['Q'])
        #print('temperatura 8 = ',t8)
    
        #Compressor de Baixa Pressão
    
        point_9s = {'P':P_int,'SMASS':point_8['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_9s)
    
        point_9 = {'P':P_int,'HMASS':point_8['HMASS'] + (point_9s['HMASS'] - point_8['HMASS']),'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_9)
    
        #Calculando vazões mássicas
    
        m1 = cycle_inputs['Q_ETB']/(point_8['HMASS'] - point_7['HMASS'])
        #print(m1)
    
        m2 = m1*(point_6['HMASS'] - point_9['HMASS'])/(point_5['HMASS'] - point_1['HMASS'])
        #print(m2)
    
        #print(m1,m2)
    
        #Calculando Potência Frigorífica da Geladeira
    
        q_ETI = m2*(point_5['HMASS'] - point_4['HMASS'])
        Q_ETI.append(q_ETI)
    #print(Q_ETI)
    
    #Calculando potência dos compressores
        w_cbp = m1*(point_9['HMASS'] - point_8['HMASS'])
        W_CBP.append(w_cbp)
        w_cap = m2*(point_2['HMASS'] - point_1['HMASS'])
        W_CAP.append(w_cap)
    
    
    for i in range(len(W_CAP)):
        work.append(W_CAP[i] + W_CBP[i])
        COP = (cycle_inputs['Q_ETB'] + Q_ETI[i])/(work[i])
        cop.append(COP)
        i+=1
    
    print(cop)
    
    plt.figure(figsize=(6, 4))
    plt.scatter(cycle_inputs['t_internal_g'],cop)
    plt.xlabel('Temperatura de Saída da Geladeira')
    plt.ylabel('COP')
    plt.grid(True)
    
COP_Duplo_Estagio(input_values)