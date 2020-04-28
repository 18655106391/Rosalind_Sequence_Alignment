import numpy as np

def ScorePair(aa1,aa2):
    if aa1==aa2:
        return 1
    else:
        return -1

def ScoreMatrix(peptide1,peptide2):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    scorematrix=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    backtrack=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    for i in range(lengthpeptide1+1):
        scorematrix[i][0]=-i
        backtrack[i][0]=0
    for j in range(lengthpeptide2+1):
        scorematrix[0][j]=0
        backtrack[0][j]=0
    for i in range(1,lengthpeptide1+1):
        for j in range(1,lengthpeptide2+1):
            possibility1=scorematrix[i-1][j-1]+ScorePair(peptide1[i-1],peptide2[j-1])
            possibility2=scorematrix[i-1][j]-1
            possibility3=scorematrix[i][j-1]-1
            maxpossibility=max(possibility1,possibility2,possibility3)
            scorematrix[i][j]=maxpossibility
            if maxpossibility==possibility1:
                backtrack[i][j]=1
            elif maxpossibility==possibility2:
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
            alignedpeptide1=[]
            alignedpeptide2=[]
            nowcolumn=j
            nowrow=lengthpeptide1
            while nowrow:
                if backtrack[nowrow][nowcolumn]==1:
                    alignedpeptide1.insert(0,peptide1[nowrow-1])
                    alignedpeptide2.insert(0,peptide2[nowcolumn-1])  
                    nowrow-=1
                    nowcolumn-=1
                elif backtrack[nowrow][nowcolumn]==2:
                    alignedpeptide1.insert(0,"-")
                    alignedpeptide2.insert(0,peptide2[nowcolumn-1])
                    nowcolumn-=1
                else:
                    alignedpeptide1.insert(0,peptide1[nowrow-1])
                    alignedpeptide2.insert(0,"-")
                    nowrow-=1
            break
    return (str(int(finalscore)),"".join(alignedpeptide2),"".join(alignedpeptide1))

with open("dataset_248_5.txt","r") as f:
    content=f.read().split()
peptide2=content[0]
peptide1=content[1]
tup=ScoreMatrix(peptide1,peptide2)
scorematrix=tup[0]
backtrack=tup[1]
print(scorematrix)
print(backtrack)
alignment=TraceBack(peptide1,peptide2,scorematrix,backtrack)
for item in alignment:
    print(item)


with open("answer.txt","w") as f:
    for item in alignment:    
        f.write(item)
        f.write("\n")















