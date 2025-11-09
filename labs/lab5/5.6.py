list1=[1, "hello", 3.14, True, (1, 2)]
def help(x):
    dict1={}
    for i in x: 
        dict1[i]=i
    return dict1
print(help(list1))