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
    

with open("dataset_8224_2.txt","r") as f:
    temp=f.read().split("\n")
colorededges=[]
for item in temp[0].split("), ("):
    if "(" in item:
        colorededges.append(list(map(int,item.replace("(","").split(", "))))
    elif ")" in item:
       colorededges.append(list(map(int,item.replace(")","").split(", "))))
    else:
        colorededges.append(list(map(int,item.split(", "))))
breakinfo=list(map(int,temp[1].split(", ")))
answer=BreakOnGenomeGraph(colorededges,breakinfo)
print(answer)

with open("answer.txt","w") as f:
    f.write("(")
    for i in range(len(answer)-1):
        f.write(str(answer[i][0]))
        f.write(", ")
        f.write(str(answer[i][1]))
        f.write("), (")
    f.write(str(answer[-1][0]))
    f.write(", ")
    f.write(str(answer[-1][1]))
    f.write(")")



