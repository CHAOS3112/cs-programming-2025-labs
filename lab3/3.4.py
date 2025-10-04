x=int(input("Ну вводи число"))
if x <0:
    print("Окак")
else:
    fack=1
    for i in range(1,x+1):
        fack*=i
print(fack)
