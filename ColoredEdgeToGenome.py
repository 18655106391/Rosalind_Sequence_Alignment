def Join(listoflist):
    new=[]
    for item in listoflist:
        new+=item
    return new

def Replace(alist,elementreplaced,newelement):
    index=alist.index(elementreplaced)
    alist.remove(elementreplaced)
    alist.insert(index,newelement)
    return alist

def Remain(listtotal,listsub):
    remainedlist=[]
    for item in listtotal:
        if item not in listsub:
            remainedlist.append(item)
    return remainedlist

def SortColoredEdges(colorededges):
    colorededges.sort(key=lambda x: x[0])
    colorededgeseasy=Join(colorededges)
    sortededges=[colorededges[0]]
    i=1
    cyclesign=0
    while i<len(colorededges):
        if cyclesign==0:
            lastedge=sortededges[-1]
        else:
            lastedge=Remain(colorededges,sortededges)[0]
            sortededges.append(lastedge)
        if lastedge[1]%2:
            index=colorededgeseasy.index(lastedge[1]+1)//2
            edge=colorededges[index]
        else:
            index=colorededgeseasy.index(lastedge[1]-1)//2
            edge=colorededges[index]
        if edge not in sortededges:
            cyclesign=0
            if abs(edge[0]-lastedge[1])!=1:
                sortededges.append(edge[::-1])
                colorededges=Replace(colorededges,edge,edge[::-1])
                colorededgeeasy=Join(colorededges)
            else:
                sortededges.append(edge)
        else:
            cyclesign=1
            if i==len(colorededges)-1:
                sortededges.append(Remain(colorededges,sortededges)[0])
                
        i+=1
    return sortededges
            
def ColoredEdgeToGenome(colorededges):
    genome=[]
    chromosome=[]
    colorededges=SortColoredEdges(colorededges)
    #print("Sorted colorededges are",colorededges)
    for i in range(len(colorededges)):
        item=colorededges[i]
        lastitem=colorededges[i-1]
        if item[0]%2:
            temp=-(item[0]+1)//2
        else:
            temp=item[0]//2
        if lastitem[1]%2:
            lasttemp=(lastitem[1]+1)//2
        else:
            lasttemp=-lastitem[1]//2
        #print("temp is %s last temp is %s"%(temp,lasttemp))
        if temp==lasttemp:
            if i!=len(colorededges)-1:
                chromosome.append(temp)
            else:
                chromosome.append(temp)
                genome.append(chromosome)    
        else:
            if i!=len(colorededges)-1:
                genome.append(chromosome)
                chromosome=[temp]
            else:
                genome.append(chromosome)
                chromosome=[temp]
                genome.append(chromosome)
    if [] in genome:
        genome.remove([])
    return genome
        

with open("dataset_8222_8.txt","r") as f:
    temp=f.read()
templist=temp.split("), (")
colorededges=[]
for item in templist:
    if "(" in item:
        colorededges.append(list(map(int,item.replace("(","").split(", "))))
    elif ")" in item:
        colorededges.append(list(map(int,item.replace(")","").split(", "))))
    else:
        colorededges.append(list(map(int,item.split(", "))))
genome=ColoredEdgeToGenome(colorededges)
print(genome)

with open("answer.txt","w") as f:
    for chromosome in genome:
        f.write("(")
        for i in range(len(chromosome)-1):
            fragment=chromosome[i]
            if fragment>0:
                f.write("+"+str(fragment)+" ")
            else:
                f.write(str(fragment)+" ")
        fragment=chromosome[-1]
        if fragment>0:
            f.write("+"+str(fragment)+")")
        else:
            f.write(str(fragment)+")")
    
