'''
Created on 17 Oct, 2014

@author: yzhang28
'''

# lam_u = params['LAM_U']
# lam_au = params['LAM_U'] * 0.1
# betah = params['BETAH'] # betah=0.5
# c=params['C_TOP']  #2
# TAU = 0.5
# VELOCITY = 5.0
# aph_l_CONST params['ALPHA_LOCAL']
# aph_r_CONST params['ALPHA_REMOTE']
# PENALTY


import numpy as np
A_linear = [1,1,2,4,2,1,1,6,7,0]
_act = A_linear.count(1)

print _act