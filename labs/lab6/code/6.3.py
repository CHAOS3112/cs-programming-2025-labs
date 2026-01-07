def prime_num():
    zxc=input("Введите помежуток чисел: ").split()
    a=int(zxc[0])
    b=int(zxc[1])
    primes=[]
    if a > b: return "Error!"
    for num in range(a,b+1):
        if num>1:
            prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    prime = False
                    break
            if prime:
                primes.append(num)
    if not primes:
        return "Error!"
    return " ".join(str(x) for x in primes)
print(prime_num())