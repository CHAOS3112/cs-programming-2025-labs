words = ["яблоко", "груша", "банан", "киви", "апельсин", "ананас"]
def dict(x):
    first = set(word[0] for word in x)
    return {letter: [word for word in x if word[0] == letter] 
            for letter in first}
result_dict = dict(words)
print(dict(words))