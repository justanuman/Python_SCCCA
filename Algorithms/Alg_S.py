from dataclasses import dataclass, field
import collections

@dataclass
class Vertex:
    number: int = 0
    parent: int = 0
    old_parent: int = 0

def Initialize(Vertex_raw):
    Vertex_processed=[]
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i))
    return Vertex_processed

def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return collections.Counter(list_1) == collections.Counter(list_2)

def parent_connect(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
       i.old_parent = i.parent
    for j in Edges_raw:
        vo=(Vertex_processed[j[0]]).old_parent
        wo=(Vertex_processed[j[1]]).old_parent
        vop=Vertex_processed[vo]
        wop=Vertex_processed[wo]
        if(vo>wo):
            vop.parent=min(vop.parent, wo)
        else:
            wop.parent=min(wop.parent, vo)

def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return  vp_collection

def vpo_collector(Vertex_processed):
    vp_collection = set()
    for i in range(len(Vertex_processed)):
        vp_collection.add((Vertex_processed[i]).old_parent)
    return vp_collection

def shortcut(Vertex_processed, Edges_raw):
    for i in Vertex_processed:
        i.old_parent=i.parent
    for k in Vertex_processed:
        k.parent=(Vertex_processed[k.old_parent]).old_parent

def Algorithm_S(Vertex_raw, Edges_raw):
    Vertex_processed = Initialize(Vertex_raw)
    while True:
        vp_old = vp_collector(Vertex_processed)
        parent_connect(Vertex_processed, Edges_raw)
        while True:
             vp_old_shct = vp_collector(Vertex_processed)
             shortcut(Vertex_processed, Edges_raw)
             vp_new_shct= vp_collector(Vertex_processed)
             if check_if_equal(vp_old_shct,vp_new_shct):
                break
        vp_new = vp_collector(Vertex_processed)
        if(check_if_equal(vp_old,vp_new)):
            break
    return Vertex_processed

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
                add=True
            if number in j:
                j.add(parent)
                add=True
        if(add==False):
            a= set()
            a.add(number)
            a.add(parent)
            list_of_components.append(a)
    return list_of_components