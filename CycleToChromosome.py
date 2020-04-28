def CycleToChromosome(p):
    chromosome=[]
    for i in range(1,max(p)//2+1):
        if p[2*(i-1)]<p[2*i-1]:
            chromosome.append(i)
        else:
            chromosome.append(-i)
    return chromosome        
   

with open("dataset_8222_5.txt","r") as f:
    content=f.read()
content1=content.replace("(","")
content2=content1.replace(")","")
print(content2)
p=list(map(int,content2.split()))
answer=CycleToChromosome(p)

with open("answer.txt","w") as f:
    f.write("(")
    for i in range(len(answer)-1):
        if answer[i]>0:
            f.write("+"+str(answer[i]))
        else:
            f.write(str(answer[i]))
        f.write(" ")
    if answer[-1]>0:
        f.write("+"+str(answer[-1]))
    else:
        f.write(str(answer[-1]))
    f.write(")")
