'''
Created on Oct 19, 2014

@author: yzhang28
'''
import pickle
from multiprocessing import Pool, Array

import timeit


import sys
sys.path.append("..")

from Core.MDPfunc import *
from Core.header import *

############################################
# PARAMETERS
############################################
G = 1 + 4
Q = 1 + 6
# N Calculated from LAM and R_COVERAGE at last
A = 2 # two actions: 0 and 1

# R_COVERAGE = 15.0
R_COVERAGE = 10.0 # by default

LAM_Q = 0.25
LAM_C = 0.0005
LAM_U = 0.0001

TAU = 0.5
C_TOP = 2
BETAH = 0.5
VELOCITY = 5.0

PENALTY = 2.5

# ALPHA_LOCAL = 1.0
# ALPHA_REMOTE = 1.0

GAM = 0.80
DELTA = 0.01
############################################


R_list = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]

PEN_list = [0.0, 2.0, 4.0, 6.0, 8.0]

expnum_R = len(R_list)
ParamsSet_R = [None for _ in range(expnum_R)]
TransProbSet_R = [None for _ in range(expnum_R)]
RESset_fast_R = [None for _ in range(expnum_R)]

expnum_PEN = len(PEN_list)
ParamsSet_PEN = [None for _ in range(expnum_PEN)]
TransProbSet_PEN = [None for _ in range(expnum_PEN)]
RESset_fast_PEN = [None for _ in range(expnum_PEN)]
 
 
tic = timeit.default_timer()
 
for ind, r_cur in enumerate(R_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum_R
    N = GetUpperboundN(LAM_C, r_cur)[0]
    ParamsSet_R[ind] = {'G': G, 'Q': Q, 'N': N, \
                      'A': A, \
                      'R_COVERAGE': r_cur, \
                      'LAM_Q': LAM_Q, 'LAM_C': LAM_C, 'LAM_U': LAM_U, \
                      'TAU': TAU, 'C_TOP': C_TOP, 'BETAH':BETAH, 'VELOCITY':VELOCITY, \
                      'PENALTY': PENALTY, \
#                       'ALPHA_LOCAL': ALPHA_LOCAL, 'ALPHA_REMOTE': ALPHA_REMOTE, \
                      'GAM': GAM, 'DELTA': DELTA
                      }
    # BUILD TRANS MAT _ PARALELL #
    TransProbSet_R[ind] = BuildTransMatrix_Para(ParamsSet_R[ind])
     
    # fast algo
    V_fast, A_fast = NaiveSolver_FastAlgo(TransProbSet_R[ind], ParamsSet_R[ind])
    RESset_fast_R[ind] = GetOptResultList(V_fast,A_fast, TransProbSet_R[ind], ParamsSet_R[ind])
       
     
toc = timeit.default_timer()
print
print "Total time spent: ",
print toc - tic
     
print "Dumping...",
pickle.dump(expnum_R, open("../results/FAST_algo/expnum_R","w"))
pickle.dump(ParamsSet_R, open("../results/FAST_algo/Paramsset_R","w"))
pickle.dump(R_list, open("../results/FAST_algo/xaxis_R","w"))
pickle.dump(RESset_fast_R, open("../results/FAST_algo/fast_R","w"))
print "Finished R...continue..."




tic = timeit.default_timer()

for ind, pen_cur in enumerate(PEN_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum_PEN
    N = GetUpperboundN(LAM_C, R_COVERAGE)[0]
    ParamsSet_PEN[ind] = {'G': G, 'Q': Q, 'N': N, \
                      'A': A, \
                      'R_COVERAGE': R_COVERAGE, \
                      'LAM_Q': LAM_Q, 'LAM_C': LAM_C, 'LAM_U': LAM_U, \
                      'TAU': TAU, 'C_TOP': C_TOP, 'BETAH':BETAH, 'VELOCITY':VELOCITY, \
                      'PENALTY': pen_cur, \
#                       'ALPHA_LOCAL': ALPHA_LOCAL, 'ALPHA_REMOTE': ALPHA_REMOTE, \
                      'GAM': GAM, 'DELTA': DELTA
                      }
    # BUILD TRANS MAT _ PARALELL #
    TransProbSet_PEN[ind] = BuildTransMatrix_Para(ParamsSet_PEN[ind])
    
    # fast algo
    V_fast, A_fast = NaiveSolver_FastAlgo(TransProbSet_PEN[ind], ParamsSet_PEN[ind])
    RESset_fast_PEN[ind] = GetOptResultList(V_fast,A_fast, TransProbSet_PEN[ind], ParamsSet_PEN[ind])
      
    
toc = timeit.default_timer()
print
print "Total time spent: ",
print toc - tic
    
print "Dumping...",
pickle.dump(expnum_PEN, open("../results/FAST_algo/expnum_PEN","w"))
pickle.dump(ParamsSet_PEN, open("../results/FAST_algo/Paramsset_PEN","w"))
pickle.dump(PEN_list, open("../results/FAST_algo/xaxis_PEN","w"))
pickle.dump(RESset_fast_PEN, open("../results/FAST_algo/fast_PEN","w"))
print "Finished PENALTY"