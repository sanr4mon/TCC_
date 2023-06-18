# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 11:46:09 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI

variacao = [0.1,0.15,0.2,0.25,0.3]

cop_R717 = [2.613466593015443, 2.6134665930154424, 2.613466593015442, 
            2.6134665930154317, 2.613466593015443]

cop_R404A = [2.3911750186137097, 2.3912448885502338, 2.3913147660127803, 
             2.391384650995586, 2.3914545434930177]

cop_R410A = [2.483157807268101, 2.4831556091308022, 2.483153411226144, 
             2.4831512135540663, 2.4831490161146426]

cop_R600 = [2.7222928431694253, 2.722292843169424, 2.7222928431694244, 
            2.7222928431694244, 2.7222928431694253]

cop_R600A = [2.6727136763104116, 2.6727136763104125, 2.6727136763104116, 
             2.672713676310413, 2.672713676310412]

cop_R1234yf = [2.5130422750519164, 2.513042275051914, 2.513042275051916, 
               2.513042275051915, 2.513042275051914]

cop_R1234zeE = [2.5130422750519164, 2.513042275051914, 2.513042275051916, 
                2.513042275051915, 2.513042275051914]

plt.figure(figsize=(12, 10))
plt.plot(variacao,cop_R717, color = 'r',label='R717')
plt.plot(variacao,cop_R404A, color = 'b',label = 'R404A')
plt.plot(variacao,cop_R410A, color = 'g',label = 'R410A')
plt.plot(variacao,cop_R600,color = 'c',label = 'R600')
plt.plot(variacao,cop_R600A,color = 'y',label = 'R600A')
plt.plot(variacao,cop_R1234yf, color = 'm', label = 'R1234yf')
plt.plot(variacao,cop_R1234zeE,color = 'k',label = 'R1234ze(E)')
plt.xlabel('Variação do Título na Saída do Freezer')
plt.ylabel('COP')
plt.legend()
plt.grid(True)