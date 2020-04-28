import numpy as np

def ScorePair(aa1,aa2):
    if aa1==aa2:
        return 1
    else:
        return -2

def ScoreMatrix(peptide1,peptide2,d):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    backtrack=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    scorematrix=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    for i in range(lengthpeptide1+1):
        scorematrix[i][0]=0
        backtrack[i][0]=0
    for j in range(lengthpeptide2+1):
        scorematrix[0][j]=0
        backtrack[0][j]=0
    for i in range(1,lengthpeptide1+1):
        for j in range(1,lengthpeptide2+1):
            possibility1=scorematrix[i-1][j-1]+ScorePair(peptide1[i-1],peptide2[j-1])
            possibility2=scorematrix[i-1][j]-d
            possibility3=scorematrix[i][j-1]-d
            score=max(possibility1,possibility2,possibility3)
            scorematrix[i][j]=score
            if score==possibility1:
                backtrack[i][j]=1
            elif score==possibility2:
                backtrack[i][j]=3
            else:
                backtrack[i][j]=2
    return (scorematrix,backtrack)

def TraceBack(peptide1,peptide2,scorematrix,backtrack):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    alignedpeptide1=[]
    alignedpeptide2=[]
    finalscore=np.max(scorematrix[lengthpeptide1:])
    for j in range(lengthpeptide2+1):
        if scorematrix[lengthpeptide1][j]==finalscore:
            break
    i=lengthpeptide1
    while j:
        if backtrack[i][j]==1:
            alignedpeptide1=[peptide1[i-1]]+alignedpeptide1
            alignedpeptide2=[peptide2[j-1]]+alignedpeptide2
            i-=1
            j-=1
        elif backtrack[i][j]==2:
            alignedpeptide1=["-"]+alignedpeptide1
            alignedpeptide2=[peptide2[j-1]]+alignedpeptide2
            j-=1
        else:
            alignedpeptide1=[peptide1[i-1]]+alignedpeptide1
            alignedpeptide2=["-"]+alignedpeptide2
            i-=1
    return(str(int(finalscore)),''.join(alignedpeptide1),''.join(alignedpeptide2))


with open("dataset_248_7.txt","r") as f:
    content=f.read().split()
peptide1=content[0]
peptide2=content[1]
print("Peptide1 is:",peptide1)
print("Peptide2 is",peptide2)
d=2
tup=ScoreMatrix(peptide1,peptide2,2)
scorematrix=tup[0]
backtrack=tup[1]
print(scorematrix)
print(backtrack)
result=TraceBack(peptide1,peptide2,scorematrix,backtrack)
print(result[0])
print(result[1])
print(result[2])

with open("answer.txt","w") as f:
    for item in result:
        f.write(item)
        f.write("\n")

