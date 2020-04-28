import numpy as np

scorelist=[]
with open("BLOSUM62.txt","r") as f:
    aalist=f.readline().split()
    for line in f:
        scorelist.append(list(map(int,line.split()[1:]))) 
substitutionmatrix=np.array(scorelist)
scoredict=dict()
for i in range(len(aalist)):
    for j in range(i,len(aalist)):
        scoredict[(aalist[i],aalist[j])]=substitutionmatrix[i][j]
        scoredict[(aalist[j],aalist[i])]=substitutionmatrix[i][j]
      
def EndColumnScore(peptide1,peptide2,gappenalty):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    scorematrix=np.zeros(shape=(lengthpeptide1+1,2))
    backpointer=[0]*(lengthpeptide1+1)
    for i in range(lengthpeptide1+1):
        scorematrix[i][0]=-i*gappenalty  
    column=1
    backpointer[0]=2
    while column<=lengthpeptide2:
        for i in range(0,lengthpeptide1+1):
            if i:
                possibility1=scorematrix[i-1][0]+scoredict[(peptide1[i-1],peptide2[column-1])]
                possibility2=scorematrix[i][0]-gappenalty
                possibility3=scorematrix[i-1][1]-gappenalty
                scorematrix[i][1]=max(possibility1,possibility2,possibility3)
                if scorematrix[i][1]==possibility1:
                    backpointer[i]=1
                elif scorematrix[i][1]==possibility2:
                    backpointer[i]=2
                else:
                    backpointer[i]=3
            else:
                scorematrix[i][1]=scorematrix[i][0]-gappenalty
                backpointer[i]=2
        scorematrix[:,0]=scorematrix[:,1]
        column+=1
    return (scorematrix[:,1],backpointer)


def MiddleEdge(peptide1,peptide2,gappenalty):
    middle=len(peptide2)//2
    #print("Middle is",middle)
    firsthalf=EndColumnScore(peptide1,peptide2[:middle],gappenalty)
    #print("First half:",peptide1,peptide2[:middle])
    firsthalfscore=firsthalf[0]
    firsthalftrace=firsthalf[1]
    secondhalf=EndColumnScore(peptide1[::-1],peptide2[len(peptide2)-1:middle-1:-1],gappenalty)
    #print("Second half:",peptide1[::-1],peptide2[len(peptide2)-1:middle-1:-1],gappenalty)
    secondhalfscore=secondhalf[0]
    secondhalftrace=secondhalf[1]
    secondhalfscore=secondhalfscore[::-1]
    secondhalftrace=secondhalftrace[::-1]
    #print(firsthalfscore,"\n",secondhalfscore)
    #print(firsthalftrace,"\n",secondhalftrace)
    finalscore=[]
    for i in range(len(secondhalfscore)):
        finalscore.append(firsthalfscore[i]+secondhalfscore[i])
    #print("finalscore list is:",finalscore)
    rowmiddlenode=finalscore.index(max(finalscore))
    startmidedge=(rowmiddlenode,middle)
    if secondhalftrace[rowmiddlenode]==1:
        endmidedge=(rowmiddlenode+1,middle+1)
    elif secondhalftrace[rowmiddlenode]==2:
        endmidedge=(rowmiddlenode,middle+1)
    else:
        endmidedge=(rowmiddlenode+1,middle)
    return(startmidedge,endmidedge)    

with open("dataset_250_12.txt","r") as f:
    content=f.read().split()
peptide1=content[0]
peptide2=content[1]
gappenalty=5
print(peptide1,"\n",peptide2,len(peptide2))
midedge=MiddleEdge(peptide1,peptide2,gappenalty)
print(midedge)

