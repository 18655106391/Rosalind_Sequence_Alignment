def ColoredEdges(genome):
    colorededges=[]
    for chromosome in genome:
        lengthchromosome=len(chromosome)
        for i in range(lengthchromosome):
            next=chromosome[(i+1)%lengthchromosome]
            if chromosome[i]>0:
                if next>0:
                    colorededges.append([2*chromosome[i],2*next-1])
                else:
                    colorededges.append([2*chromosome[i],-2*next])
            else:
                if next>0:
                    colorededges.append([-2*chromosome[i]-1,2*next-1])
                else:
                    colorededges.append([-2*chromosome[i]-1,-2*next])
    return colorededges

def BreakOnGenomeGraph(genome,breakinfo):
    i1,i2,i3,i4=breakinfo
    if [i1,i2] in genome:
        genome.remove([i1,i2])
    else:
        genome.remove([i2,i1])
    if [i3,i4] in genome:
        genome.remove([i3,i4])
    else:
        genome.remove([i4,i3])
    genome.append([i1,i3])
    genome.append([i2,i4])
    return genome

def GetEdge(edgeeasy,node):
    index=edgeeasy.index(node)
    if index%2:
        return[edgeeasy[index-1],node]
    else:
        return[node,edgeeasy[index+1]]

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
        

def BreakSorting(genomelist):
    genome1=genomelist[0]
    genome2=genomelist[1]
    rededges=ColoredEdges(genome1)
    #print("Original red edges are",rededges)
    sortprocess=[genome1]
    blueedges=ColoredEdges(genome2)[::-1]
    #print("Original blue edges are",blueedges)
    while blueedges:
        blueedge=blueedges[0]
        rededgeseasy=Join(rededges)
        if blueedge[0] in rededgeseasy and blueedge[1] in rededgeseasy:
            rededge1=GetEdge(rededgeseasy,blueedge[0])
            rededge2=GetEdge(rededgeseasy,blueedge[1])
            #print("We deal with the rededges",rededge1,rededge2,"on the sides of",blueedge)
            if set(rededge1)==set(rededge2):
                blueedges.remove(blueedge)
            else:
                breakinfo=(blueedge[0],rededge1[1-rededge1.index(blueedge[0])],blueedge[1],rededge2[1-rededge2.index(blueedge[1])])
                #print("Rededges",rededges,"break at",breakinfo,"and becomes")
                rededges=BreakOnGenomeGraph(rededges,breakinfo)
                #print(rededges)
                sortprocess.append(ColoredEdgeToGenome(rededges))
                blueedges.remove(blueedge)
    return sortprocess
                
with open("dataset_288_5.txt","r") as f:
    temp=f.read().split("\n")
if "" in temp:
    temp.remove("")
genomelist=[]
for genome in temp:
    chromosome=[]
    chromosomeinstring=genome.replace(")","").split("(")
    chromosomeinstring.remove("")
    for item in chromosomeinstring:
        chromosome.append(list(map(int,item.split(" "))))
    genomelist.append(chromosome)
sortprocess=BreakSorting(genomelist)

with open("answer.txt","w") as f:
    for genome in sortprocess:
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
        f.write("\n")
    
