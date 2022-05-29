"""
// || это параллельность

так 
цитирую оригинальную статью

In direct-root-connect (as in parent-connect) we need to save the old parents to get a correct sequential
implementation, so that the root test is correct even if the parent has been changed by processing another
edge during the same iteration of the loop over the edges. If we truly have global concurrency, simpler
pseudocode suffices, as for parent-connect.

таким образом я могу всунуть простой псевдокод 
обычный не подходит тк придется циклом проходиться по массиву вершин что уберет весь смысл в //
"""
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


# Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes


def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in Vertex_processed:
        vp_collection.append(i.number)
        vp_collection.append(i.parent)
        vp_collection.append((Vertex_processed[i.old_parent]).old_parent)
    return vp_collection


def Initialize(Vertex_raw):
    Vertex_processed = []
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))
    return Vertex_processed


def parInit(a):
    return Vertex(a, a)


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

"""
for i in Vertex_processed:
        i.old_parent = i.parent
    for k in Vertex_processed:
        k.parent = (Vertex_processed[k.old_parent]).old_parent
"""
def shortcut(Vertex_processed, Edges_raw):
    for i in range(len(Vertex_processed)):
        b=Vertex_processed[i]
        Vertex_processed[i]=Vertex(b.number,b.parent,b.parent)
    for j in range(len(Vertex_processed)):
        b=Vertex_processed[j]
        bp=(Vertex_processed[b.old_parent]).old_parent
        Vertex_processed[j]=Vertex(b.number,bp,b.old_parent)


def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)
"""
def parent_root_connect_simple(Vertex_processed, Edges_raw):
parent-root-connect-simple
for each edge {v, w} do
    if v.p > v.p and v.p = v.p.p then 
        v.p.p = min(v.p.p, w.p)
    else if w.p = w.p.p then
        w.p.p = min{w.p.p, v.o}


!!!! как вариант менять только те вершины что упоминаются в дугах таким образом НАВЕРНОЕ будет всё лучше
"""
def parent_connect_simple(Vertex_processed, Edges_raw):
    for j in Edges_raw:
        v=Vertex_processed[j[0]]
        w=Vertex_processed[j[1]]
        vp=(Vertex_processed[v.parent])
        wp=(Vertex_processed[w.parent])
        if(v.parent>w.parent):
            vp.parent=min(vp.parent, w.parent)
            if((Vertex_processed[v.parent]).parent>vp.parent):
                (Vertex_processed[v.parent])=vp
        else:
            wp.parent=min(wp.parent, v.parent)
            if((Vertex_processed[w.parent]).parent>wp.parent):
                (Vertex_processed[w.parent])=wp

   
def Algorithm_RA(Vertex_processed, Edges_raw):
    while True:
        vp_old = vp_collector(Vertex_processed)
        parent_connect_simple(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed,Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if (check_if_equal(vp_new, vp_old)):
            break
    #print(str(Edges_raw)+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return Vertex_processed


def processPart(Vertex_raw, Edges_raw):
    return Algorithm_RA(Vertex_raw, Edges_raw)


def parentCollect(a):
    return a.parent


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def grouping(vert, edge):
    arglist = []
    for i in edge:
        arglist.append((vert, i))
    return arglist


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=6)
    Vertex_raw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    Edges_raw = [[18, 16],[13, 16],[17, 5],[6, 13],[11, 10],[4, 6],[9, 10],[0, 6],[7, 12],[13, 11],[7, 10],[3, 11],[14, 0],[13, 7],[15, 1],[6, 9],[0, 18],[3, 2],[15, 11],[3, 2],]
    manager = multiprocessing.Manager()
    Vertex_processed = pool.map(parInit, Vertex_raw)
    splitEdges = list(chunks(Edges_raw, 6))
    grouplist = grouping(Vertex_processed, splitEdges)
    list1 = pool.starmap(processPart, grouplist)
    list2 = manager.list(Vertex_processed)
    list3 = pool.map(parentCollect, list2)
    list4 = []
    while list3 != list4:
        list3 = pool.map(parentCollect, list2)
        grouplist = grouping(list2, splitEdges)
        list1 = pool.starmap(Algorithm_RA, grouplist)
        list4 = pool.map(parentCollect, list2)
    print(list4)
    print(list2)
    pool.close()
