from dataclasses import dataclass, field
import collections

@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0


def Initialize(Vertex_raw):
    Vertex_processed = []
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))
    return Vertex_processed

"""for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o then
v.o.p = min{v.o.p, w.o}
else w.o.p = min{w.o.p, v.o}"""
def parent_connect(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for j in Edges_raw:
        vo = (Vertex_processed[j[0]]).old_parent
        wo = (Vertex_processed[j[1]]).old_parent
        if vo > wo:
            (Vertex_processed[vo]).parent = min((Vertex_processed[vo]).parent, wo)
        else:
            (Vertex_processed[wo]).parent = min((Vertex_processed[wo]).parent, vo)


def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return vp_collection




def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent = i.parent
    for k in Vertex_processed:
        k.parent = (Vertex_processed[k.old_parent]).old_parent

def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)

def inside_wrap(Vertex_processed):
    list_of_components=[]
    output_list=[]
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
# Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
def Algorithm_S(Vertex_raw, Edges_raw):
    Vertex_processed = Initialize(Vertex_raw)
    while True:
        vp_old = vp_collector(Vertex_processed)
        parent_connect(Vertex_processed, Edges_raw)
        while True:
            vp_old_ct = vp_collector(Vertex_processed)
            shortcut(Vertex_processed, Edges_raw)
            vp_new_ct = vp_collector(Vertex_processed)
            if check_if_equal(vp_new_ct, vp_old_ct):
                break
        vp_new = vp_collector(Vertex_processed)
        if check_if_equal(vp_new, vp_old):
            break
    return inside_wrap(Vertex_processed)


def Algorithm_wrap(Vertex_raw, Edges_raw):
    list_of_components = []
    Vertex_processed = Algorithm_S(Vertex_raw, Edges_raw)
    for i in Vertex_processed:
        number = i.number
        parent = i.parent
        old_parent = i.old_parent
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
