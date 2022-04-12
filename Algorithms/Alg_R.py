# Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
from dataclasses import dataclass, field

import collections
@dataclass
class Vertex:

    number: int = 0
    parent: int = 0
    old_parent: int = 0

    def ret():
        return old_parent

def check_if_equal(list_1, list_2):
    """ Check if both the lists are of same length and then get the frequency
    of each element in list using collections.Counter. Then Compare if both the Counter
    objects are equal or not to confirm if lists contain similar elements with same frequency"""
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)

def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return vp_collection

def vpo_collector(Vertex_processed):
    vp_collection = set()
    for i in range(len(Vertex_processed)):
        vp_collection.add((Vertex_processed[i]).old_parent)
    return vp_collection

def Initialize(Vertex_raw, Vertex_processed):
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))


def parent_root_connect(Vertex_processed, Edges_raw):
    for i in range(len(Vertex_processed)):
        (Vertex_processed[i]).old_parent = (Vertex_processed[i]).parent
    for j in range(len(Edges_raw)):
        if (Vertex_processed[Edges_raw[j][0]]).old_parent > (
            Vertex_processed[Edges_raw[j][1]]
        ).old_parent and (Vertex_processed[Edges_raw[j][0]]).old_parent == (
            Vertex_processed[((Vertex_processed[Edges_raw[j][0]]).old_parent)]
        ).old_parent:
            (
                Vertex_processed[((Vertex_processed[Edges_raw[j][0]]).old_parent)]
            ).parent = min(
                (
                    Vertex_processed[((Vertex_processed[Edges_raw[j][0]]).old_parent)]
                ).parent,
                (Vertex_processed[Edges_raw[j][1]]).old_parent,
            )
        elif (Vertex_processed[Edges_raw[j][1]]).old_parent == (
            Vertex_processed[((Vertex_processed[Edges_raw[j][1]]).old_parent)]
        ).old_parent:
            (
                Vertex_processed[((Vertex_processed[Edges_raw[j][1]]).old_parent)]
            ).parent = min(
                (
                    Vertex_processed[((Vertex_processed[Edges_raw[j][1]]).old_parent)]
                ).parent,
                (Vertex_processed[Edges_raw[j][0]]).old_parent,
            )


def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent=i.parent
    for k in Vertex_processed:
        k.parent=(Vertex_processed[k.old_parent]).old_parent


def AlgorithmR(Vertex_raw, Edges_raw):
    Vertex_processed = []
    t = 0
    Initialize(Vertex_raw, Vertex_processed)
    while True:
        vp_old = vp_collector(Vertex_processed)
        vpo_old = vpo_collector(Vertex_processed)
        parent_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        vpo_new = vpo_collector(Vertex_processed)
        if(check_if_equal(vp_new,vp_old)):
            break
    #print(Vertex_processed)
    return Vertex_processed


def Algorithm_wrap(Vertex_raw, Edges_raw):
    list_of_components = []
    Vertex_processed = AlgorithmR(Vertex_raw, Edges_raw)
    for i in Vertex_processed:
        number= i.number
        parent= i.parent
        add = False
        for j in list_of_components:
            if parent in j:
                add=True
                j.add(number)
            if number in j:
                j.add(parent)
                add=True
        if(add==False):
            a= set()
            a.add(number)
            a.add(parent)
            list_of_components.append(a)
    return list_of_components