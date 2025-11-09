def sort(x):
    if all(isinstance(item, (int, float)) for item in x):
        return tuple(sorted(x))
    return x
lis1=[3,2,5,6,1,5]
lis=[a,f,3,5,h,4]
print(sort(lis1))
print(sort(lis2))