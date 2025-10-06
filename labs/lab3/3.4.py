x=int(input("Ну вводи число"))
if x <0:
    print("Окак")
else:
    fac=1
    for i in range(1,x+1):
        fac*=i
print(fac)
