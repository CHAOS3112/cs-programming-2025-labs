x=int(input("введите год: "))
if x%4==0 and x%100!=0: print(f'{x}- високосный год')
else: print(f'{x}- не високосный год')