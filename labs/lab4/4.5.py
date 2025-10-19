pas= input("введите пароль: ")
def chek(password):
    if len(password)<8: return print("пароль должен содержать не менее 8 символов")
    if password.lower()== password: return print("пароль должен содержать хотябы 1 заглавный символ")
    if password.upper()== password: return print("пароль должен содержать хотябы 1 символ нижнего регистра")
    if not any(x.isdigit() for x in password): return print("пароль должен содержать хотябы 1 цифру")
    if not any(x.isalnum() for x in password): return print("пароль должен содержать хотябы 1 специальный символ")
    else: return print("пароль установлен")
print(chek(pas))