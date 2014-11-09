'''
Created on 17 Oct, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
from scipy.misc import factorial
from scipy.integrate import quad
import random
import math
from multiprocessing import Pool as ThreadPool
from multiprocessing import Process, Queue, Array, RawArray
import timeit
import time

'''
Pre-defined functions:
WHETHER THE PHASE IS FINISHING PHASE
'''
def ESg(g):
    if 3==g or 4==g:
        return True
    else:
        return False

def G_mat(g1, g2, params):
#     def PGOnlyTransProb(g1=0, g2=0):
    if params.has_key('G_MAT'):
        mat_g = params['G_MAT']
    else:
        #G2=  0    1    2    3    4
        mat_g = [
        [0.0, 0.0, 0.0, 0.0, 0.0], # G1=0
        [0.0, 0.0, 1.0, 0.0, 0.0], #    1
        [0.0, 0.0, 0.0, 0.8, 0.2], #    2
        [0.0, 0.0, 0.0, 0.0, 0.0], #    3
        [0.0, 0.0, 0.0, 0.0, 0.0]  #    4
        ]
        #             ___ 3 
        #            |
        #  1 -- 2 ---<
        #            |___ 4
        #
    if (g1 in range(params['G'])) and (g2 in range(params['G'])):
        return mat_g[g1][g2]
    else:
        return 0.0

def ETAAvail(params): #v=0.0,R=10.0):
    def UserSideProb_WorstCase(R_outbound, params):
        lam_u = params['LAM_U']
        lam_au = params['LAM_U'] * 0.1
        betah = params['BETAH'] # betah=0.5
        c = params['C_TOP']  #2
        tau = params['TAU']
        v = params['VELOCITY'] #5.0
        def integrand(r_var,R_top):
            pai = np.pi    
            return np.exp(-2*pai*lam_au*(betah**(2/c))*(r_var**2))*(1-v*tau/(R_top-r_var))*np.exp(-1*pai*lam_u*(r_var**2)) * r_var
        coef = 2.0*np.pi*lam_u/(1-np.exp(-1*np.pi*lam_u*(R_outbound**2)))
        result, err = quad(integrand,0.0,R_outbound-v*tau,args=(R_outbound))
        eta = coef * result
        # return the numerically integrated result of $eta_a$    
        boost_coef = 1.00
        if boost_coef * eta <= 1:
            return boost_coef * eta
        else:
            return 1.0
    def UserSideProb_BestCase(R_outbound, params):
        lam_u = params['LAM_U']
        lam_au = params['LAM_U'] * 0.1
        betah = params['BETAH'] # betah=0.5
        c = params['C_TOP']  #2
        tau = params['TAU']
        v = params['VELOCITY'] #5.0
        def integrand(r,R):
            pai = np.pi    
            return np.exp(-2*pai*lam_au*(betah**(2/c))*(r**2))*(1-v*tau/(R+r))*np.exp(-1*pai*lam_u*(r**2)) * r
        coef = 2.0*np.pi*lam_u/(1-np.exp(-1*np.pi*lam_u*(R_outbound**2)))
        result, err = quad(integrand,0.0,R_outbound,args=(R_outbound))
        eta = coef*result
        # return the numerically integrated result of $eta_a$    
        return eta
    
    if params.has_key('ETA_DIRECT'):
        return params['ETA_DIRECT'] 
    else:
        R = params['R_COVERAGE']
        return ( UserSideProb_WorstCase(R,params) + UserSideProb_BestCase(R,params) ) / 2.0

def G_and_Q_mat(g1,q1, g2,q2, n1, act1, params):
    lam_q_CONST = params['LAM_Q']
    G_max_CONST = params['G']
    Q_max_CONST = params['Q']
    
    eta_CONST = ETAAvail(params)# VELOCITY,R_clt_CONST)
    
    def PoissonFunc(lam,ka):
        return np.exp(-1.0*lam) * (lam**ka) / factorial(ka,exact=True)
    
    '''
    Pre-defined functions:
    Successful prob caused by eta_CONST
    '''
    def ProbETA(n1,eta1,act1):
        if 0==act1:
            return 1
        else: # when act==1
            return 1.0-np.power((1.0-eta1),n1)
    
    #
    if g1==0 and g2==0 and q1==0 and q2==0:
        return PoissonFunc(lam_q_CONST,0)
    
    #
    if g1==0 and g2==1 and q1==0 and q2>=1 and q1<=(Q_max_CONST-1):
        return PoissonFunc(lam_q_CONST,q2-q1)
    
    #1
    if g1>0 and (ESg(g1)==False) and g1<=(G_max_CONST-1) and g1!=g2 and 0<q1 and q1<(Q_max_CONST-1) and q1<=q2 and q2<(Q_max_CONST-1):
        return ProbETA(n1,eta_CONST,act1)*G_mat(g1,g2,params)*PoissonFunc(lam_q_CONST,q2-q1)
    
    #2
    if g1>0 and (ESg(g1)==False) and g1<=(G_max_CONST-1) and g1!=g2 and 0<q1 and q1<(Q_max_CONST-1) and (Q_max_CONST-1)==q2:
        sum_tmp = 0.0
        for k in range(q1,Q_max_CONST-1): #\mathcal{Q},\mathcal{Q}+1,...,(Q_max_CONST-1)-1 (i.e., Q-1)
            sum_tmp = sum_tmp + PoissonFunc(lam_q_CONST, (k-q1)) 
        return ProbETA(n1,eta_CONST,act1) * G_mat(g1,g2,params) * (1.0-sum_tmp)

    #3
    if g1>0 and (ESg(g1)==False) and g1<=(G_max_CONST-1) and g1!=g2 and (Q_max_CONST-1)==q1 and (Q_max_CONST-1)==q2:
        return ProbETA(n1,eta_CONST,act1) * G_mat(g1,g2,params)
    
    #4
    if g1>0 and g1==g2 and g1<=(G_max_CONST-1) and 0<q1 and q1<(Q_max_CONST-1) and q1<=q2 and q2<(Q_max_CONST-1):
        return (1.0 - ProbETA(n1,eta_CONST,act1)) * PoissonFunc(lam_q_CONST, q2-q1)
    
    #5
    if g1>0 and g1==g2 and g1<=(G_max_CONST-1) and 0<q1 and q1<(Q_max_CONST-1) and (Q_max_CONST-1)==q2:
        sum_tmp = 0.0
        for k in range(q1,Q_max_CONST-1):
            sum_tmp = sum_tmp + PoissonFunc(lam_q_CONST, (k-q1)) 
        return (1.0 - ProbETA(n1,eta_CONST,act1)) * (1.0-sum_tmp)
    
    #6
    if g1>0 and g1==g2 and g1<=(G_max_CONST-1) and (Q_max_CONST-1)==q1 and (Q_max_CONST-1)==q2:
        return 1.0 - ProbETA(n1,eta_CONST,act1)
     
    
    #7,8-1
    if (ESg(g1)==True) and 1==g2 and q1>1 and q1<=(Q_max_CONST-1) and q2>=q1-1 and q2<(Q_max_CONST-1):
        return ProbETA(n1,eta_CONST,act1) * PoissonFunc(lam_q_CONST,q2-(q1-1))
    
    #7,8-1-1
    if (ESg(g1)==True) and 0==g2 and 1==q1 and q2>=q1-1 and q2<(Q_max_CONST-1):
        return ProbETA(n1,eta_CONST,act1) * PoissonFunc(lam_q_CONST,q2-(q1-1))
    
    #7,8-2
    if (ESg(g1)==True) and 1==g2 and q1>1 and q1<=(Q_max_CONST-1) and q2==(Q_max_CONST-1):
        sum_tmp = 0.0
        for k in range((q1-1),Q_max_CONST-1): #\mathcal{Q},\mathcal{Q}+1,...,(Q_max_CONST-1)-1 (i.e., Q-1)
            sum_tmp = sum_tmp + PoissonFunc(lam_q_CONST, (k-(q1-1))) 
        return ProbETA(n1,eta_CONST,act1) * (1.0-sum_tmp)
    
    #7,8-2-1
    if (ESg(g1)==True) and 0==g2 and 1==q1 and q2==(Q_max_CONST-1):
        sum_tmp = 0.0
        for k in range((q1-1),Q_max_CONST-1): #\mathcal{Q},\mathcal{Q}+1,...,(Q_max_CONST-1)-1 (i.e., Q-1)
            sum_tmp = sum_tmp + PoissonFunc(lam_q_CONST, (k-(q1-1))) 
        return ProbETA(n1,eta_CONST,act1) * (1.0-sum_tmp)
    
    #9
    else:
        return 0.0
    
def P_SpatialPoisson_Pure(k, LAM, R_COVERAGE):
    return np.exp(-1*math.pi*LAM*np.power(R_COVERAGE,2))*np.power(math.pi*LAM*np.power(R_COVERAGE,2), k)/factorial(k)

def GetUpperboundN(LAM, R_COVERAGE):
    _n = 0
    _sum = 0.0
    while 1:
        _sum = _sum + P_SpatialPoisson_Pure(_n, LAM, R_COVERAGE)
        _residual = 1.0 - _sum
        if _residual < 0.0001:
            return _n + 1, _residual
        else:
            _n = _n + 1

def N_mat(n1,n2, params):
    _LAM_C = params['LAM_C']
    _R_COVERAGE = params['R_COVERAGE']
    _N, _residual = GetUpperboundN(_LAM_C, _R_COVERAGE)
    
    if n1 not in range(_N):
        return 0.0
    else:
        if n2 not in range(_N):
            return 0.0
        elif n2==_N-1:
            return P_SpatialPoisson_Pure(n2, _LAM_C, _R_COVERAGE) + _residual
        else:
            return P_SpatialPoisson_Pure(n2, _LAM_C, _R_COVERAGE)


def OverallTransProb(g1,q1,n1, g2,q2,n2, act, params):
    G_max_CONST = params['G']
    Q_max_CONST = params['Q']
#     LAM_C = params['LAM_C']
#     R_COVERAGE = params['R_COVERAGE']
    N_max = params['N']
    
    if g1>(G_max_CONST-1) or g2>(G_max_CONST-1) or q1>(Q_max_CONST-1) or q2>(Q_max_CONST-1) or n1>(N_max-1) or n2>(N_max-1):
        print "my error signal, out of bound. Pos - header.py: OverallTransProb()"
        exit(-1)
    else:
        return 1.0 * G_and_Q_mat(g1,q1, g2,q2, n1,act, params) * N_mat(n1,n2, params)


def ShowMatrix(Mat, mode, fixdim, fixnum, params):
    if Mat==None:
        print "ERROR INPUT ShowMatrix()"
        exit()
        
    if mode=='a': # Show action
        print "---ACTION MATRIX---"
    elif mode=='v': # Show value
        print "---UTILITY MATRIX---"
    else:
        print "ERROR, UNKNOWN MATRIX"
        exit()
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])
    dimList = ['g', 'q', 'n']
    feasList = [rangeG, rangeQ, rangeN]
    
    del(feasList[dimList.index(fixdim)])
    del(dimList[dimList.index(fixdim)])
    print 'Line: ', dimList[0]
    print 'Column: ', dimList[1]
    
    fix = fixnum
    for ra in feasList[0]:
        for rb in feasList[1]:
            if fixdim=='g':
                if mode=='a':
                    print "%d" % Mat[fix][ra][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[fix][ra][rb],
                else:
                    print "ERROR, POS 1"
                    exit()
                print ' ',
            elif fixdim=='q':
                if mode=='a':
                    print "%d" % Mat[ra][fix][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][fix][rb],
                else:
                    print "ERROR, POS 2"
                    exit()
                print ' ',
            elif fixdim=='n':
                if mode=='a':
                    print "%d" % Mat[ra][rb][fix],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][rb][fix],
                else:
                    print "ERROR, POS 3"
                    exit()
                print ' ',
            else:
                print "ERROR, POS 4"
                exit()
        print


def HashMatIndex(ind_mat, max_dimension_sizes_list):
    # Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
    if not len(ind_mat)==len(max_dimension_sizes_list):
        print "Error in HashMatIndex"
        exit(0)
    prodnt = np.append(np.delete(max_dimension_sizes_list,0),1)
    _sum = 0
    for i,item in enumerate(ind_mat):
        _tmp = 1
        for j in range(i,len(prodnt)):
            _tmp = _tmp * prodnt[j]
        _sum = _sum + item*_tmp
    return int(_sum)


def ReversedHashMatIndex(ind_lin, max_dimension_sizes_list):
# INPUT 1: The index in the linear matrix
# INPUT 2: A list, containing the maximum size of each dimension in the multi-dimensional matrix.
# REVERSED Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
    rem = ind_lin
    _mod_list = [item for item in reversed(max_dimension_sizes_list)]
    ind_mat = []
    
    for i in _mod_list:
        rem, mod_num = divmod(rem, i)
        ind_mat.insert(0, mod_num)
    
    return ind_mat


def SlicingListToSections(sec_list, proc_num, total_number):
    for i in range(proc_num):
        if i==0:
            _start = int(total_number/proc_num)*i
            _end = int(total_number/proc_num)*(i+1)
        elif i==proc_num-1:
            _start = int(total_number/proc_num)*i
            _end = total_number
        else:
            _start = int(total_number/proc_num)*i
            _end = int(total_number/proc_num)*(i+1)
        sec_list.append(range(_start, _end))

def BuildTransMatrix_Para(params):   
    
    def subfunc_MatCalc(arr,sec, params):
        _len_G, _len_Q, _len_N = params['G'], params['Q'], params['N'] 
        _len_A = params['A']
        _dimension_size = [_len_G, _len_Q, _len_N,  _len_G, _len_Q, _len_N,  _len_A]
        
        for _ind_lin in sec:
            g1,q1,n1, g2,q2,n2, act = ReversedHashMatIndex(_ind_lin, _dimension_size)
            _c = OverallTransProb(g1,q1,n1, g2,q2,n2, act, params)
            arr[_ind_lin] = _c 

    
    _len_G, _len_Q, _len_N = params['G'], params['Q'], params['N'] 
    _len_A = params['A']
    _total_cnt = (_len_G * _len_Q * _len_N) * (_len_G * _len_Q * _len_N) * _len_A
    trans_prob_linear = Array('d', np.zeros(_total_cnt))
    
    sec = []
    PROCNUM = 12
    SlicingListToSections(sec, PROCNUM, _total_cnt)

    p = []
    print 'Building transition matrix...'
    for i in range(len(sec)):
        proc = Process(target=subfunc_MatCalc, args=(trans_prob_linear, sec[i], params))
        proc.start()
        p.append(proc)
        
    for proc in p:
        proc.join()
    
    trans_prob_mat = np.asarray(trans_prob_linear).reshape(_len_G, _len_Q, _len_N, _len_G, _len_Q, _len_N, _len_A)

    print 'Building transition matrix...[DONE]'
    return trans_prob_mat


def BuildTransMatrix(params):
    rangeG = range(params['G'])
    rangeQ = range(params['Q'])
    rangeN = range(params['N'])
    rangeA = range(params['A'])
    _len_G, _len_Q, _len_N = params['G'], params['Q'], params['N'] 
    _len_A = params['A']
     
    trans_prob_mat = np.zeros((_len_G, _len_Q, _len_N,  _len_G, _len_Q, _len_N,  _len_A))
     
    print 'Building transition matrix...'
     
    for g1 in rangeG:
        for q1 in rangeQ:
            for n1 in rangeN:
                for g2 in rangeG:
                    for q2 in rangeQ:
                        for n2 in rangeN:
                            for act in rangeA:
                                trans_prob_mat[g1][q1][n1][g2][q2][n2][act] = OverallTransProb(g1,q1,n1, g2,q2,n2, act, params)
     
    print 'Building transition matrix...[DONE]'
    return trans_prob_mat


def GetOptResultList(V,A, transmat, params):
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])
    _len_G, _len_Q, _len_N = params['G'], params['Q'], params['N']
#     steady_mat = SteadyStateMatrix(transmat, A, params)
         
    V_linear = V.reshape(1, _len_G*_len_Q*_len_N)[0]    
    v_avg = np.average(V_linear) # AVERAGE COST
    A_linear = A.reshape(1, _len_G*_len_Q*_len_N)[0]
    _act_0 = A_linear.tolist().count(0)
    _act_1 = A_linear.tolist().count(1)
    _act_sum = _act_0 + _act_1
    if not (_act_sum==len(A_linear)):
        print "error in GetOptResultList"
        exit(-1) 
    
    a1_avg = _act_1*1.0/(1.0*len(A_linear)) # ACT_1_AVG
     
#     e_steady = 0.0
#     QoS_steady = 0.0
#     a1_steady = 0.0
#     a2_steady = 0.0
#     for l1 in rangeL:
#         for e1 in rangeE:
#             for n1 in rangeN:
#                 for p1 in rangeP:
#                     e_steady = e_steady + 1.0 * e1 * steady_mat[l1][e1][n1][p1]
#                     if A[l1][e1][n1][p1] == 1:
#                         a1_steady = a1_steady + 1.0 * steady_mat[l1][e1][n1][p1]
#                     if A[l1][e1][n1][p1] == 2:
#                         a2_steady = a2_steady + 1.0 * steady_mat[l1][e1][n1][p1]
#                     if (l1 in params['L_S']) and (e1>=params['E_S']) and (A[l1][e1][n1][p1]==2):
#                         QoS_steady = QoS_steady +  1.0*steady_mat[l1][e1][n1][p1]
    return v_avg, a1_avg
#     return v_avg, a1_steady, a2_steady, e_steady, QoS_steady
# #            0       1           2         3          4






# %-------------------------------------------------------------



# def SteadyStateMatrix(transmat, optA, params):
#     rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
#     total_dim = params['L'] * params['E'] * params['N'] * params['P']
#     expanded_matrix = np.matrix( [[0.0 for _ in range(total_dim)] for _ in range(total_dim)] )
#     search_list = [[[[-1 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
#     
#     expd_x_ind, expd_y_ind = 0, 0
#     for l1 in rangeL:
#         for e1 in rangeE:
#             for n1 in rangeN:
#                 for p1 in rangeP:
#                     for l2 in rangeL:
#                         for e2 in rangeE:
#                             for n2 in rangeN:
#                                 for p2 in rangeP:
#                                     act = optA[l1][e1][n1][p1]
#                                     expanded_matrix[expd_x_ind, expd_y_ind] = transmat[l1][e1][n1][p1][l2][e2][n2][p2][act]
#                                     expd_y_ind = expd_y_ind + 1
#                     search_list[l1][e1][n1][p1] = expd_x_ind
#                     expd_x_ind = expd_x_ind + 1
#                     expd_y_ind = 0
#     
#     p_hat = expanded_matrix - np.diag(np.array([1.0 for _ in range(total_dim)]))
#     for x in range(total_dim):
#         p_hat[x,total_dim-1] = 1.0
#     a_rhs = np.zeros(total_dim)
#     a_rhs[total_dim-1] = 1.0
#     steady_p = a_rhs * p_hat.getI()
#     steady_p_transf = [[[[-1 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
#     
#     for l in rangeL:
#         for e in rangeE:
#             for n in rangeN:
#                 for p in rangeP:
#                     steady_p_transf[l][e][n][p] = steady_p[0,search_list[l][e][n][p]]
#     return steady_p_transf
#     
# 
# 
# def GetOptResultList(V,A, transmat, params):
#     rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']
#     steady_mat = SteadyStateMatrix(transmat, A, params)
#         
#     V_linear = V.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]    
#     v_avg = np.average(V_linear) # AVERAGE COST
#     A_linear = A.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]
#     _act = np.bincount(A_linear)
#     while len(_act) < 3:
#         _act = np.append(_act, 0)
#     a1_avg = _act[1]*1.0/(1.0*len(A_linear)) # ACT_1_AVG
#     a2_avg = _act[2]*1.0/(1.0*len(A_linear)) # ACT_2_AVG
#     
#     e_steady = 0.0
#     QoS_steady = 0.0
#     a1_steady = 0.0
#     a2_steady = 0.0
#     for l1 in rangeL:
#         for e1 in rangeE:
#             for n1 in rangeN:
#                 for p1 in rangeP:
#                     e_steady = e_steady + 1.0 * e1 * steady_mat[l1][e1][n1][p1]
#                     if A[l1][e1][n1][p1] == 1:
#                         a1_steady = a1_steady + 1.0 * steady_mat[l1][e1][n1][p1]
#                     if A[l1][e1][n1][p1] == 2:
#                         a2_steady = a2_steady + 1.0 * steady_mat[l1][e1][n1][p1]
#                     if (l1 in params['L_S']) and (e1>=params['E_S']) and (A[l1][e1][n1][p1]==2):
#                         QoS_steady = QoS_steady +  1.0*steady_mat[l1][e1][n1][p1]
#     
#     return v_avg, a1_steady, a2_steady, e_steady, QoS_steady
# #            0       1           2         3          4

