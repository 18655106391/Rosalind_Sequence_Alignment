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

with open("data.txt","r") as f:
    content=f.read().split()
sequence1=content[0]
sequence2=content[1]
gappenalty=5

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
            
def Reverse(peptide):
    return peptide[::-1]

def MiddleEdge(peptide1,peptide2,gappenalty,top,bottom,left,right):
    investigatingwidth=right-left+1
    if investigatingwidth>2:
        middle=(left+right)//2
        firsthalf=EndColumnScore(peptide1[top:bottom],peptide2[left:middle],gappenalty)
        firsthalfscore=firsthalf[0]
        reversedpeptide1=Reverse(peptide1[top:bottom])
        reversedhalfpeptide2=Reverse(peptide2[middle:right])
        secondhalf=EndColumnScore(reversedpeptide1,reversedhalfpeptide2,gappenalty)
        secondhalfscore=secondhalf[0]
        secondhalftrace=secondhalf[1]
        secondhalfscore=secondhalfscore[::-1]
        secondhalftrace=secondhalftrace[::-1]
        finalscore=[]
        for i in range(len(secondhalfscore)):
            finalscore.append(firsthalfscore[i]+secondhalfscore[i])
        rowmiddlenode=finalscore.index(max(finalscore))
        startmidedge=(rowmiddlenode+top,middle)
        if secondhalftrace[rowmiddlenode]==1:
            endmidedge=(rowmiddlenode+1+top,middle+1)
        elif secondhalftrace[rowmiddlenode]==2:
            endmidedge=(rowmiddlenode+top,middle+1)
        else:
            endmidedge=(rowmiddlenode+1+top,middle)
        return [startmidedge,endmidedge]
      
    if investigatingwidth==2:
        firstscores=[]
        for i in range(bottom-top+1):
            firstscores.append(-i*gappenalty)
        reversedpeptide1=Reverse(peptide1[top:bottom])
        temp=EndColumnScore(reversedpeptide1,peptide2[left:right],gappenalty)
        secondscores=temp[0]
        secondscores=secondscores[::-1]
        backpointer=temp[1]
        backpointer=backpointer[::-1]
        finalscores=[]
        for i in range(len(secondscores)):
            finalscores.append(firstscores[i]+secondscores[i])
        rowmiddlenode=finalscores.index(max(finalscores))
        if backpointer[rowmiddlenode]==1:
            return[(rowmiddlenode+top,left),(rowmiddlenode+1+top,right)]
        elif backpointer[rowmiddlenode]==2:
            return[(rowmiddlenode+top,left),(rowmiddlenode+top,right)]
        else:
            return[(rowmiddlenode+top,left),(rowmiddlenode+1+top,left)]


def LinearSpaceAlignment(peptide1,peptide2,gappenalty,top,bottom,left,right,path): 
    if left==right:
        for i in range(top,bottom+1):
            path.append((i,left))
        return path
    if top==bottom:
        for j in range(left,right+1):
            path.append((top,j))
        return path
    midedge=MiddleEdge(peptide1,peptide2,gappenalty,top,bottom,left,right)
    firstrectangleright=midedge[0][1]
    firstrectanglebottom=midedge[0][0]
    secondrectangleleft=midedge[1][1]
    secondrectangletop=midedge[1][0]
    path=LinearSpaceAlignment(peptide1,peptide2,gappenalty,top,firstrectanglebottom,left,firstrectangleright,path)
    path=LinearSpaceAlignment(peptide1,peptide2,gappenalty,secondrectangletop,bottom,secondrectangleleft,right,path)
    return path

    
def Trace(peptide1,peptide2,path):
    alignedpeptide1=[]
    alignedpeptide2=[]
    index1=0
    index2=0
    for i in range(1,len(path)):
        pre=path[i-1]
        suf=path[i]
        if suf[0]==pre[0]+1:
            if suf[1]==pre[1]+1:
                alignedpeptide1.append(peptide1[index1])
                alignedpeptide2.append(peptide2[index2])
                index1+=1
                index2+=1
            else:
                alignedpeptide1.append(peptide1[index1])
                alignedpeptide2.append("-")
                index1+=1
        else:
            alignedpeptide1.append("-")
            alignedpeptide2.append(peptide2[index2])
            index2+=1
    return ["".join(alignedpeptide1),"".join(alignedpeptide2)]

def FinalScore(alignedpeptides):
    peptide1=alignedpeptides[0]
    peptide2=alignedpeptides[1]
    score=0
    for i in range(len(peptide1)):
        if peptide1[i]!='-' and peptide2[i]!='-':
            score+=scoredict[(peptide1[i],peptide2[i])]
        else:
            score-=gappenalty
    return score

bestpath=LinearSpaceAlignment(sequence1,sequence2,gappenalty,0,len(sequence1),0,len(sequence2),[])
alignedpeptides=Trace(sequence1,sequence2,bestpath)
score=FinalScore(alignedpeptides)

with open("answer.txt","w") as f:
    f.write(str(score))
    f.write("\n")
    f.write(alignedpeptides[0])
    f.write("\n")
    f.write(alignedpeptides[1])





