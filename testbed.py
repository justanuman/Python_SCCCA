from dataclasses import dataclass, field
import networkx as nx
import numpy
import collections
from joblib import Parallel, delayed
import math
import time

# from multiprocessing import Pool
import multiprocessing

Vertex_raw = [0, 1, 2, 3, 4, 5, 6]
Edges_raw = [[1, 2], [1, 3], [2, 3], [4, 3], [5, 6], [0, 4]]


@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0


# попытка обойти ограничение на 1 параметр
# костыли но у меня идеи заканчиваются
"""
for each v do v.p = v;
repeat
for each arc (v, w) do if v.p < w.p then w.p ¬ v.p
until no parent changes
"""



"""for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o then
v.o.p = min{v.o.p, w.o}
else w.o.p = min{w.o.p, v.o}"""
# Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes

"""
for each vertex v do
    v.o = v.p
for each vertex v do
    v.p = v.o.o


for each edge {v, w} do
if v.p > w.p then
v.p.p = min{v.p.p, w.p}
else w.p.p = min{w.p.p, v.p}

for j in Edges_raw:
        vp = (Vertex_processed[j[0]]).parent
        wp = (Vertex_processed[j[1]]).parent
        if(vp>wp):
             (Vertex_processed[vp]).parent = min((Vertex_processed[vp]).parent, wp)
        else:
             (Vertex_processed[wp]).parent = min((Vertex_processed[wp]).parent, vp)

write_confl_v = findVertex_v2(v.number, sharedlist)
    write_confl_w = findVertex_v2(w.number, sharedlist)
    write_confl_v_addr = findVertex_analog(v.number, sharedlist)
    write_confl_w_addr = findVertex_analog(w.number, sharedlist)

"""
def vp_collector(v,sharedlist,sharedlist2):
    pass

def shortcut(v,sharedlist):
    v.old_parent=v.parent
    #print(v.old_parent,v.parent)
    v.parent= (findVertex_v2(v.old_parent, sharedlist)).old_parent
    sharedlist[findVertex_analog(v.number,sharedlist)]=v

def parent_connect_simple(arc, sharedlist):
    vp = (findVertex_v2(arc[0], sharedlist)).parent
    wp = (findVertex_v2(arc[1], sharedlist)).parent
    vpp= (findVertex_v2(vp, sharedlist))
    wpp=(findVertex_v2(wp, sharedlist))
    if(vp>wp):
        vpp.parent= min(vpp.parent, wp)
        addr=findVertex_analog(vpp.number,sharedlist)
        if( (sharedlist[addr]).parent> vpp.parent):
            sharedlist[addr]= vpp
    else:
        wpp.parent= min(wpp.parent, vp)
        #print(wpp,vp)
        addr=findVertex_analog(wpp.number,sharedlist)
        if( (sharedlist[addr]).parent> wpp.parent):
            sharedlist[addr]= wpp

def findVertex(vert, Vertexes):
    for i in Vertexes:
        if i.number == vert:
            return i


def findVertex_v2(vert, Vertexes):
    for i in Vertexes:
        if type(i) == Vertex:
            if i.number == vert:
                return i
    return None


def findVertex_analog(vert, Vertexes):
    for i in range(len(Vertexes)):
        if (Vertexes[i]).number == vert:
            return i


def findVertex_analog_v2(vert, Vertexes):
    for i in range(len(Vertexes)):
        if type(i) == Vertex:
            if (Vertexes[i]).number == vert:
                return i
    return None


def prot_init_v3(element, sharedlist):
    sharedlist.append(Vertex(element, element))


def prot_naive_alg_v6(arc, sharedlist):
    v = findVertex_v2(arc[0], sharedlist)
    w = findVertex_v2(arc[1], sharedlist)
    write_confl_v = findVertex_v2(v.number, sharedlist)
    write_confl_w = findVertex_v2(w.number, sharedlist)
    write_confl_v_addr = findVertex_analog(v.number, sharedlist)
    write_confl_w_addr = findVertex_analog(w.number, sharedlist)
    if v.parent < w.parent:
        w.parent = v.parent
    if write_confl_v.parent > v.parent:
        sharedlist[write_confl_v_addr] = v
    if write_confl_w.parent > w.parent:
        sharedlist[write_confl_w_addr] = w


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    sharedlist = manager.list()
    sharedlist2 = manager.list()
    tasks = [(x, sharedlist) for x in Vertex_raw]
    task2 = [(x, sharedlist) for x in Edges_raw]
    taskvert=[(x,sharedlist) for x in sharedlist]
    pool.starmap(prot_init_v3, tasks)
    pool.close()
    pool2 = multiprocessing.Pool()
    for i in range(5):
        pool2.starmap(parent_connect_simple, task2)
        taskvert=[(x,sharedlist) for x in sharedlist]
        pool2.starmap(shortcut, taskvert)
        pool2.starmap(shortcut, taskvert)
        pool2.starmap(parent_connect_simple, task2)
        pool2.starmap(shortcut, taskvert)
        pool2.starmap(shortcut, taskvert)
        pool2.starmap(shortcut, taskvert)
    pool2.close()
    print(sharedlist)
# наивный алгоритм (наверное)
