def deposit():
    zxc=input("Введите сумму вклада и срок вклада через пробел: ").split()
    n=int(zxc[1])
    a=float(zxc[0])
    if a<30000:
        return Домой, Уолтер
    bonus=a/10000
    bonus0=bonus*0.3
    if bonus0>5:
        bonus0=5
    if n<=3:
        bonus1=3
    elif n>=4 and n<=6:
        bonus1=5
    elif n>6:
        bonus1=2
    BONUS = (bonus0 + bonus1) / 100 + 1
    profit = (a * (BONUS ** n)) - a
    return f"Ваш прибыль составляет {profit:.2f} рублей"
print(deposit())