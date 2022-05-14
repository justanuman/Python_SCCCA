from dataclasses import dataclass, field
import networkx as nx
import numpy
import collections
from joblib import Parallel, delayed
import math
import time
from multiprocessing import shared_memory
import multiprocessing
import numpy as np
import sys
@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0

#Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes

def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in Vertex_processed:
        vp_collection.append(i.number)
        vp_collection.append(i.parent)
        vp_collection.append((Vertex_processed[i.old_parent]).old_parent)
    return vp_collection


def Initialize(Vertex_raw):
	Vertex_processed=[]
	for i in range(len(Vertex_raw)):
		Vertex_processed.append(Vertex(i, i))
	return Vertex_processed
def alter(Vertex_processed, Edges_raw):
    i = 0  # тут если фор использовать будет выход за пределы так что так
    while i < len(Edges_raw):
        if (Vertex_processed[Edges_raw[i][0]]).parent == (
            Vertex_processed[Edges_raw[i][1]]
        ).parent:
            del Edges_raw[i]
        else:
            Edges_raw[i][0] = (Vertex_processed[Edges_raw[i][0]]).parent
            Edges_raw[i][1] = (Vertex_processed[Edges_raw[i][1]]).parent
        i += 1


def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for k in Vertex_processed:
        k.parent = (Vertex_processed[k.old_parent]).old_parent

def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)


def direct_connect(Vertex_processed, Edges_raw):
    for i in range(len(Edges_raw)):
        if (Vertex_processed[Edges_raw[i][0]]).number > (
            Vertex_processed[Edges_raw[i][1]]
        ).number:
            (Vertex_processed[Edges_raw[i][0]]).parent = min(
                (Vertex_processed[Edges_raw[i][0]]).parent, Edges_raw[i][1]
            )
        else:
            (Vertex_processed[Edges_raw[i][1]]).parent = min(
                (Vertex_processed[Edges_raw[i][1]]).parent,
                (Vertex_processed[Edges_raw[i][0]]).number,
            )

def Algorithm_A(Vertex_processed, Edges_raw):
	while True:
		vp_old = vp_collector(Vertex_processed)
		direct_connect(Vertex_processed, Edges_raw)
		shortcut(Vertex_processed, Edges_raw)
		alter(Vertex_processed, Edges_raw)
		vp_new = vp_collector(Vertex_processed)
		if (check_if_equal(vp_new, vp_old)) and len(Edges_raw) == 0:
		    break
	
	#print(str(Edges_raw)+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	return Vertex_processed

def processPart(Vertex_raw,Edges_raw):
	return Algorithm_A(Vertex_raw, Edges_raw)

def compareProccess(a,b):
	if(a.parent>b.parent):
		return b
	else:
		return a
def parentCollect(a):
	return a.parent
if __name__ == "__main__":
	Vertex_raw=[0,1,2,3,4,5,6]
	Vertex_processed=[]
	Edges_raw=[[1,2],[1,3],[2,3],[0,4],[5,6],[3,4]]
	pool = multiprocessing.Pool()
	vert= Initialize(Vertex_raw)
	a1=(vert, Edges_raw[:3])
	a2=(vert, Edges_raw[3:])
	list1 = (pool.starmap(processPart, [a1,a2]))
	list2=(pool.starmap(compareProccess, zip(list1[0],list1[1])))
	list3=pool.map(parentCollect, list2)
	print(list3)
	list4=[]
	while (list3!=list4):
		list3=pool.map(parentCollect, list2)
		a1=(list2, Edges_raw[:3])
		a2=(list2, Edges_raw[3:])
		list1 = (pool.starmap(processPart, [a1,a2]))
		list2=(pool.starmap(compareProccess, zip(list1[0],list1[1])))
		list4=pool.map(parentCollect, list2)
		print(list3)
	print(list2)
	pool.close()