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
      

def ScoreMatrix(peptide1,peptide2,d):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    backtrack=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    scorematrix=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    for i in range(lengthpeptide1+1):
        scorematrix[i][0]=-i*d
        backtrack[i][0]=0
    for j in range(lengthpeptide2+1):
        scorematrix[0][j]=-j*d
        backtrack[0][j]=0
    for i in range(1,lengthpeptide1+1):
        for j in range(1,lengthpeptide2+1):
            possibility1=scorematrix[i-1][j-1]+scoredict[(peptide1[i-1],peptide2[j-1])]
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

def TraceBack(peptide1,peptide2,backtrack):
    i=len(peptide1)
    j=len(peptide2)
    alignedpeptide1=[]
    alignedpeptide2=[]
    while i or j:
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
    alignedpeptide1=''.join(alignedpeptide1)
    alignedpeptide2=''.join(alignedpeptide2)
    return(alignedpeptide1,alignedpeptide2)


with open("data.txt","r") as f:
    content=f.read().split()
peptide1=content[0]
peptide2=content[1]
d=5
tup=ScoreMatrix(peptide1,peptide2,5)
scorematrix=tup[0]
bestscore=int(scorematrix[len(peptide1)][len(peptide2)])
backtrack=tup[1]
peptides=TraceBack(peptide1,peptide2,backtrack)
print(bestscore)
print(peptides[0])
print(peptides[1])

with open("answer.txt","w") as f:
    f.write(str(bestscore))
    f.write('\n')
    f.write(peptides[0])
    f.write('\n')
    f.write(peptides[1])














