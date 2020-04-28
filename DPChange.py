def DPChange(money,coins):
    minnumcoins=[]
    minnumcoins.append(0)
    for change in range(1,money+1):
        minnumcoins.append(money)
        for coin in coins:
            if coin<=change:
                if minnumcoins[change-coin]+1<minnumcoins[change]:
                    minnumcoins[change]=minnumcoins[change-coin]+1
    return minnumcoins[money]

with open("dataset.txt","r") as f:
    content=f.read().split()
money=int(content[0])
coins=list(map(int,content[1].split(",")))
coins.sort(reverse=True)

print(DPChange(money,coins))
