def eng_rus(x,word):
    for eng, rus in x.items():
        if rus==word:
            return eng
        return None
d = {"apple": "яблоко","banana": "банан", "orange": "апельсин","cat": "кот","dog": "собака","house": "дом","car": "машина"}
print(eng_rus(d, 'яблоко'))