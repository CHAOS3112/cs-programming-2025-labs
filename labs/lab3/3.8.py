while True:
    num=input("Введите два числа через пробел:")
    x, y= map(int, num.split())
    print(f'Сумма равна:{x+y}')
    print("")