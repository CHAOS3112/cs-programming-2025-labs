txt=input("введи слово:")
res=""
k=0
while k<len(txt):
    res+= txt[k]+str(k+1)
    k+=1
print(res)