num=input("Введите число: ")
if int(num[-1]) %2==0 and sum(map(int,num))%3==0: print("число делится на 6")
else: print("Число не делится на 6")