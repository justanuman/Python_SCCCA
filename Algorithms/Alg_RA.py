# • Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
from dataclasses import dataclass, field
import collections


@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0


def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)


def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return vp_collection


"""
initialize:
    for each vertex v do v.p = v
"""


def Initialize(Vertex_raw):
    Vertex_processed = []
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))
    return Vertex_processed


"""
direct-root-connect:
    for each vertex v do
        v.o = v.p
    for each edge {v, w} do
        if v > w and v = v.o then
            v.p = min{v.p, w}
        else if w = w.o then
            w.p = min{w.p, v}
"""


def direct_root_connect(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for j in Edges_raw:
        v = (Vertex_processed[j[0]]).number
        w = (Vertex_processed[j[1]]).number
        if ((v > w)) and (v == (Vertex_processed[j[0]]).old_parent):
            (Vertex_processed[j[0]]).parent = min((Vertex_processed[j[0]]).parent, w)
        elif w == (Vertex_processed[j[1]]).old_parent:
            (Vertex_processed[j[1]]).parent = min((Vertex_processed[j[1]]).parent, v)


"""
for each vertex v do
    v.o = v.p
for each vertex v do
    v.p = v.o.o
"""


def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for k in Vertex_processed:
        k.parent = (Vertex_processed[k.old_parent]).old_parent


"""
for each edge {v, w} do
    if v.p = w.p then
        delete {v, w}
    else replace {v, w} by {v.p, w.p}
"""


def alter(Vertex_processed, Edges_raw):
    i = 0
    while i < len(Edges_raw):
        if (Vertex_processed[Edges_raw[i][0]]).parent == (
            Vertex_processed[Edges_raw[i][1]]
        ).parent:
            del Edges_raw[i]
        else:
            Edges_raw[i][0] = (Vertex_processed[Edges_raw[i][0]]).parent
            Edges_raw[i][1] = (Vertex_processed[Edges_raw[i][1]]).parent
        i += 1


def inside_wrap(Vertex_processed):
    list_of_components = []
    output_list = []
    for i in Vertex_processed:
        number = i.number
        parent = i.parent
        add = False
        for i in list_of_components:
            if parent in i:
                add = True
                i.add(number)
            if number in i:
                i.add(parent)
                add = True
        if add == False:
            a = set()
            a.add(number)
            a.add(parent)
            list_of_components.append(a)
    for i in list_of_components:
        output_list.append(list(i))
    return list(output_list)


# • Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes


def AlgorithmRA(Vertex_raw, Edges_raw):
    Vertex_processed = Initialize(Vertex_raw)
    while True:
        vp_old = vp_collector(Vertex_processed)
        direct_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        # print(Vertex_processed)
        if check_if_equal(vp_new, vp_old) and len(Edges_raw) == 0:
            break
        direct_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
    return inside_wrap(Vertex_processed)


def Algorithm_wrap(Vertex_raw, Edges_raw):
    list_of_components = []
    Vertex_processed = AlgorithmRA(Vertex_raw, Edges_raw)
    for i in Vertex_processed:
        number = i.number
        parent = i.parent
        add = False
        for j in list_of_components:
            if parent in j:
                j.add(number)
                add = True
            if number in j:
                j.add(parent)
                add = True
        if add == False:
            a = set()
            a.add(number)
            a.add(parent)
            list_of_components.append(a)
    return list_of_components
