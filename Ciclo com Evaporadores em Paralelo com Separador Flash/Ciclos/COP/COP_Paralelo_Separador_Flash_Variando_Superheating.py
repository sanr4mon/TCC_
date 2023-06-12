# -*- coding: utf-8 -*-
"""
Created on Wed May 31 09:16:32 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI

Q_ETI = []
W_CAP = []
W_CBP = []
work = []
COP =[]



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
    't_internal_g':270,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R600A',
    'r':1.5,
    'subcooling':5,
    'superheating':[1,2,3,4,5,6,7,8,9,10]
}

#P_ETB = PropsSI("P","Q",1,"T",temp.freezer","refrigerant")

def COP_Paralelo_Separador(cycle_inputs):
    
    for superheating in cycle_inputs['superheating']:
    
    
        P_ETB = PropsSI("P","Q",1,"T",cycle_inputs['t_internal_f'],cycle_inputs['refrigerant'])

    
    #Condensador
    
        point_5 = {'Q':0,'T':cycle_inputs['t_cond'] - cycle_inputs['subcooling'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_5)
    #print("Pressao Intermediária",P_ETI)
    
    #Compressor de Alta Pressão
    
    
    #Divissão da vazão mássica em A  
    
        point_7a = {'T':cycle_inputs['t_internal_g'],'Q':0,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_7a)
    #print('pressão da geladeira=',point_7a['P'])
    
        P_ETI = point_7a['P']
    
        point_7 = {'P':P_ETI,'Q':0,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_7)
    
    
        point_8a = {'P':P_ETI,'Q':1,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_8a)
    
    
        point_3 = {'P':P_ETI,'Q':1,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_3)
    
        point_4s = {'P':point_5['P'],'SMASS':point_3['SMASS'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_4s)
    
        point_4 = {'P':point_5['P'],'HMASS':point_3['HMASS'] + (point_4s['HMASS'] - point_3['HMASS'])/cycle_inputs['N_isent'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_4)
    
    #Dispositivo de Expansão
        point_6 = {'P':P_ETI,'HMASS':point_5['HMASS'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_6)
    
    #Pós Separador Flash
    

    
    

    
    #print("temp. 8a =",point_8a['T'])
    
    #print(point_8a['T'])
    
    #print(point_7a['T'],point_8a['T'])
    
        point_9a = {'P':P_ETB,'HMASS':point_8a['HMASS'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_9a)
    #print('temp.9a = ',point_9a['T'])
    #print('titulo 9a',point_9a['Q'])
    
        point_7b = {'P':P_ETI,'Q':0,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_7b)
    
        point_8b = {'HMASS':point_7b['HMASS'],'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_8b)
    #print('temperatura 8b =',point_8b['T'])
    
        t9 = 0
    
        if superheating == 0:
            t9 = int(point_8b['T'])
    
        else:
            t9 = point_8b['T'] + superheating
    
        point_9b = {'P':P_ETB,'T':t9,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_9b)
    
    #print('temp. superaquecida = ',point_9b['T'])
    #print('titulo 9b',point_9b['Q'])
    
    
    #Encontrando vazão mássica 4
    
        m4 = cycle_inputs['Q_ETB']/(point_9b['HMASS'] - point_8b['HMASS'])
    #print(m4)
    
    #Encontrando vazão mássica 3
    
        m3 = cycle_inputs['r']*m4
    #print(m3)
    
    #Encontrando vazão mássica 2
        m2 = m3 + m4
    #print(m2)
    #Compressor de Baixa Pressão
    
        h1 = (m3*point_9a['HMASS'] + m4*point_9b['HMASS'])/m2
        
        point_1 = {'HMASS':h1,'P':P_ETB,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_1)
    
    #print('titulo 1:',point_1['Q']) #dá mistura bifásica
    
        point_2s = {'SMASS':point_1['SMASS'],'P':P_ETI,'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2s)
    
        point_2 = {'P':P_ETI,'HMASS':point_1['HMASS'] + (point_2s['HMASS'] - point_1['HMASS'])/cycle_inputs['N_isent'],'refrigerant':cycle_inputs['refrigerant']}
        propriedades(point_2)
    
    #Encontrando vazão mássica 1 pelo balanço do separador
        m1 = m2*(point_2['HMASS'] - point_7['HMASS'])/(point_3['HMASS'] - point_6['HMASS'])
    #
    #print(m1,m2,m3,m4)
    
    #Encontrando trabalho dos compressores
    #
    #print(m1,m2,m3,m4)
    
    #Encontrando trabalho dos compressores
    
        w_cap = m1*(point_4['HMASS'] - point_3['HMASS'])
        W_CAP.append(w_cap)
    
        w_cbp = m2*(point_2['HMASS'] - point_1['HMASS'])
        W_CBP.append(w_cbp)
       
        #Encontrando potência do ETI
        q_ETI = m4*(point_8a['HMASS'] - point_7a['HMASS'])
        Q_ETI.append(q_ETI)
    
        #print(Q_ETI)
   
    for i in range(len(W_CAP)):
        work.append(W_CAP[i] + W_CBP[i])
        cop = (cycle_inputs['Q_ETB'] + Q_ETI[i])/(work[i])
        COP.append(cop)
        i+=1
    
    print(COP)
    
    plt.figure(figsize=(6, 4))
    plt.scatter(cycle_inputs['superheating'],COP)
    plt.xlabel('Superaquecimento no Freezer')
    plt.ylabel('COP')
    plt.grid(True)
    

COP_Paralelo_Separador(input_values)  
    
