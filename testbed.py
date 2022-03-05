from dataclasses import dataclass, field
# для начала сделаю алгоритм  S чтоб хоть что то работало
#Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
"""
• Algorithm A: repeat {direct-connect; shortcut; alter} until no v.p changes
• Algorithm R: repeat {parent-root-connect; shortcut} until no v.p changes
• Algorithm RA: repeat {direct-root-connect; shortcut; alter} until no v.p changes
parent-connect:
for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o then
v.o.p = min{v.o.p, w.o}
else w.o.p = min{w.o.p, v.o}

shortcut:
for each vertex v do
v.o = v.p
for each vertex v do
v.p = v.o.o

parent-root-connect:
for each vertex v do
v.o = v.p
for each edge {v, w} do
if v.o > w.o and v.o = v.o.o then
v.o.p = min{v.o.p, w.o}
else if w.o = w.o.o then
w.o.p = min{w.o.p, v.o}

alter:
for each edge {v, w} do
if v.p = w.p then
delete {v, w}
else replace {v, w} by {v.p, w.p}
"""
@dataclass
class Vertex():
    """для хранение вершин тк им нужна свзяь"""
    number: int = 0
    parent: int = 0
    old_parent: int=0
    def ret():
    	return old_parent
Vertex_raw=[0,1,2,3,4,5,6]

Vertex_processed=[]

Edges_raw=[[1,2],[1,3],[2,3],[0,4],[5,6],[3,4]]

Edges_processed=Edges_raw
#инициализация которая обрабатывает введеные данные(raw->processed)
#вообще тут проблема которая не факт что сразу решу но надо как то обойтись без поинтеров
# но не факт возможно отдельный список вершин не нужен
# так я подумал и по сути номер вершины это считай ссылка на неё так что в принцие можно будет обойтись 
def Initialize(Vertex_raw, Vertex_processed):
	for i in range(len(Vertex_raw)):
		Vertex_processed.append(Vertex(i, i, i))
Initialize(Vertex_raw, Vertex_processed)
#print(Vertex_processed, "|",Edges_processed) проверка на правильность обработки
#main loop for alg S
#change и vp_check перменные для проверки сизменения v.p другого решения этой проблемы я не вижу так что будет так
"""
for each edge {v, w} do
if v > w then
v.p = min{v.p, w}
else w.p = min{w.p, v}
"""
def shortcut_no_while(Vertex_processed, Edges_raw):
	for i in  range(len(Vertex_processed)):
		(Vertex_processed[i]).old_parent=(Vertex_processed[i]).parent
	for k in range(len(Vertex_processed)):
		x= (Vertex_processed[k]).old_parent
		if type(x)== 'int' and (Vertex_processed[k]).parent!=(Vertex_processed[x]).old_parent:
			(Vertex_processed[k]).parent=(Vertex_processed[x]).old_parent
def alter(Vertex_processed, Edges_raw):
	i=0#тут если фор использовать будет выход за пределы так что так
	while(i<len(Edges_raw)):
		if  (Vertex_processed[Edges_raw[i][0]]).parent==(Vertex_processed[Edges_raw[i][1]]).parent:
			del Edges_raw[i]
		else:
			Edges_raw[i][0]=(Vertex_processed[Edges_raw[i][0]]).parent
			Edges_raw[i][1]=(Vertex_processed[Edges_raw[i][1]]).parent
		i+=1
def direct_connect(Vertex_processed, Edges_raw):
	vp_check=0
	while (True):
		for i in range(len(Edges_raw)):
			if((Vertex_processed[Edges_raw[i][0]]).number > (Vertex_processed[Edges_raw[i][1]]).number):
				if((Vertex_processed[Edges_raw[i][0]]).parent != min((Vertex_processed[Edges_raw[i][0]]).parent,(Vertex_processed[Edges_raw[i][1]]).number)):
					(Vertex_processed[Edges_raw[i][0]]).parent = min((Vertex_processed[Edges_raw[i][0]]).parent,(Vertex_processed[Edges_raw[i][1]]).number)
					vp_check+=1
			else:
				if((Vertex_processed[Edges_raw[i][1]]).parent != min((Vertex_processed[Edges_raw[i][1]]).parent,(Vertex_processed[Edges_raw[i][0]]).number)):
					(Vertex_processed[Edges_raw[i][1]]).parent = min((Vertex_processed[Edges_raw[i][1]]).parent,(Vertex_processed[Edges_raw[i][0]]).number)
					vp_check+=1
		shortcut_no_while(Vertex_processed, Edges_raw)
		alter(Vertex_processed, Edges_raw)
		if vp_check==0:
			break
		else:
			vp_check=0
def Algorithm_A(Vertex_raw, Edges_raw):
	Vertex_processed=[]
	Initialize(Vertex_raw, Vertex_processed) 
	direct_connect(Vertex_processed, Edges_raw)
	print(Vertex_processed)
Algorithm_A(Vertex_raw, Edges_raw)