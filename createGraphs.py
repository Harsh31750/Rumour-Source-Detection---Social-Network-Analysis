# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:46:06 2023

@author: barbh
"""

import random
import networkx as nx

def createInstance():
	for j in range(1, 5):
		fileHandle = open(path+"/instance"+str(j)+".txt","w")
        G = nx.karate_club_graph()
        
		with open('DiffusionModel/InfectedGraph.txt') as file:
			array = file.readlines()
			actualSource = array[0]
			fileHandle.write(actualSource)
			for i in range(1,len(array)):
				src, dst = array[i].split(" ")
				dst = dst.strip('\n')	
				wt = str("{0:.2f}".format(random.random()))
				if(wt == '0.00'):
					wt = '0.02'
				fileHandle.write(str(src) + " " + str(dst) + " " + wt + "\n")
		fileHandle.close()