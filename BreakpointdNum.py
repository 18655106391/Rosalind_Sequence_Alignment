def BreakpointNum(p):
    lengthp=len(p)
    p.append(lengthp+1)
    p.insert(0,0)
    breakpointnum=0
    for i in range(lengthp+1):
        if p[i+1]-p[i]!=1:
            breakpointnum+=1
    return breakpointnum
            
with open('dataset_287_6.txt','r') as f:
    p=list(map(int,f.read().split()))
print(BreakpointNum(p))
