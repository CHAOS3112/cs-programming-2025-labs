x=int(input("Введите число: "))
def check(num):
    if num<=1: return "ошибка: простое число должно быть больше 1"
    elif num==2: return f'{num}- простое число'
    elif num%2==0 or num%3==0: return f'{num}- составное число'
    else: return f'{num}-простое число'
print(check(x))
