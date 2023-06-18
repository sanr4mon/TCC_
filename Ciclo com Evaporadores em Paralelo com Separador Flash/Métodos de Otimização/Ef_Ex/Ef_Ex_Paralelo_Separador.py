# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:48:16 2023

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
    't_internal_g':268,
    'Q_ETB':35200, #10 TR
    'N_isent': 0.7,
    'refrigerant':'R410A',
    'r':2.0,
    'subcooling':10,
    'superheating':1
}





def Ef_Ex_Paralelo_Sep(cycle_inputs):
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
    
    
    point_9b = {'P':P_ETB,'T':point_8b['T']+cycle_inputs['superheating'],'refrigerant':cycle_inputs['refrigerant']}
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
    
    W_CAP = m1*(point_4['HMASS'] - point_3['HMASS'])
    W_CBP = m2*(point_2['HMASS'] - point_1['HMASS'])
    
    work = W_CAP + W_CBP
    #print("work",work)
    
    #print(W_CAP,W_CBP,work)
    
    #Encontrando potência do ETI
    
    Q_ETI = m3*(point_8a['HMASS'] - point_7a['HMASS'])
    #print(Q_ETI)
    
    #Encontrando taxa de destruição de exergia para cada componente do ciclo
    
    #1. Compressor de Alta Pressão
    delta_A_CAP = (point_4['HMASS'] - point_3['HMASS']) - cycle_inputs['t_external']*(point_4['SMASS'] - point_3['SMASS'])
    Ad_CAP = W_CAP - m1*delta_A_CAP
    #print("Ad_CAP",Ad_CAP)
    
    
    #2. Condensador 
    Q_cond = m1*(point_4['HMASS'] - point_5['HMASS'])
    delta_A_cond = (point_4['HMASS'] - point_5['HMASS']) - cycle_inputs['t_external']*(point_4['SMASS'] - point_5['SMASS'])
    Ad_cond = m1*delta_A_cond 
    #print("Ad_cond",Ad_cond)
    
    #3.Disp. Expansão 2
    delta_A_DE2 = -cycle_inputs['t_external'] * (point_7b['SMASS'] - point_8b['SMASS'])
    Ad_DE2 = m3 * delta_A_DE2
    #print("Ad_DE2",Ad_DE2)
    
    #4.Separador Flash
    Sger_sep = m1*(point_3['SMASS'] - point_6['SMASS']) + m2*(point_7['SMASS'] - point_2['SMASS'])
    Ad_sep = cycle_inputs['t_external'] * Sger_sep
    #print('Ad_sep',Ad_sep)
    
    #5.Evaporador de Temperatura Intermediária
    delta_A_ETI = point_7a['HMASS'] - point_8a['HMASS'] - cycle_inputs['t_external']*(point_7a['SMASS'] - point_8a['SMASS'])
    Ad_ETI = m3*delta_A_ETI + (1 - (cycle_inputs['t_external']/(point_8a['T']+5))) * Q_ETI
    #print("Ad_ETI",Ad_ETI)
    
    #6.Válvula Reguladora de Pressão
    delta_A_VRP = -cycle_inputs['t_external'] * (point_8a['SMASS'] - point_9a['SMASS'])
    Ad_VRP = m2 * delta_A_VRP
    #print("Ad_VRP",Ad_VRP)
    
    #7. Dispositivo de Expansão 1
    delta_A_DE1 = -cycle_inputs['t_external'] * (point_5['SMASS'] - point_6['SMASS'])
    Ad_DE1 = m1 * delta_A_DE1
    #print("Ad_DE1",Ad_DE1)
    
    
    #8. Evaporador de Baixa Temperatura
    delta_A_ETB = point_8b['HMASS'] - point_9b['HMASS'] - cycle_inputs['t_external']*(point_8b['SMASS'] - point_9b['SMASS'])
    Ad_ETB = m4 *delta_A_ETB + (1 - (cycle_inputs['t_external']/(point_9b['T']+5))) * cycle_inputs['Q_ETB']
    #print("Ad_ETB",Ad_ETB)
    
    #9 Compressor de Baixa Pressão
    delta_A_CBP = (point_2['HMASS'] - point_1['HMASS']) - cycle_inputs['t_external']*(point_2['SMASS'] - point_1['SMASS'])
    Ad_CBP = W_CBP - m2*delta_A_CBP
    #print("Ad_CBP",Ad_CBP)
    
    #10. Nó no ponto 1
    delta_A_9b_1 = point_9b['HMASS'] - point_1['HMASS'] - cycle_inputs['t_external']*(point_9b['SMASS'] - point_1['SMASS'])
    delta_A_9a_1 = point_9a['HMASS'] - point_1['HMASS'] - cycle_inputs['t_external']*(point_9a['SMASS'] - point_1['SMASS'])
    Ad_no =  m4* delta_A_9b_1 + m3*delta_A_9a_1 
    #print("Ad_no",Ad_no)
    
    Ad_total = Ad_CAP + Ad_cond + Ad_DE1 + Ad_ETI + Ad_VRP + Ad_DE2 + Ad_ETB + Ad_CBP + Ad_sep + Ad_no
    
    #Cálculo da Eficiência Exergética
    ef_ex = 1 - (Ad_total/work)
    
    print(ef_ex)
    
    return ef_ex
    





Ef_Ex_Paralelo_Sep(input_values)