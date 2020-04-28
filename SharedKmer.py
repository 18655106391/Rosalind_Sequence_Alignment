base2num={"A":0,"C":1,"G":2,"T":3}
def Kmer2Num(kmer):
    if len(kmer)==1:
        return base2num[kmer]
    return 4*Kmer2Num(kmer[:-1])+Kmer2Num(kmer[-1])   


def HashString(string,k):
    kmerpositions={}
    for i in range(len(string)-k+1):
        key=Kmer2Num(string[i:i+k])
        if key not in kmerpositions:
            kmerpositions[key]=[i]
        else:
            kmerpositions[key].append(i)
        key=Kmer2Num(ReverseComplement(string[i:i+k]))
        if key not in kmerpositions:
            kmerpositions[key]=[i]
        else:
            kmerpositions[key].append(i)
    return kmerpositions

def ReverseComplement(string):
    complement=[]
    pairing_rule={"A":"T","T":"A","C":"G","G":"C"}
    for base in string:
        complement.insert(0,pairing_rule[base])
    return "".join(complement)

def SharedKmers(string1,string2,k):
    pairs=[]
    kmerpositions_string1=HashString(string1,k)
    for i in range(len(string2)-k+1):
        kmer=string2[i:i+k]
        key=Kmer2Num(kmer)
        if key in kmerpositions_string1:
            for position in kmerpositions_string1[key]:
                pairs.append((position,i))
    return pairs


with open("E_coli.txt","r") as f:
    read2=f.read().split()[0]
    
with open("Salmonella_enterica.txt","r") as f:
    read1=f.read().split()[0]
k=30
answer=list(set(SharedKmers(read1,read2,k)))
print(answer)
print(len(answer))
with open("num.txt",'w') as f:
    f.write(str(len(nswer)))
with open("answer.txt","w") as f:
    for item in answer:
        f.write("(")
        f.write(str(item[0]))
        f.write(", ")
        f.write(str(item[1]))
        f.write(")\n")
