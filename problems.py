from dataclasses import dataclass, field
# для начала сделаю алгоритм  S чтоб хоть что то работало
#Algorithm S: repeat {parent-connect; repeat shortcut until no v.p changes} until no v.p changes
"""
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
def parent_connect(Vertex_processed, Edges_raw):
	change =0
	while (True):
		for i in range(len(Vertex_processed)):
			(Vertex_processed[i]).old_parent=(Vertex_processed[i]).parent
		for j in range(len(Edges_raw)):
			if(Vertex_processed[Edges_raw[j][0]]).old_parent>(Vertex_processed[(Edges_raw[j][1])]).old_parent:
				if((Vertex_processed[(Vertex_processed[Edges_raw[j][0]]).old_parent]).parent !=min((Vertex_processed[(Vertex_processed[Edges_raw[j][0]]).old_parent]).parent, (Vertex_processed[Edges_raw[j][1]]).old_parent)):
					(Vertex_processed[(Vertex_processed[Edges_raw[j][0]]).old_parent]).parent = min((Vertex_processed[(Vertex_processed[Edges_raw[j][0]]).old_parent]).parent, (Vertex_processed[Edges_raw[j][1]]).old_parent)
					change+=1
			else:
				if((Vertex_processed[(Vertex_processed[Edges_raw[j][1]]).old_parent]).parent != min((Vertex_processed[(Vertex_processed[Edges_raw[j][1]]).old_parent]).parent,(Vertex_processed[Edges_raw[j][0]]).old_parent)):
					(Vertex_processed[(Vertex_processed[Edges_raw[j][1]]).old_parent]).parent = min((Vertex_processed[(Vertex_processed[Edges_raw[j][1]]).old_parent]).parent,(Vertex_processed[Edges_raw[j][0]]).old_parent)
					change+=1
		if(change==0):
			break
		else:
			change=0
		shortcut(Vertex_processed, Edges_raw)
def shortcut(Vertex_processed, Edges_raw):
	while (True):
		vp_check=0
		for i in  range(len(Vertex_processed)):
			(Vertex_processed[i]).old_parent=(Vertex_processed[i]).parent
		for k in range(len(Vertex_processed)):
			x= (Vertex_processed[k]).old_parent
			if type(x)== 'int' and (Vertex_processed[k]).parent!=(Vertex_processed[x]).old_parent:
				(Vertex_processed[k]).parent=(Vertex_processed[x]).old_parent
				vp_check+=1
		if(vp_check==0):
			break

#print(Vertex_processed)

def Algorithm_S(Vertex_raw, Edges_raw):
	Vertex_processed=[]
	Initialize(Vertex_raw, Vertex_processed)
	parent_connect(Vertex_processed, Edges_raw)
	print(Vertex_processed)

Algorithm_S(Vertex_raw,Edges_raw)