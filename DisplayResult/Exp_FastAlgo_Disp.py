'''
Created on Sep 4, 2014

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
from reportlab.lib.styles import LineStyle
sys.path.append("..")
from Core.MDPfunc import *

from matplotlib.backends.backend_pdf import PdfPages


expnum_R = pickle.load(open("../results/FAST_algo/expnum_R","r"))
x_axis_list_R = pickle.load(open("../results/FAST_algo/xaxis_R","r"))
 
RESset_fast_R = pickle.load(open("../results/FAST_algo/fast_R","r"))
RESset_bell_R = pickle.load(open("../results/R_changing/bell","r"))
RESset_myo_R = pickle.load(open("../results/R_changing/myo","r"))
RESset_rnd_R = pickle.load(open("../results/R_changing/rnd","r"))
RESset_zero_R = pickle.load(open("../results/R_changing/zero","r"))
RESset_one_R = pickle.load(open("../results/R_changing/one","r"))

y_v_avg_bell_R = [RESset_bell_R[i][0] for i in range(expnum_R)]
y_v_avg_fast_R = [100.0*RESset_fast_R[i][0]/(1.0*y_v_avg_bell_R[i]) for i in range(expnum_R)]
y_v_avg_myo_R = [100.0*RESset_myo_R[i][0]/(1.0*y_v_avg_bell_R[i]) for i in range(expnum_R)]
y_v_avg_rnd_R = [100.0*RESset_rnd_R[i][0]/(1.0*y_v_avg_bell_R[i]) for i in range(expnum_R)]
y_v_avg_zero_R = [100.0*RESset_zero_R[i][0]/(1.0*y_v_avg_bell_R[i]) for i in range(expnum_R)]
y_v_avg_one_R = [100.0*RESset_one_R[i][0]/(1.0*y_v_avg_bell_R[i]) for i in range(expnum_R)]
y_v_avg_bell_R = [100 for i in range(expnum_R)]

# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list_R,y_v_avg_fast_R,color='black',markerfacecolor='grey', markeredgecolor='black', marker='h',markersize=8,label='FAST')
plot(x_axis_list_R,y_v_avg_bell_R,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP', linestyle='-')
plot(x_axis_list_R,y_v_avg_myo_R,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO', linestyle='--')
plot(x_axis_list_R,y_v_avg_rnd_R,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list_R,y_v_avg_zero_R,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LOC', linestyle='--')
plot(x_axis_list_R,y_v_avg_one_R,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='OFF', linestyle='--')
xlabel('Cloudlet coverage radius $R$',fontsize=14)
ylabel('User\'s raletive expected cost ($\%$)',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best',fancybox=True)
locs, labels = plt.yticks()
xlim([8,15])
yticks([100, 101, 102, 103, 104])
ylim([99.9, 104.5])
plt.setp(labels, rotation=90)
pp = PdfPages('../results/FAST_algo/figure1.pdf')
plt.savefig(pp, format='pdf')
pp.close()

# fig 1 different R
####################
# fig 2 different penalty

expnum_PEN = pickle.load(open("../results/FAST_algo/expnum_PEN","r"))
x_axis_list_PEN = pickle.load(open("../results/FAST_algo/xaxis_PEN","r"))

RESset_fast_PEN = pickle.load(open("../results/FAST_algo/fast_PEN","r"))
RESset_bell_PEN = pickle.load(open("../results/PEN_changing/bell","r"))
RESset_myo_PEN = pickle.load(open("../results/PEN_changing/myo","r"))
RESset_rnd_PEN = pickle.load(open("../results/PEN_changing/rnd","r"))
RESset_zero_PEN = pickle.load(open("../results/PEN_changing/zero","r"))
RESset_one_PEN = pickle.load(open("../results/PEN_changing/one","r"))

y_v_avg_bell_PEN = [RESset_bell_PEN[i][0] for i in range(expnum_PEN)]
y_v_avg_fast_PEN = [100.0*RESset_fast_PEN[i][0]/(1.0*y_v_avg_bell_PEN[i]) for i in range(expnum_PEN)]
y_v_avg_myo_PEN = [100.0*RESset_myo_PEN[i][0]/(1.0*y_v_avg_bell_PEN[i]) for i in range(expnum_PEN)]
y_v_avg_rnd_PEN = [100.0*RESset_rnd_PEN[i][0]/(1.0*y_v_avg_bell_PEN[i]) for i in range(expnum_PEN)]
y_v_avg_zero_PEN = [100.0*RESset_zero_PEN[i][0]/(1.0*y_v_avg_bell_PEN[i]) for i in range(expnum_PEN)]
y_v_avg_one_PEN = [100.0*RESset_one_PEN[i][0]/(1.0*y_v_avg_bell_PEN[i]) for i in range(expnum_PEN)]
y_v_avg_bell_PEN = [100 for i in range(expnum_PEN)]

# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list_PEN,y_v_avg_fast_PEN,color='black',markerfacecolor='grey', markeredgecolor='black', marker='h',markersize=8,label='FAST')
plot(x_axis_list_PEN,y_v_avg_bell_PEN,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP', linestyle='-')
plot(x_axis_list_PEN,y_v_avg_myo_PEN,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO', linestyle='--')
plot(x_axis_list_PEN,y_v_avg_rnd_PEN,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list_PEN,y_v_avg_zero_PEN,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LOC', linestyle='--')
plot(x_axis_list_PEN,y_v_avg_one_PEN,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='OFF', linestyle='--')
xlabel('Penalty $c_{pen}$',fontsize=14)
ylabel('User\'s raletive expected cost ($\%$)',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best',fancybox=True)
ylim([99.9, 107.9])
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('../results/FAST_algo/figure2.pdf')
plt.savefig(pp, format='pdf')
pp.close()

# show()