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


def direct_connect(Vertex_processed, Edges_raw):
    for i in range(len(Edges_raw)):
        if (Vertex_processed[Edges_raw[i][0]]).number > (Vertex_processed[Edges_raw[i][1]]).number:
            v=(Vertex_processed[Edges_raw[i][0]])
            v.parent = min((Vertex_processed[Edges_raw[i][0]]).parent, Edges_raw[i][1])
            if((Vertex_processed[Edges_raw[i][0]]).parent> v.parent ):
                (Vertex_processed[Edges_raw[i][0]])=v
        else:
            w= (Vertex_processed[Edges_raw[i][1]])
            w.parent = min((Vertex_processed[Edges_raw[i][1]]).parent,(Vertex_processed[Edges_raw[i][0]]).number)
            if((Vertex_processed[Edges_raw[i][1]]).parent> w.parent ):
                (Vertex_processed[Edges_raw[i][1]])=w


def Algorithm_A(Vertex_processed, Edges_raw):
    while True:
        vp_old = vp_collector(Vertex_processed)
        direct_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if (check_if_equal(vp_new, vp_old)):
            break
    #print(str(Edges_raw)+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return Vertex_processed


def processPart(Vertex_raw, Edges_raw):
    return Algorithm_A(Vertex_raw, Edges_raw)


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
        list1 = pool.starmap(Algorithm_A, grouplist)
        list4 = pool.map(parentCollect, list2)
    print(list4)
    print(list2)
    pool.close()
"""
    pool = multiprocessing.Pool(processes=6)
    Vertex_raw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    Edges_raw = [
        [18, 16],
        [13, 16],
        [17, 5],
        [6, 13],
        [11, 10],
        [4, 6],
        [9, 10],
        [0, 6],
        [7, 12],
        [13, 11],
        [7, 10],
        [3, 11],
        [14, 0],
        [13, 7],
        [15, 1],
        [6, 9],
        [0, 18],
        [3, 2],
        [15, 11],
        [3, 2],
    ]
    manager = multiprocessing.Manager()
    Vertex_processed = pool.map(parInit, Vertex_raw)
    splitEdges = list(chunks(Edges_raw, 6))
    grouplist = grouping(Vertex_processed, splitEdges)
    list1 = pool.starmap(processPart, grouplist)
    list2 = manager.list()
    list2 = pool.starmap(compareProccess, zipper(list1))
    list3 = pool.map(parentCollect, list2)
    list4 = []
    while list3 != list4:
        list3 = pool.map(parentCollect, list2)
        grouplist = grouping(list2, splitEdges)
        list1 = pool.starmap(processPart, grouplist)
        #list2 = pool.starmap(compareProccess, zipper(list1))
        list4 = pool.map(parentCollect, list2)
    print(list4)
    print(list2)
    pool.close()
"""
