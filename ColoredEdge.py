with open("data.txt","r") as f:
    temp=f.read().split(")(")
content=[]
content.append(list(map(int,temp[0].replace("(","").split())))
for i in range(1,len(content)-1):
    content.append(list(map(int,temp[i].split())))
content.append(list(map(int,temp[-1].replace(")","").split())))

def ColoredEdges(genome):
    colorededges=[]
    for chromosome in genome:
        lengthchromosome=len(chromosome)
        for i in range(lengthchromosome):
            next=chromosome[(i+1)%lengthchromosome]
            if chromosome[i]>0:
                if next>0:
                    colorededges.append((2*chromosome[i],2*next-1))
                else:
                    colorededges.append((2*chromosome[i],-2*next))
            else:
                if next>0:
                    colorededges.append((-2*chromosome[i]-1,2*next-1))
                else:
                    colorededges.append((-2*chromosome[i]-1,-2*next))
    return colorededges

answer=ColoredEdges(content)
print(answer)

with open("answer.txt","w") as f:
    for i in range(len(answer)-1):
        item=answer[i]
        f.write("(")
        f.write(str(item[0]))
        f.write(",")
        f.write(str(item[1]))
        f.write("), ")
    f.write("(")
    f.write(str(answer[-1][0]))
    f.write(",")
    f.write(str(answer[-1][1]))
    f.write(") ")
