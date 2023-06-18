# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 09:46:52 2023

@author: Ramon
"""

import matplotlib.pyplot as plt
import numpy as np
import CoolProp as cp
from CoolProp.CoolProp import PropsSI



cop_R717 = [2.6134665930154424, 2.6134665930154424, 2.613466593015442, 
             2.6134665930154424, 2.6134665930154424]


cop_R404A = [2.391268180201801, 2.39129406079516, 2.3913147660127803, 
             2.391331707136443, 2.3913458250770403]

cop_R410A = [2.483154876470052, 2.4831540624329156, 2.483153411226144, 
             2.483152878435772, 2.4831524344542575]

cop_R600 = [2.7222928431694244, 2.7222928431694258, 2.7222928431694244, 
            2.722292843169425, 2.7222928431694244]

cop_R600A = [2.672713676310412, 2.672713676310413, 2.6727136763104116, 
             2.672713676310413, 2.6727136763104133]

cop_R1234yf = [2.5130422750519164, 2.5130422750519155, 2.513042275051916, 
               2.513042275051915, 2.513042275051916]

cop_R1234zeE = [2.603510689379276, 2.603510689379276, 2.603510689379276, 2.603510689379276, 2.6035106893792768]

r = [1.0,1.25,1.5,1.75,2.0]

plt.figure(figsize=(12, 10))
plt.plot(r,cop_R717, color = 'r',label='R717')
plt.plot(r,cop_R404A, color = 'b',label = 'R404A')
plt.plot(r,cop_R410A, color = 'g',label = 'R410A')
plt.plot(r,cop_R600,color = 'c',label = 'R600')
plt.plot(r,cop_R600A,color = 'y',label = 'R600A')
plt.plot(r,cop_R1234yf, color = 'm', label = 'R1234yf')
plt.plot(r,cop_R1234zeE,color = 'k',label = 'R1234ze(E)')
plt.xlabel('Razão entre Vazões Mássicas')
plt.ylabel('COP')
plt.legend()
plt.grid(True)