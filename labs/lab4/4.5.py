pas= input("введите пароль: ")
def chek(password):
    if len(password)<8: print("пароль должен содержать не менее 8 символов")
    if password.lower()== password: print("пароль должен содержать хотябы 1 заглавный символ")
    if password.upper()== password:  print("пароль должен содержать хотябы 1 символ нижнего регистра")
    if not any(x.isdigit() for x in password):  print("пароль должен содержать хотябы 1 цифру")
    if not any(x.isalnum() for x in password):  print("пароль должен содержать хотябы 1 специальный символ")
    else: print("пароль установлен")

chek(pas)