# • Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
from dataclasses import dataclass, field


@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0


def vp_collector(Vertex_processed):
    vp_collection = set()
    for i in range(len(Vertex_processed)):
        vp_collection.add((Vertex_processed[i]).parent)
    return vp_collection


def Initialize(Vertex_raw):
    Vertex_processed = []
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))
    return Vertex_processed


"""
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
        if j[0] > j[1] and j[0] == (Vertex_processed[j[0]]).old_parent:
            (Vertex_processed[j[0]]).parent = min((Vertex_processed[j[0]]).parent, j[1])
        elif j[1] == (Vertex_processed[j[1]]).old_parent:
            (Vertex_processed[j[1]]).parent = min((Vertex_processed[j[1]]).parent, j[0])


def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for k in Vertex_processed:
        k.parent = (Vertex_processed[k.old_parent]).old_parent


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


def AlgorithmRA(Vertex_raw, Edges_raw):
    Vertex_processed = Initialize(Vertex_raw)
    while True:
        vp_old = vp_collector(Vertex_processed)
        direct_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if vp_old == vp_new:
            break
    return Vertex_processed


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
