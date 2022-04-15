# для начала сделаю алгоритм  S чтоб хоть что то работало
# Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
"""
• Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes
• Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
• Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
"""
import networkx as nx
import numpy as np
import random
from collections import Counter
from Algorithms import Alg_R as R
from Algorithms import Alg_RA as RA
from Algorithms import Alg_A as A
from Algorithms import Alg_S as S

"""
Vertex_raw=[0,1,2,3,4,5,6]
Vertex_processed=[]
Edges_raw=[[1,2],[1,3],[2,3],[0,4],[5,6],[3,4]]R.Algorithm_wrap(Vertex_raw, Edges_raw)
RA.Algorithm_wrap(Vertex_raw, Edges_raw)
A.Algorithm_wrap(Vertex_raw, Edges_raw)
S.Algorithm_wrap(Vertex_raw, Edges_raw)
list_1 = Algorithm_wrap(Vertex_raw, Edges_raw)
Algorithm_wrap(Vertex_raw, Edges_raw)
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (0, 4), (5, 6), (3, 4)])
list_2 = list(nx.connected_components(G))
assert numpy.array_equiv(list_1, list_2)
print(list_1)"""


# сравнение к  сожалению не идеальное я постараюсь придумать получше
# так что периодически он ломается если внутри компонентов разный порядок
#
def compare(s, t):
    first_set = set(map(tuple, s))
    secnd_set = set(map(tuple, t))
    return first_set == secnd_set


def findpart(s, t):
    found = False
    for i in t:
        if set(s) == set(i):
            found = True
    return found


def compare_adv(s, t):
    if len(s) != len(t):
        return False
    equal = True
    for j in s:
        if not findpart(j, t):
            equal = False
    return equal


def cleanup(dirtyInp):
    cleanout = list()
    for i in dirtyInp:
        if len(i) != 1:
            temp = list(i)
            cleanout.append(temp)
    return cleanout


# ассерты это конечно здорово на как два массива вывести один над другим я не придумал так что будут условия
# да и вообще не очень удобно
# и вообще у меня небольшие сомнения насчет логарифмов(ну кончено это я всё не так сделал но всё равно)
# direct root connect самый странный конечно
# в процессе тестирования был найден очень интересный момент, который к сожалению говорит о том что я не до конца понимаю что написал
# что то каким то образом ломает ввод в алгоритм, тк сам по себе РА работает без ошибок но вместе с другими он валится
# я попытаюсь разбить тестирование на 4 скрипта чтобы избежать абсолютно непонятную ошибку
def automatic_testing_RA():
    G = nx.Graph()
    raw_vert = [i for i in range(0, 20)]
    for i in range(20):
        for_net = []
        raw_ra = []
        for i in range(20):
            c = random.randint(0, 19)
            v = random.randint(0, 19)
            if c == v:
                while c == v:
                    c = random.randint(0, 19)
                    v = random.randint(0, 19)
                a = [c, v]
                b = {c, v}
                raw_ra.append(a)
                for_net.append(b)
            else:
                a = [c, v]
                b = {c, v}
                raw_ra.append(a)
                for_net.append(b)
        G.add_edges_from(for_net)
        etalon = list(nx.connected_components(G))
        etalon = cleanup(etalon)
        clean_RA = cleanup(RA.AlgorithmRA([ra for ra in range(0, 20)], raw_ra))
        if not compare_adv(clean_RA, etalon):
            print("input")
            print(((str(for_net)).replace("{", "[")).replace("}", "]"))
            print("mistake alg RA")
            print(etalon)
            print(clean_RA)
            print("_______")
        G.clear()


def automatic_testing_A():
    G_A = nx.Graph()
    raw_vert = [i for i in range(0, 20)]
    for i in range(20):
        for_net = []
        raw_a = []
        for i in range(20):
            c = random.randint(0, 19)
            v = random.randint(0, 19)
            if c == v:
                while c == v:
                    c = random.randint(0, 19)
                    v = random.randint(0, 19)
                a = [c, v]
                b = {c, v}
                raw_a.append(a)
                for_net.append(b)
            else:
                a = [c, v]
                b = {c, v}
                raw_a.append(a)
                for_net.append(b)
        G_A.add_edges_from(for_net)
        etalon = list(nx.connected_components(G_A))
        etalon = cleanup(etalon)
        clean_A = cleanup(A.Algorithm_A([a for a in range(0, 20)], raw_a))
        if not compare_adv(clean_A, etalon):
            print("input")
            print(((str(for_net)).replace("{", "[")).replace("}", "]"))
            print("mistake alg A")
            print(etalon)
            print(clean_A)
            print("_______")
        G_A.clear()


def automatic_testing_S():
    G = nx.Graph()
    raw_vert = [i for i in range(0, 20)]
    for i in range(20):
        for_net = []
        raw_s = []
        for i in range(20):
            c = random.randint(0, 19)
            v = random.randint(0, 19)
            if c == v:
                while c == v:
                    c = random.randint(0, 19)
                    v = random.randint(0, 19)
                a = [c, v]
                b = {c, v}
                raw_s.append(a)
                for_net.append(b)
            else:
                a = [c, v]
                b = {c, v}
                raw_s.append(a)
                for_net.append(b)
        G.add_edges_from(for_net)
        etalon = list(nx.connected_components(G))
        etalon = cleanup(etalon)
        clean_S = cleanup(S.Algorithm_S([s for s in range(0, 20)], raw_s))
        if not compare_adv(clean_S, etalon):
            print("input")
            print(((str(for_net)).replace("{", "[")).replace("}", "]"))
            print("mistake alg S")
            print(etalon)
            print(clean_S)
            print("_______")
        G.clear()


def automatic_testing_R():
    G = nx.Graph()
    raw_vert = [i for i in range(0, 20)]
    for i in range(20):
        for_net = []
        raw_r = []
        for i in range(20):
            c = random.randint(0, 19)
            v = random.randint(0, 19)
            if c == v:
                while c == v:
                    c = random.randint(0, 19)
                    v = random.randint(0, 19)
                a = [c, v]
                b = {c, v}
                raw_r.append(a)
                for_net.append(b)
            else:
                a = [c, v]
                b = {c, v}
                raw_r.append(a)
                for_net.append(b)
        G.add_edges_from(for_net)
        etalon = list(nx.connected_components(G))
        etalon = cleanup(etalon)
        clean_R = cleanup(R.AlgorithmR([r for r in range(0, 20)], raw_r))
        if not (compare_adv(clean_R, etalon)):
            print("input")
            print(((str(for_net)).replace("{", "[")).replace("}", "]"))
            print("mistake alg R")
            print(etalon)
            print(clean_R)
            # иногда сравнение ломается если порядок различается
            # разберусь чуть позже
            print("_______")
        G.clear()


automatic_testing_A()
automatic_testing_S()
automatic_testing_RA()
automatic_testing_R()
"""
самое удивительное было в условии выхода алгоритмы были так то правильные но они не доходили до конца и пожтому валились на тестировании
поэтому вы можете увидеть там ещё доп условие 
без него не работает 
raw=[[18, 16], [13, 16], [17, 5], [6, 13], [11, 10], [4, 6], [9, 10], [0, 6], [7, 12], [13, 11], [7, 10], [3, 11], [14, 0], [13, 7], [15, 1], [6, 9], [0, 18], [3, 2], [15, 11], [3, 2]]

print(cleanup(RA.AlgorithmRA([i for i in range(0,20)], raw)))"""
