import numpy as np

with open("data.txt","r") as f:
    content=f.read().split()
sequence1=content[0]
sequence2=content[1]
sequence3=content[2]

def Score(a,b,c):
    if a==b and a==c:
        return 1
    else:
        return 0

def ScoreMatrix(sequence1,sequence2,sequence3):
    lengthsequence1=len(sequence1)
    lengthsequence2=len(sequence2)
    lengthsequence3=len(sequence3)
    scorematrix=np.zeros(((lengthsequence1+1,lengthsequence2+1,lengthsequence3+1)))
    traceback=np.zeros(((lengthsequence1+1,lengthsequence2+1,lengthsequence3+1)))
    for i in range(1,lengthsequence1+1):
        for j in range(1,lengthsequence2+1):
            for k in range(1,lengthsequence3+1):
                possibility=[0]*8
                possibility[1]=scorematrix[i-1][j][k]
                possibility[2]=scorematrix[i][j-1][k]
                possibility[3]=scorematrix[i][j][k-1]
                possibility[4]=scorematrix[i-1][j-1][k]
                possibility[5]=scorematrix[i-1][j][k-1]
                possibility[6]=scorematrix[i][j-1][k-1]
                possibility[7]=scorematrix[i-1][j-1][k-1]+Score(sequence1[i-1],sequence2[j-1],sequence3[k-1])
                scorematrix[i][j][k]=max(possibility)
                traceback[i][j][k]=possibility.index(scorematrix[i][j][k])
    return (scorematrix,traceback)

def Alignment(sequence1,sequence2,sequence3):
    scorematrix,traceback=ScoreMatrix(sequence1,sequence2,sequence3)
    print("Scorematrix:\n",scorematrix)
    print("Traceback:\n",traceback)
    alignedsequence1=[]
    alignedsequence2=[]
    alignedsequence3=[]
    i=len(sequence1)
    j=len(sequence2)
    k=len(sequence3)
    score=scorematrix[i][j][k]
    while i or j or k: 
        temp=traceback[i][j][k]
        #print("position",i,j,k,"has score",scorematrix[i][j][k],"and traceback",traceback[i][j][k])
        if temp==1:
            alignedsequence1.insert(0,sequence1[i-1])
            alignedsequence2.insert(0,"-")
            alignedsequence3.insert(0,"-")
            i-=1
        elif temp==2:
            alignedsequence1.insert(0,"-")
            alignedsequence2.insert(0,sequence2[j-1])
            alignedsequence3.insert(0,"-")
            j-=1
        elif temp==3:
            alignedsequence1.insert(0,"-")
            alignedsequence2.insert(0,"-")
            alignedsequence3.insert(0,sequence3[k-1])
            k-=1
        elif temp==4:
            alignedsequence1.insert(0,sequence1[i-1])
            alignedsequence2.insert(0,sequence2[j-1])
            alignedsequence3,insert(0,"-")
            i-=1
            j-=1
        elif temp==5:
            alignedsequence1.insert(0,sequence1[i-1])
            alignedsequence2.insert(0,"-")
            alignedsequence3.insert(0,sequence3[k-1])
            i-=1
            k-=1
        elif temp==6:
            alignedsequence1.insert(0,"-")
            alignedsequence2.insert(0,sequence2[j-1])
            alignedsequence3.insert(0,sequence3[k-1])
            j-=1
            k-=1
        elif temp==7:
            alignedsequence1.insert(0,sequence1[i-1])
            alignedsequence2.insert(0,sequence2[j-1])
            alignedsequence3.insert(0,sequence3[k-1])
            i-=1
            j-=1
            k-=1
        else:
            if i==0:
                if j:
                    if k:
                        alignedsequence1.insert(0,"-")
                        alignedsequence2.insert(0,sequence2[j-1])
                        alignedsequence3.insert(0,sequence3[k-1])
                        j-=1
                        k-=1
                    else:
                        alignedsequence1.insert(0,"-")
                        alignedsequence2.insert(0,sequence2[j-1])
                        alignedsequence3.insert(0,"-")
                        j-=1
                else:
                    alignedsequence1.insert(0,"-")
                    alignedsequence2.insert(0,"-")
                    alignedsequence3.insert(0,sequence3[k-1])
                    k-=1
            else:
                if j:
                    alignedsequence1.insert(0,sequence1[i-1])
                    alignedsequence2.insert(0,sequence2[j-1])
                    alignedsequence3.insert(0,"-")
                    i-=1
                    j-=1
                else:
                    if k:
                        alignedsequence1.insert(0,sequence1[i-1])
                        alignedsequence2.insert(0,"-")
                        alignedsequence3.insert(0,sequence3[k-1])
                        i-=1
                        k-=1
                    else:
                        alignedsequence1.insert(0,sequence1[i-1])
                        alignedsequence2.insert(0,"-")
                        alignedsequence3.insert(0,"-")
                        i-=1
        print(alignedsequence1,"\n",alignedsequence2,"\n",alignedsequence3,"\n")
    return (str(int(score)),"".join(alignedsequence1),"".join(alignedsequence2),"".join(alignedsequence3))

with open("dataset_251_5.txt","r") as f:
    content=f.read().split()
    sequence1=content[0]
    sequence2=content[1]
    sequence3=content[2]
result=Alignment(sequence1,sequence2,sequence3)
print(result)

with open("answer.txt","w") as f:
    for item in result:
        f.write(item)
        f.write('\n')

