'''
Created on 26 Aug, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
import random

from Core.header import *
from multiprocessing import Process, Queue, Array, Value


def ImmediateCost(g1,q1,n1, act, params):
    def BaseCostG(G=-1):
#         baseG = [0,    0.01,0.1,0.2,0.15] #[0, 1234]
        baseG = [0,   0.1, 0.1, 10.0, 0.01] # in KBs
        #baseG = [0,   0.1*1000, 0.1*1000, 10.0*1000, 0.01*1000] # in MBs
        if -1==G:
            print "error in FUNCTION: BaseCostG(G)"
            exit(-1)
        else:
            return baseG[G]
        
    def c_r(G, Q, N, act, params): # Cost of pure remote execution
        eta_CONST = ETAAvail(params)
        penalty_input = params['PENALTY']
        aph_r_CONST = params['ALPHA_REMOTE']
        
        if 0==G or 0==Q:
            return 0
        if 0==N or 0.0==eta_CONST:
            return 13800138000.0 # NO WAY TO OFFLOAD SINCE N==0
        if 1==act: # Remote execution
            return (1.0+aph_r_CONST*((1.0-eta_CONST)**N)*penalty_input)*BaseCostG(G) #The second term is Penalty
#             print 'NOTE THAT COST OF OFFLOADING HAS CHANGED'
#             return (10.0+((1.0-eta_CONST)**N)*penalty_input)*BaseCostG(G) #The second term is Penalty
            #return 1.0
        else:
            return 0

    def c_l(G, Q, N, act, params): # Cost of pure local execution
        Q_max_CONST = params['Q']
        aph_l_CONST = params['ALPHA_LOCAL']
        
        def coef_local_G(G):
            if BaseCostG(G)<=0.011:
                return 1.0
            elif BaseCostG(G)>0.011 and BaseCostG(G)<=1.0:
                return 1.0
            elif BaseCostG(G)>1.0:
                return 10.0
                
        if 0==G or 0==Q:
            return 0
        if (Q_max_CONST-Q)==0:
            print "WARNING, DIVIDING ZERO! in cl(...)"
            exit(-1)
        if 0==act: # Local execution
#             print 'NOTE THAT COST OF LOCALEXECUTION HAS CHANGED'
            return (coef_local_G(G) + aph_l_CONST*(Q*1.0)/((Q_max_CONST-1)*1.0))*BaseCostG(G)
        else:
            return 0
    
    if 1 == act:
        return c_r(g1,q1,n1, act, params)
    elif 0 == act:
        return c_l(g1,q1,n1, act, params)
    else:
        print "error in Immediatecost()"
        exit(-1)

def BellmanSolver(TransProb, params):
    ## COST INSIDE IN THE ORIGINAL CODES???
    
    print "MDP starts..."
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])

    V_op = np.zeros(( params['G'], params['Q'], params['N'] ))
    A_op = np.zeros(( params['G'], params['Q'], params['N'] ), dtype=np.int)
    
    while 1:
        delta = 0.0
        for g1 in rangeG:
            for q1 in rangeQ:
                for n1 in rangeN:
                    _v_old = V_op[g1][q1][n1]
                    _v_temp = [None, None]
                    for act in [0,1]:
                        _s_tmp = 0.0
                        for g2 in rangeG:
                            for q2 in rangeQ:
                                for n2 in rangeN:
                                    _s_tmp = _s_tmp + TransProb[g1][q1][n1][g2][q2][n2][act] * V_op[g2][q2][n2]
                        _v_temp[act] = ImmediateCost(g1,q1,n1, act, params) + params['GAM'] * _s_tmp
                    _v_min = min(_v_temp[0], _v_temp[1])
                    _a_min = [_v_temp[0], _v_temp[1]].index(_v_min)
                    V_op[g1][q1][n1] = _v_min
                    A_op[g1][q1][n1] = _a_min
                    
                    delta = delta if delta>np.fabs(V_op[g1][q1][n1]-_v_old) else np.fabs(V_op[g1][q1][n1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            print "MDP [DONE]"
            print
            return V_op, A_op
        

def NaiveSolver_Myopic(TransProb, params):
    print "Myopic starts..."
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])

    V_op = np.zeros(( params['G'], params['Q'], params['N'] ))
    A_op = np.zeros(( params['G'], params['Q'], params['N'] ), dtype=np.int)
    
    for g1 in rangeG:
        for q1 in rangeQ:
            for n1 in rangeN:
                _v_temp = min(ImmediateCost(g1,q1,n1, 0, params), ImmediateCost(g1,q1,n1, 1, params) )
                _a_temp = [ImmediateCost(g1,q1,n1, 0, params), ImmediateCost(g1,q1,n1, 1, params)].index(_v_temp)
                A_op[g1][q1][n1] = _a_temp
    
    while 1:
        delta = 0.0
        for g1 in rangeG:
            for q1 in rangeQ:
                for n1 in rangeN:
                    _v_old = V_op[g1][q1][n1]
                    act = A_op[g1][q1][n1]
                    _s_tmp = 0.0
                    for g2 in rangeG:
                        for q2 in rangeQ:
                            for n2 in rangeN:
                                _s_tmp = _s_tmp + TransProb[g1][q1][n1][g2][q2][n2][act] * V_op[g2][q2][n2]
                    V_op[g1][q1][n1] = ImmediateCost(g1,q1,n1, act, params) + params['GAM'] * _s_tmp
                    
                    delta = delta if delta>np.fabs(V_op[g1][q1][n1]-_v_old) else np.fabs(V_op[g1][q1][n1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            print "Myopic [DONE]"
            print
            return V_op, A_op


def NaiveSolver_Rnd(TransProb, params):
    print "Random..."
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])

    V_op = np.zeros(( params['G'], params['Q'], params['N'] ))
    A_op = np.zeros(( params['G'], params['Q'], params['N'] ), dtype=np.int)
    
    for g1 in rangeG:
        for q1 in rangeQ:
            for n1 in rangeN:
                A_op[g1][q1][n1] = random.randint(0,1)
                if 0 == n1:
                    A_op[g1][q1][n1] = 0
    
    while 1:
        delta = 0.0
        for g1 in rangeG:
            for q1 in rangeQ:
                for n1 in rangeN:
                    _v_old = V_op[g1][q1][n1]
                    act = A_op[g1][q1][n1]
                    _s_tmp = 0.0
                    for g2 in rangeG:
                        for q2 in rangeQ:
                            for n2 in rangeN:
                                _s_tmp = _s_tmp + TransProb[g1][q1][n1][g2][q2][n2][act] * V_op[g2][q2][n2]
                    V_op[g1][q1][n1] = ImmediateCost(g1,q1,n1, act, params) + params['GAM'] * _s_tmp
                    
                    delta = delta if delta>np.fabs(V_op[g1][q1][n1]-_v_old) else np.fabs(V_op[g1][q1][n1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op
        

def NaiveSolver_Always(TransProb, FixAction, params):
    print "Random..."
    rangeG, rangeQ, rangeN = range(params['G']), range(params['Q']), range(params['N'])

    V_op = np.zeros(( params['G'], params['Q'], params['N'] ))
    A_op = np.zeros(( params['G'], params['Q'], params['N'] ), dtype=np.int)
    
    for g1 in rangeG:
        for q1 in rangeQ:
            for n1 in rangeN:
                if 0 == FixAction:
                    A_op[g1][q1][n1] = 0
                elif 1 == FixAction:
                    A_op[g1][q1][n1] = 1
                    if 0 == n1:
                        A_op[g1][q1][n1] = 0
                else:
                    print "error action! NaiveSolver_Always()"
                    exit(-1)
    
    while 1:
        delta = 0.0
        for g1 in rangeG:
            for q1 in rangeQ:
                for n1 in rangeN:
                    _v_old = V_op[g1][q1][n1]
                    act = A_op[g1][q1][n1]
                    _s_tmp = 0.0
                    for g2 in rangeG:
                        for q2 in rangeQ:
                            for n2 in rangeN:
                                _s_tmp = _s_tmp + TransProb[g1][q1][n1][g2][q2][n2][act] * V_op[g2][q2][n2]
                    V_op[g1][q1][n1] = ImmediateCost(g1,q1,n1, act, params) + params['GAM'] * _s_tmp
                    
                    delta = delta if delta>np.fabs(V_op[g1][q1][n1]-_v_old) else np.fabs(V_op[g1][q1][n1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op
        
################################################################################################
        

        
        
def NaiveSolver_Side(TransProb, params):
    print "Taking side action scheme..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    
    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    if l1 in params['L_NC']:
                        A_op[l1][e1][n1][p1] = 0
                    elif l1 in params['L_B']:
                        A_op[l1][e1][n1][p1] = 1
                    elif l1 in params['L_S']:
                        A_op[l1][e1][n1][p1] = 2
                    else:
                        print "ERROR in NaiveSolver_Side(TransProb, params)"
                        exit(0)
                        

    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        act = A_op[l1][e1][n1][p1]
                        _s_tmp = 0.0
                        for l2 in rangeL:
                            for e2 in rangeE:
                                for n2 in rangeN:
                                    for p2 in rangeP:
                                        _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                        V_op[l1][e1][n1][p1] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                      
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)

        print "Delta=",delta
        if delta< params['DELTA']:
            print "Taking side action scheme [DONE]"
            print
            return V_op, A_op



def NaiveSolver_SideRandom(TransProb, params):
    print "Random..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']

    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    if l1 in params['L_NC']:
                        A_op[l1][e1][n1][p1] = 0
                    elif l1 in params['L_B']:
                        A_op[l1][e1][n1][p1] = random.randint(0,1)
                    elif l1 in params['L_S']:
                        A_op[l1][e1][n1][p1] = random.randint(0,2)
                    else:
                        A_op[l1][e1][n1][p1] = 0
    
    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        act = A_op[l1][e1][n1][p1]
                        _s_tmp = 0.0
                        for l2 in rangeL:
                            for e2 in rangeE:
                                for n2 in rangeN:
                                    for p2 in rangeP:
                                        _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                        V_op[l1][e1][n1][p1] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op