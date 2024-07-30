# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:56:54 2023

@author: barbh
"""

import numpy as np
from scipy.linalg import sqrtm
import networkx as nx
from SI import *
import community
import random
import math


# V = ['A', 'B', 'C']
# E = [('A', 'B'), ('B', 'C'),('A', 'C')]
# W = {('A', 'B'): 0.5, ('B', 'A'): 0.5, ('B', 'C'): 0.7, ('C', 'B'): 0.3, ('A', 'C'): 0.4, ('C', 'A'): 0.5}
# m = 2
def likelihood(Gs, bfs_tree, sensor_nodes, Delta_t):
    likelihood = 0
    for Gj in Gs:
        time_of_diffusion = diffusion(bfs_tree)
        for node in Gj:
            if node not in time_of_diffusion.keys(): 
                time_of_diffusion[node]=-1
        
        P_G = 1 / len(Gs)
    
        mu_vj = mu(time_of_diffusion, sensor_nodes)
        lamda_vj = lamda(time_of_diffusion, sensor_nodes)
        
        sub = np.subtract(Delta_t,mu_vj)
        
        det_Lambda_vj = np.linalg.det(lamda_vj)
        #print(np.subtract(Delta_t, mu_vj))
        exponent = -0.5 * abs(np.dot(np.dot(np.subtract(Delta_t, mu_vj), np.linalg.inv(lamda_vj)), np.transpose(np.subtract(Delta_t, mu_vj))))
        likelihood += P_G / np.sqrt(det_Lambda_vj) * np.exp(exponent)
    return likelihood

def likelihood_cg(Gs, G, bfs_tree, sensor_nodes, Delta_t):
    likelihood = 0
    for Gj in Gs:
        time_of_diffusion = diffusion_cluster(bfs_tree, G)
        for node in Gj:
            if node not in time_of_diffusion.keys(): 
                time_of_diffusion[node]=-1
        
        P_G = 1 / len(Gs)
    
        mu_vj = mu(time_of_diffusion, sensor_nodes)
        lamda_vj = lamda(time_of_diffusion, sensor_nodes)
        
        sub = np.subtract(Delta_t,mu_vj)
        
        det_Lambda_vj = np.linalg.det(lamda_vj)
        #print(np.subtract(Delta_t, mu_vj))
        exponent = -0.5 * abs(np.dot(np.dot(np.subtract(Delta_t, mu_vj), np.linalg.inv(lamda_vj)), np.transpose(np.subtract(Delta_t, mu_vj))))
        likelihood += P_G / np.sqrt(det_Lambda_vj) * np.exp(exponent)
    return likelihood

def mu(time_of_diffusion, sensor_nodes):
    min_v = min([time_of_diffusion[i] for i in sensor_nodes])
    min_n = -1
    for i in sensor_nodes:
        if time_of_diffusion[i] == min_v:
            min_n = i
            break
    return [abs(time_of_diffusion[i]+min_v)/2 for i in sensor_nodes if(i != min_n)]



def lamda(time_of_diffusion, sensor_nodes):
    arrivals = []
    for sensor in sensor_nodes:
            if(time_of_diffusion[sensor]==-1):
                arrivals.append(200)
            else:
                arrivals.append(time_of_diffusion[sensor])
                
    new_delta_ts = []
    for i in range(0,len(arrivals)):
        new_delta_t=[]
        for j in range(0,len(arrivals)):
            if(i!=j):
                new_delta_t.append(abs(arrivals[j]-arrivals[i]))
        new_delta_ts.append(new_delta_t)
        
    lambd = []
    for i in range(0,len(new_delta_ts)-1):
        val = np.correlate(new_delta_ts[i],new_delta_ts[i+1],"same")
        for i in range(0,len(val)):
            if (val[i]==0):
                    val[i]=1
        lambd.append(val)
    lambd[0][1]=0
    return lambd

    

# def probability_of_graph(G):
#     det_sum = 0
#     for v in G['V']:
#         det_sum += np.log(np.linalg.det(G['Lambda'][v]))
#     return np.exp(det_sum)

# def find_m_most_likely_graphs(V, E, W, m):
#     Gs = []
#     for j in range(m):
#         G = {'V': V, 'E': E, 'W': W, 'Lambda': {}, 'mu': {}}
#         for v in V:
#             neighbors = [u for (u, w) in E if u == v or w == v]
#             A = np.zeros((len(neighbors), len(neighbors)))
#             b = np.zeros((len(neighbors),))
#             for i in range(len(neighbors)):
#                 for k in range(len(neighbors)):
#                     if i == k:
#                         A[i, k] = sum([W[u, v] for (u, w) in E if u == neighbors[i] and w != v and u != v] + [W[w, v] for (u, w) in E if u != v and w == neighbors[i] and v != w])
#                     else:
#                         A[i, k] = -W[neighbors[i], neighbors[k]]
#                 b[i] = sum([W[u, v] for (u, w) in E if u == neighbors[i] and w == v] + [W[w, v] for (u, w) in E if u == v and w == neighbors[i]])
#     #         G['Lambda'][v] = np.linalg.inv(A)
#     #         G['mu'][v] = np.dot(G['Lambda'][v], b)
#     #     Gs.append(G)
#     # Gs.sort(key=probability_of_graph, reverse=True)
#     return A

# f_m = find_m_most_likely_graphs(V, E, W, m)
# # def find_candidate_cluster(V, E, W, m_hat, k1):
# #     Vgate, Egate, Wgate = CF(V, E, W)
# #     Gs = find_most_likely_graphs(Vgate, Egate, Wgate, m_hat)
# #     sensors = FBCS(Gs)[:k1]
# #     Delta_t = compute_Delta_t(sensors)
# #     likelihoods = [likelihood(v, Gs, Delta_t) for v in Vgate]
# #     v_hat = Vgate[np.argmax(likelihoods)]
# #     Ecluster = set(filter(lambda e: e[0] in [v_hat] + sensors and e[1] in [v_hat] + sensors, E))
# #     Vcluster = set([v_hat] + sensors)
# #     return Vcluster, Ecluster