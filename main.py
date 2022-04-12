# для начала сделаю алгоритм  S чтоб хоть что то работало
#Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
"""
• Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes
• Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
• Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
"""
import networkx as nx
import numpy as np
import random 
from collections import Counter
from Algorithms import Alg_R as R
from Algorithms import Alg_RA as RA
from Algorithms import Alg_A as A
from Algorithms import Alg_S as S

'''
Vertex_raw=[0,1,2,3,4,5,6]
Vertex_processed=[]
Edges_raw=[[1,2],[1,3],[2,3],[0,4],[5,6],[3,4]]R.Algorithm_wrap(Vertex_raw, Edges_raw)
RA.Algorithm_wrap(Vertex_raw, Edges_raw)
A.Algorithm_wrap(Vertex_raw, Edges_raw)
S.Algorithm_wrap(Vertex_raw, Edges_raw)
list_1 = Algorithm_wrap(Vertex_raw, Edges_raw)
Algorithm_wrap(Vertex_raw, Edges_raw)
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (0, 4), (5, 6), (3, 4)])
list_2 = list(nx.connected_components(G))
assert numpy.array_equiv(list_1, list_2)
print(list_1)'''
raw_vert=[i for i in range(0,20)]
for_net=[]
raw_a=[]
raw_s=[]
raw_r=[]
raw_ra=[]
for i in range(20):
	c= random.randint(0,19)
	v=random.randint(0,19)
	if(c==v):
		while (c==v):
			c= random.randint(0,19)
			v=random.randint(0,19)
		a=[c,v]
		b= {c,v}
		raw_a.append(a)
		raw_s.append(a)
		raw_r.append(a)
		raw_ra.append(a)
		for_net.append(b)
	else:
		a=[c,v]
		b= {c,v}
		raw_a.append(a)
		raw_s.append(a)
		raw_r.append(a)
		raw_ra.append(a)
		for_net.append(b)

#print(for_net)
print("____")
G = nx.Graph()
G.add_edges_from(for_net)
print("networkx")
etalon=list(nx.connected_components(G))
def compare(s, t):
    first_set = set(map(tuple, s))
    secnd_set = set(map(tuple, t))
    return first_set==secnd_set
def cleanup(dirtyInp):
	cleanout=list()
	for i in dirtyInp:
		if len(i)!=1:
			temp=list(i)
			cleanout.append(temp)
	return cleanout
etalon=cleanup(etalon)
print(etalon)
print("alg_S")
clean_S=cleanup(S.Algorithm_wrap([i for i in range(0,20)], raw_s))
print(clean_S)
print("Alg_R")
clean_R=cleanup(R.Algorithm_wrap([i for i in range(0,20)], raw_r))
print(clean_R)
print("Alg_A")
clean_A=cleanup(A.Algorithm_wrap([i for i in range(0,20)], raw_a))
print(clean_A)
clean_RA=cleanup(RA.Algorithm_wrap([i for i in range(0,20)], raw_ra))
print("Alg_RA")
print(clean_RA)

assert compare(clean_A, etalon)
assert compare(clean_R, etalon)
assert compare(clean_S, etalon)
assert compare(clean_RA, etalon)