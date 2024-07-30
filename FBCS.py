# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:22:17 2023

@author: barbh
"""

import heapq
import networkx as nx


def FBCS(Gs):
    # Initialize the list of sensor nodes to an empty dictionary
    BCS = {}
    # For each graph Gj in the list of graphs Gs
    for Gj in Gs:
        if not isinstance(Gj, nx.Graph):  # check if Gj is a graph object
            raise ValueError("Input is not a graph object.")
        # Compute the betweenness centrality values for all nodes in the graph Gj
        BC_Gj = nx.betweenness_centrality(Gj, weight='weight')
        # Sort the list of betweenness centrality values for nodes in the graph Gj using a heap sort algorithm
        
        # For each node v in the graph Gj, compute the priority value and add it to the current value of BCS(v)
        for v in Gj.nodes():
            if v not in BCS:
                BCS[v] = 0
            BCS[v] += (1.0 / len(Gs)) * BC_Gj[v]
    # Return the final list of sensor nodes
    return sorted(BCS.keys(), key=BCS.get, reverse=True)

def pickSensors(BCS, k):
    return BCS[:k]

# # Create an example graph
# G = nx.karate_club_graph()
# Gs = [G]

# # Test the function
# print(FBCS(Gs))