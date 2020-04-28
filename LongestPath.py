graph=dict()
nodelist=[]
with open("dataset.txt","r") as f:
    start=int(f.readline().split()[0])
    end=int(f.readline().split()[0])
    for line in f:
        temp=line.split(":")
        value=int(temp[1])
        temp=temp[0].split("->")
        graph[(int(temp[0]),int(temp[1]))]=value
        if int(temp[0]) not in nodelist:
            nodelist.append(int(temp[0]))
        if int(temp[1]) not in nodelist:
            nodelist.append(int(temp[1]))
    
pathlist=list(graph.keys())
nodelist.sort()

print("Node list is:",nodelist)


def LongestPath(graph,start,end):
    node_num=[]
    path=[]
    for node in nodelist:
        if node==start:
            node_num.append((start,0))
        else:
            print("Now investigate node:",node)
            possibilities=[]
            temp=[]
            for item in pathlist:
                if item[1]==node and item[0]<node:
                    print("There is a calculable path ending with",node,":",item)
                    temp.append(item)
                    for tuple in node_num:
                        if tuple[0]==item[0]:
                            possibility=tuple[1]+graph[item]
                            print("One possibility of answer is:",possibility)
                            possibilities.append(possibility)
               
                else:
                    for edge in pathlist:
                        if edge[0]==item:
                            pathlist.remove(edge)    
            if possibilities:        
                maxpossibility=max(possibilities)
                node_num.append((node,maxpossibility))
                print("Now max number of",node,"becomes:",maxpossibility)
                path.append((node,temp[possibilities.index(maxpossibility)][0]))
                print("Path becomes:",path)
    return (node_num,path)
       
def FindPath(path,start,nownode):
    if nownode==start:
        return [start]
    for tuple in path:
        if tuple[0]==nownode:
            return FindPath(path,start,tuple[1])+[nownode]
        

temp=LongestPath(graph,start,end)
node_num=temp[0]
for item in node_num:
    if item[0]==end:
        score=item[1]
print(score)
path=temp[1]
bestpath=FindPath(path,start,end)
print(bestpath)


with open("answer.txt","w") as f:
    f.write(str(score))
    f.write("\n")
    for i in range(len(bestpath)-1):
        f.write(str(bestpath[i]))
        f.write("->")
    f.write(str(bestpath[-1]))
