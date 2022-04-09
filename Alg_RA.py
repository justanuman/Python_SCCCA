# R {parent-root-connect; shortcut} until no v.p changes
from dataclasses import dataclass, field


@dataclass
class Vertex:
    """для хранение вершин тк им нужна свзяь"""

    number: int = 0
    parent: int = 0
    old_parent: int = 0

    def ret():
        return old_parent


Vertex_raw = [0, 1, 2, 3, 4, 5, 6]

Vertex_processed = []

Edges_raw = [[1, 2], [1, 3], [2, 3], [0, 4], [5, 6], [3, 4]]

Edges_processed = Edges_raw


def vp_collector(Vertex_processed):
    vp_collection = []
    for i in range(len(Vertex_processed)):
        vp_collection.append((Vertex_processed[i]).parent)
    return vp_collection


def Initialize(Vertex_raw, Vertex_processed):
    for i in range(len(Vertex_raw)):
        Vertex_processed.append(Vertex(i, i, i))


def direct_root_connect(Vertex_processed, Edges_raw):
    for i in range(len(Vertex_processed)):
        (Vertex_processed[i]).old_parent = (Vertex_processed[i]).parent
        for j in range(len(Edges_raw)):
            if (
                Edges_raw[j][0] > Edges_raw[j][1]
                and Edges_raw[j][0] == (Vertex_processed[Edges_raw[j][0]]).old_parent
            ):
                (Vertex_processed[Edges_raw[j][0]]).parent = min(
                    (Vertex_processed[Edges_raw[j][0]]).parent, Edges_raw[j][1]
                )
            elif Edges_raw[j][1] == (Vertex_processed[Edges_raw[j][1]]).old_parent:
                (Vertex_processed[Edges_raw[j][1]]).parent = min(
                    (Vertex_processed[Edges_raw[j][1]]).parent, Edges_raw[j][0]
                )


def shortcut(Vertex_processed, Edges_raw):
    for i in range(len(Vertex_processed)):
        (Vertex_processed[i]).old_parent = (Vertex_processed[i]).parent
    for k in range(len(Vertex_processed)):
        x = (Vertex_processed[k]).old_parent
        if (
            type(x) == "int"
            and (Vertex_processed[k]).parent != (Vertex_processed[x]).old_parent
        ):
            (Vertex_processed[k]).parent = (Vertex_processed[x]).old_parent


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
    Vertex_processed = []
    t = 0
    Initialize(Vertex_raw, Vertex_processed)
    while len(Edges_raw) != 0:
        vp_old = vp_collector(Vertex_processed)
        direct_root_connect(Vertex_processed, Edges_raw)
        shortcut(Vertex_processed, Edges_raw)
        alter(Vertex_processed, Edges_raw)
        vp_new = vp_collector(Vertex_processed)
        if vp_old == vp_new:
            t += 1
        if t == 2:
            break
    return Vertex_processed


# Algorithm_A(Vertex_raw, Edges_raw)


def Algorithm_wrap(Vertex_raw, Edges_raw):
    list_of_components = []
    Vertex_processed = AlgorithmRA(Vertex_raw, Edges_raw)
    for i in Vertex_processed:
        vert_parent = i.parent
        vert = i.number
        add = False
        for j in range(len(list_of_components)):
            if vert_parent in (list_of_components[j]):
                (list_of_components[j]).add(vert)
                add = True
        if add == False:
            a = set()
            a.add(vert)
            list_of_components.append(a)
    return list_of_components


