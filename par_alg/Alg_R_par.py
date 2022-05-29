#Algorithm R: repeat {parent-root-connect; shortcut} until no v.p change
"""
вообще алгоритмы р и ра самые сложные для меня в плане реализации
и если с ра я как то выкрутился(вообще я постраюсь это исправить но вряд ли сейчас) ()
то тут настоящая проблема с // если вы это читаете то наверное я проблему решил
если я это не удалил то это будет мой поток мысли который в идеале поможет вам понять логику кода

проблема:
for each vertex v do
    v.o = v.p
убьет // так как вершины на 6 частей не поделить то // исчезает что не хорошо а так как циклы вложены отдельно это вынести нельзя
вариант решения номер 1:
    делить вершины на 6 частей и тд
    наверное самое рабочее на данный момент 
parent-root-connect:
for each vertex v do
    v.o = v.p
    for each edge {v, w} do
        if v.o > w.o and v.o = v.o.o then
            v.o.p = min{v.o.p, w.o}
        else if w.o = w.o.o then
            w.o.p = min{w.o.p, v.o}



так пока я думал я понял что расчитывать автоматическое деление на кол во ядер и нод достаточно сложно(попробую летом, если получится то будет здорово
(я делю кол во дуг и вершин и хочу чтоб на каждое ко-во вершин было кол-во дуг и этих групп было меньше или равно кол-ву ядер системы и если это будет запускаться на разных устройствах
то кол во будет меняться и следовательно размеры групп надо менять  ))

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


#да, он самый 
def euclid_alg(a,b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
        return a+b

#TODO красивое решение

"""
parent-root-connect:
for each vertex v do
    v.o = v.p
    for each edge {v, w} do
        if v.o > w.o and v.o = v.o.o then
            v.o.p = min{v.o.p, w.o}
        else if w.o = w.o.o then
            w.o.p = min{w.o.p, v.o}
"""
#!!!!!!!!!!!!!!!! вот тут вообще старнность но ладно
# они пишут что цикл в цикле но работает если циклы идут один за другим
#вообще как они думали реализовать \\ алгоритм где есть цикл в цикле но ладно
def parent_root_connect(Vertex_processed, Edges_raw):
    for i in range(len(Vertex_processed)):
        Vertex_processed[i]=Vertex( (Vertex_processed[i]).number,(Vertex_processed[i]).parent,(Vertex_processed[i]).parent)
    for j in Edges_raw:
        v=Vertex_processed[j[0]]
        w=Vertex_processed[j[1]]
        if(v.old_parent>w.old_parent and v.old_parent==(Vertex_processed[v.old_parent]).old_parent):
            a=(Vertex_processed[v.old_parent])
            (Vertex_processed[v.old_parent])=Vertex(a.number,min(a.parent,w.old_parent),a.old_parent)
        elif  w.old_parent==(Vertex_processed[w.old_parent]).old_parent:
            b=(Vertex_processed[w.old_parent])
            (Vertex_processed[w.old_parent])=Vertex(b.number,min(b.parent,v.old_parent),b.old_parent)

def Algorithm_R(Vertex_processed, Edges_raw):
    while True:
        vp_old = vp_collector(Vertex_processed)
        parent_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if (check_if_equal(vp_new, vp_old)):
            break
    #print(str(Edges_raw)+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return Vertex_processed

def processPart(Vertex_raw, Edges_raw):
    return Algorithm_R(Vertex_raw, Edges_raw)


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
        list1 = pool.starmap(Algorithm_R, grouplist)
        list4 = pool.map(parentCollect, list2)

    print(list4)
    print(list2)
    pool.close()
