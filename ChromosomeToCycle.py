def ChromosomeToCycle(p):
    nodes=[]
    for item in p:
        temp=abs(item)*2
        if item>0:
            nodes.append(temp-1)
            nodes.append(temp)
        else:
            nodes.append(temp)
            nodes.append(temp-1)
    return nodes
   

with open("dataset_8222_4.txt","r") as f:
    content=f.read()
content1=content.replace("(","")
content2=content1.replace(")","")
print(content2)
p=list(map(int,content2.split()))
answer=ChromosomeToCycle(p)

with open("answer.txt","w") as f:
    f.write("(")
    for i in range(len(answer)-1):
        f.write(str(answer[i]))
        f.write(" ")
    f.write(str(answer[-1]))
    f.write(")")

