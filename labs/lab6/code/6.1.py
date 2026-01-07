def convert():
    time=input("введите время, единицу измерения (h, m, s) и в какую единицу измерения нужно перевести (h, m, s):").split()
    time0= float(time[0])
    time1= str(time[1])
    time2= str(time[2])
    if time1 == "h" and time2 == "m":
        return time0*60
    elif time1 == "h" and time2 == "s":
        return time0*3600
    elif time1 == "m" and time2 == "h":
        return time0/60
    elif time1 == "m" and time2 == "s":
        return time0*60
    elif time1 == "s" and time2 == "h":
        return time/3600
    elif time1 == "s" and time2 == "m":
        return time0/60
    else:
        return "некорректные данные"
print(convert())