import re
def palindrome(text):
    text=text.lower()
    text= re.sub(r'\W', '', text)
    return text == text[::-1]
print(palindrome("A man, a plan, a canal: Panama"))
print(palindrome("Hello, World!"))
