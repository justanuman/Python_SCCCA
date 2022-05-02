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


def prot_naive_alg_v3(arc, sharedlist):
    v = findVertex(arc[0], sharedlist)
    w = findVertex(arc[1], sharedlist)
    v_addr = findVertex_analog(arc[0], sharedlist)
    w_addr = findVertex_analog(arc[1], sharedlist)
    if v.parent < w.parent:
        w.parent = v.parent
        sharedlist[w_addr] = w
        # print (v,w)


# всё очень плохо
def prot_naive_alg_v4(arc, sharedlist, sharedlist2):
    if type(arc) != Vertex:
        v = findVertex_v2(arc[0], sharedlist)
        w = findVertex_v2(arc[1], sharedlist)
        if v.parent < w.parent:
            w.parent = v.parent
        print(len(sharedlist2))
        sharedlist2.append(v)
        sharedlist2.append(w)
        # sharedlist2.append(arc)


def prot_naive_alg_v5(arc, sharedlist, sharedlist2):
    if type(arc) != Vertex:
        v = findVertex_v2(arc[0], sharedlist)
        w = findVertex_v2(arc[1], sharedlist)
        if v.parent < w.parent:
            w.parent = v.parent
        else:
            v.parent = w.parent
        write_confl_v = findVertex_v2(v.number, sharedlist2)
        write_confl_v_addr = findVertex_analog_v2(v.number, sharedlist2)
        write_confl_w = findVertex_v2(w.number, sharedlist2)
        write_confl_w_addr = findVertex_analog_v2(w.number, sharedlist2)
        if write_confl_v != None:
            if write_confl_v.number > v.number:
                sharedlist2[write_confl_v_addr] = v
        else:
            sharedlist2.append(v)
        if write_confl_w != None:
            if write_confl_w.number > w.number:
                sharedlist2[write_confl_w_addr] = w
        else:
            sharedlist2.append(w)


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


# вообще так и должно быть у них было write conflict resovled in favour of smaller value
def step_cleanup_v1():
    pass


# по их идее процессы идут глобальными шагами поэтому я хочу  сделать что то похожее


def step_forward_v1():
    pass


def test(x):
    print(x)


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    sharedlist = manager.list()
    sharedlist2 = manager.list()
    tasks = [(x, sharedlist) for x in Vertex_raw]
    task2 = [(x, sharedlist) for x in Edges_raw]
    pool.starmap(prot_init_v3, tasks)
    pool.close()
    pool2 = multiprocessing.Pool()
    pool2.starmap(prot_naive_alg_v6, task2)
    task2 = [(x, sharedlist) for x in Edges_raw]
    pool2.starmap(prot_naive_alg_v6, task2)
    task2 = [(x, sharedlist) for x in Edges_raw]
    pool2.starmap(prot_naive_alg_v6, task2)
    task2 = [(x, sharedlist) for x in Edges_raw]
    pool2.starmap(prot_naive_alg_v6, task2)
    task2 = [(x, sharedlist) for x in Edges_raw]
    pool2.starmap(prot_naive_alg_v6, task2)
    pool2.close()
    print(sharedlist)
    """pool=multiprocessing.Pool()
    
    pool3=multiprocessing.Pool()
    manager=multiprocessing.Manager()
    
    
    
    #print(sharedlist)
    
    pool3.starmap(prot_naive_alg_v3, task2)
    pool3.close()
    """
# наивный алгоритм (наверное)
