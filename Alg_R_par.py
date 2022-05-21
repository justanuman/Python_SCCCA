#• Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
"""
parent-connect:
for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o then
v.o.p = min{v.o.p, w.o}
else w.o.p = min{w.o.p, v.o}


parent-root-connect:
for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o and v.o = v.o.o then
v.o.p = min{v.o.p, w.o}
else if w.o = w.o.o then
w.o.p = min{w.o.p, v.o}

так 
цитирую оригинальную статью

In direct-root-connect (as in parent-connect) we need to save the old parents to get a correct sequential
implementation, so that the root test is correct even if the parent has been changed by processing another
edge during the same iteration of the loop over the edges. If we truly have global concurrency, simpler
pseudocode suffices, as for parent-connect.

таким образом я могу всунуть простой псевдокод 
обычный не подходит тк придется циклом проходиться по массиву вершин что уберет весь смысл в // 


поэтому я изменю то что они написали на simpler
pseudocode

parent-root-connect:
for each vertex v do
	v.o = v.p
for each edge {v, w} do
	if v.o > w.o and v.o = v.o.o then
		v.o.p = min{v.o.p, w.o}
	else if w.o = w.o.o then
		w.o.p = min{w.o.p, v.o}

parent-root-connect-simple
for each edge {v, w} do
	if v.p > v.p and v.p = v.p.p then 
		v.p.p = min(v.p.p, w.p)
	else if w.p = w.p.p then
		w.p.p = min{w.p.p, v.o}

тестирование (см файлы в папке алгоритмы Alg_R) показало что данный псевдокод проходит тестирование из файла мейн
является ли это совпадением неизвестно но пока я просто функции подставлял заметил что там вообще много что можно подставить чтоб правильно работать



"""
