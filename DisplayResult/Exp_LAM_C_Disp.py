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
sys.path.append("..")
from Core.MDPfunc import *

from matplotlib.backends.backend_pdf import PdfPages

expnum = pickle.load(open("../results/LAM_C_changing/expnum","r"))

x_axis_list = pickle.load(open("../results/LAM_C_changing/xaxis","r"))
for i in range(len(x_axis_list)):
    x_axis_list[i] = x_axis_list[i] * 1000
RESset_bell = pickle.load(open("../results/LAM_C_changing/bell","r"))
RESset_myo = pickle.load(open("../results/LAM_C_changing/myo","r"))
RESset_rnd = pickle.load(open("../results/LAM_C_changing/rnd","r"))
RESset_zero = pickle.load(open("../results/LAM_C_changing/zero","r"))
RESset_one = pickle.load(open("../results/LAM_C_changing/one","r"))

# V_opt_set_bell = pickle.load(open("../results/LAM_C_changing/V_opt_bell","r"))
# A_opt_set_bell = pickle.load(open("../results/LAM_C_changing/A_opt_bell","r"))


y_v_avg_bell = [RESset_bell[i][0] for i in range(expnum)]
y_a1_bell = [RESset_bell[i][1] for i in range(expnum)]
 
 
y_v_avg_myo = [RESset_myo[i][0] for i in range(expnum)]
y_a1_myo = [RESset_myo[i][1] for i in range(expnum)]
 
y_v_avg_rnd = [RESset_rnd[i][0] for i in range(expnum)]
y_a1_rnd = [RESset_rnd[i][1] for i in range(expnum)]

y_v_avg_zero = [RESset_zero[i][0] for i in range(expnum)]
y_a1_zero = [RESset_zero[i][1] for i in range(expnum)]

y_v_avg_one = [RESset_one[i][0] for i in range(expnum)]
y_a1_one = [RESset_one[i][1] for i in range(expnum)]


# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_v_avg_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_v_avg_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO', linestyle='--')
plot(x_axis_list,y_v_avg_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_v_avg_zero,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LOC', linestyle='--')
plot(x_axis_list,y_v_avg_one,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='OFF', linestyle='--')
xlabel('Cloudlet density $\lambda_c$ ($\\times 10^3$)',fontsize=14)
ylabel('User\'s expected cost',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best',fancybox=True, ncol=2)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('../results/LAM_C_changing/figure2.pdf')
plt.savefig(pp, format='pdf')
pp.close()


# Show steady action 1
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_a1_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_a1_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO', linestyle='--')
plot(x_axis_list,y_a1_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_a1_zero,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LOC')
# plot(x_axis_list,y_a1_one,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='OFF')
xlabel('Cloudlet density $\lambda_c$ ($\\times 10^3$)',fontsize=14)
ylabel('Offloading rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.04,0.48),fancybox=True)
locs, labels = plt.yticks()
ylim([0.101,0.44])
plt.setp(labels, rotation=90)
pp = PdfPages('../results/LAM_C_changing/figure1.pdf')
plt.savefig(pp, format='pdf')
pp.close()

# show()