from dataclasses import dataclass, field
import networkx as nx
import numpy
import collections
# для начала сделаю алгоритм  S чтоб хоть что то работало
# Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
"""
• Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes
• Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
• Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
"""


@dataclass
class Vertex:
    """для хранение вершин тк им нужна свзяь"""

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
# инициализация которая обрабатывает введеные данные(raw->processed)
# вообще тут проблема которая не факт что сразу решу но надо как то обойтись без поинтеров
# но не факт возможно отдельный список вершин не нужен
# так я подумал и по сути номер вершины это считай ссылка на неё так что в принцие можно будет обойтись
def vp_collector(Vertex_processed):
    vp_collection = list()
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return vp_collection


def Initialize(Vertex_raw, Vertex_processed):
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i, i))


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


def direct_connect(Vertex_processed, Edges_raw):
    for i in range(len(Edges_raw)):
        if (Vertex_processed[Edges_raw[i][0]]).number > (
            Vertex_processed[Edges_raw[i][1]]
        ).number:
            (Vertex_processed[Edges_raw[i][0]]).parent = min(
                (Vertex_processed[Edges_raw[i][0]]).parent, Edges_raw[i][1]
            )
        else:
            (Vertex_processed[Edges_raw[i][1]]).parent = min(
                (Vertex_processed[Edges_raw[i][1]]).parent,
                (Vertex_processed[Edges_raw[i][0]]).number,
            )


def Algorithm_A(Vertex_raw, Edges_raw):
    Vertex_processed = []
    Initialize(Vertex_raw, Vertex_processed)
    while len(Edges_raw) != 0:
        vp_old = vp_collector(Vertex_processed)
        direct_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if check_if_equal(vp_new,vp_old):
            break
    return Vertex_processed


# Algorithm_A(Vertex_raw, Edges_raw)


def Algorithm_wrap(Vertex_raw, Edges_raw):
    list_of_components = []
    Vertex_processed = Algorithm_A(Vertex_raw, Edges_raw)
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
    return list_of_components
