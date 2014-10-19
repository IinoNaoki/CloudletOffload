'''
Created on Sep 19, 2014

@author: yzhang28
'''

import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox
import sys
from matplotlib.lines import fillStyles
from matplotlib.markers import MarkerStyle
sys.path.append("..")
from Core.MDPfunc import *

from matplotlib.backends.backend_pdf import PdfPages



V_opt_set_bell_R_changing = pickle.load(open("../results/R_changing/V_opt_bell","r"))
A_opt_set_bell_R_changing = pickle.load(open("../results/R_changing/A_opt_bell","r"))
params_set_bell_R_changing = pickle.load(open("../results/R_changing/Paramsset","r"))
expnum_bell_R_changing = pickle.load(open("../results/R_changing/expnum","r"))
sys.stdout = open('../results/R_changing/__Amat_Q_N', 'w')
for i in range(expnum_bell_R_changing):
    G = params_set_bell_R_changing[i]['G']
    for _g in range(G):
        print
        print "state G =", _g
        ShowMatrix(A_opt_set_bell_R_changing[i], 'a', 'g', _g, params_set_bell_R_changing[i])
        print


V_opt_set_bell_LAM_C_changing = pickle.load(open("../results/LAM_C_changing/V_opt_bell","r"))
A_opt_set_bell_LAM_C_changing = pickle.load(open("../results/LAM_C_changing/A_opt_bell","r"))
params_set_bell_LAM_C_changing = pickle.load(open("../results/LAM_C_changing/Paramsset","r"))
expnum_bell_LAM_C_changing = pickle.load(open("../results/LAM_C_changing/expnum","r"))
sys.stdout = open('../results/LAM_C_changing/__Amat_Q_N', 'w')
for i in range(expnum_bell_LAM_C_changing):
    G = params_set_bell_LAM_C_changing[i]['G']
    for _g in range(G):
        print
        print "state G =", _g
        ShowMatrix(A_opt_set_bell_LAM_C_changing[i], 'a', 'g', _g, params_set_bell_LAM_C_changing[i])
        print


V_opt_set_bell_ETA_changing = pickle.load(open("../results/ETA_changing/V_opt_bell","r"))
A_opt_set_bell_ETA_changing = pickle.load(open("../results/ETA_changing/A_opt_bell","r"))
params_set_bell_ETA_changing = pickle.load(open("../results/ETA_changing/Paramsset","r"))
expnum_bell_ETA_changing = pickle.load(open("../results/ETA_changing/expnum","r"))
sys.stdout = open('../results/ETA_changing/__Amat_Q_N', 'w')
for i in range(expnum_bell_ETA_changing):
    G = params_set_bell_ETA_changing[i]['G']
    for _g in range(G):
        print
        print "state G =", _g
        ShowMatrix(A_opt_set_bell_ETA_changing[i], 'a', 'g', _g, params_set_bell_ETA_changing[i])
        print
        
        
