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
      
def AffineGapAlignment(peptide1,peptide2,gapopen,gapextension):
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    tracebackl=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    tracebackm=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    tracebacku=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    lower=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    middle=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    upper=np.zeros(shape=(lengthpeptide1+1,lengthpeptide2+1))
    lower[0][0]=np.nan
    upper[0][0]=np.nan
    for i in range(1,lengthpeptide1+1):
        middle[i][0]=-gapopen-(i-1)*gapextension
        tracebackm[i][0]=23
        lower[i][0]=-gapopen-(i-1)*gapextension
        tracebackl[i][0]=13
        upper[i][0]=np.nan
    for j in range(1,lengthpeptide2+1):
        middle[0][j]=-gapopen-(j-1)*gapextension
        tracebackm[0][j]=22
        upper[0][j]=-gapopen-(j-1)*gapextension
        tracebacku[0][j]=32
        lower[0][j]=np.nan
    for i in range(1,lengthpeptide1+1):
        for j in range(1,lengthpeptide2+1):
            if not np.isnan(lower[i-1][j]):
                lower[i][j]=max(lower[i-1][j]-gapextension,middle[i-1][j]-gapopen) 
                if lower[i][j]==lower[i-1][j]-gapextension:
                    tracebackl[i][j]=13
                else:
                    tracebackl[i][j]=14
            else:
                lower[i][j]=middle[i-1][j]-gapopen
                tracebackl[i][j]=14
            if not np.isnan(upper[i][j-1]):
                upper[i][j]=max(upper[i][j-1]-gapextension,middle[i][j-1]-gapopen)
                if upper[i][j]==upper[i][j-1]-gapextension:
                    tracebacku[i][j]=32
                else:
                    tracebacku[i][j]=34
            else:
                upper[i][j]=middle[i][j-1]-gapopen
                tracebacku[i][j]=34
            middle[i][j]=max(lower[i][j],upper[i][j],middle[i-1][j-1]+scoredict[(peptide1[i-1],peptide2[j-1])])
            if middle[i][j]==lower[i][j]:
                tracebackm[i][j]=23
            elif middle[i][j]==upper[i][j]:
                tracebackm[i][j]=22
            else:
                tracebackm[i][j]=21
    return (lower,middle,upper,tracebackl,tracebackm,tracebacku)

def TraceBack(peptide1,peptide2,gapopen,gapextension):
    matrices=AffineGapAlignment(peptide1,peptide2,gapopen,gapextension)
    lower=matrices[0]
    middle=matrices[1]
    upper=matrices[2]
    tracebackl=matrices[3]
    tracebackm=matrices[4]
    tracebacku=matrices[5]
    lengthpeptide1=len(peptide1)
    lengthpeptide2=len(peptide2)
    i=lengthpeptide1
    j=lengthpeptide2
    alignedpeptide1=[]
    alignedpeptide2=[]
    finalscore=max(lower[lengthpeptide1][lengthpeptide2],middle[lengthpeptide1][lengthpeptide2],upper[lengthpeptide1][lengthpeptide2])
    if finalscore==lower[lengthpeptide1][lengthpeptide2]:
        workingtracematrix=tracebackl
    elif finalscore==middle[lengthpeptide1][lengthpeptide2]:
        workingtracematrix=tracebackm
    else:
        workingtracematrix=tracebacku
    while i or j:
        if workingtracematrix[i][j]==13:
            alignedpeptide1.insert(0,peptide1[i-1])
            alignedpeptide2.insert(0,"-")
            i-=1  
        elif workingtracematrix[i][j]==14:
            alignedpeptide1.insert(0,peptide1[i-1])
            alignedpeptide2.insert(0,"-")
            workingtracematrix=tracebackm 
            i-=1       
        elif workingtracematrix[i][j]==21:
            alignedpeptide1.insert(0,peptide1[i-1])
            alignedpeptide2.insert(0,peptide2[j-1])
            i-=1
            j-=1
            workingtracematrix=tracebackm
        elif workingtracematrix[i][j]==32:
            alignedpeptide1.insert(0,"-")
            alignedpeptide2.insert(0,peptide2[j-1])
            j-=1
        elif workingtracematrix[i][j]==34:
            alignedpeptide1.insert(0,"-")
            alignedpeptide2.insert(0,peptide2[j-1])
            workingtracematrix=tracebackm
            j-=1
        elif workingtracematrix[i][j]==22:
            workingtracematrix=tracebacku
        elif workingtracematrix[i][j]==23:
            workingtracematrix=tracebackl
        else:
            print("There seems to be a problem at",i,j,"with value:",workingtracematrix[i][j],"in this matrix:",workingtracematrix)
            return
    return (str(int(finalscore)),"".join(alignedpeptide1),"".join(alignedpeptide2))         

with open("data.txt","r") as f:
    content=f.read().split()
peptide1=content[0]
peptide2=content[1]
gapopen=11
gapextension=5
results=TraceBack(peptide1,peptide2,gapopen,gapextension)
print("For gap extension as",gapextension)
for item in results:
    print(item)




