from dataclasses import dataclass, field
import collections
from multiprocessing import shared_memory
import multiprocessing
import numpy as np


@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0


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


def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in Vertex_processed:
        vp_collection.append(i.number)
        vp_collection.append(i.parent)
        vp_collection.append((Vertex_processed[i.old_parent]).old_parent)
    return vp_collection


def parInit(a):
    return Vertex(a, a)

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


def Algorithm_S(Vertex_processed, Edges_raw):
    while True:
        vp_old = vp_collector(Vertex_processed)
        parent_connect_simple(Vertex_processed, Edges_raw)
        while True:
            vp_old_ct = vp_collector(Vertex_processed)
            shortcut(Vertex_processed, Edges_raw)
            vp_new_ct = vp_collector(Vertex_processed)
            if check_if_equal(vp_new_ct, vp_old_ct):
                break
        vp_new = vp_collector(Vertex_processed)
        if check_if_equal(vp_new, vp_old):
            break
    return Vertex_processed


def processPart(Vertex_raw, Edges_raw):
    return Algorithm_S(Vertex_raw, Edges_raw)


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
        list1 = pool.starmap(Algorithm_S, grouplist)
        list4 = pool.map(parentCollect, list2)
    print(list4)
    print(list2)
    pool.close()