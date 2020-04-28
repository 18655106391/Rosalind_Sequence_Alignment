import numpy as np

def ScorePair(aa1,aa2):
    if aa1==aa2:
        return 0
    else:
        return 1

def ScoreMatrix(peptide1,peptide2):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    scorematrix=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    for i in range(lengthpeptide1+1):
        scorematrix[i][0]=i
    for j in range(lengthpeptide2+1):
        scorematrix[0][j]=j
    for i in range(1,lengthpeptide1+1):
        for j in range(1,lengthpeptide2+1):
            possibility1=scorematrix[i-1][j-1]+ScorePair(peptide1[i-1],peptide2[j-1])
            possibility2=scorematrix[i-1][j]+1
            possibility3=scorematrix[i][j-1]+1
            scorematrix[i][j]=min(possibility1,possibility2,possibility3)
    return scorematrix


with open("dataset.txt","r") as f:
    content=f.read().split()
peptide1=content[0]
peptide2=content[1]
scorematrix=ScoreMatrix(peptide1,peptide2)
print(scorematrix[len(peptide1)][len(peptide2)])













