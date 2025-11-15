def help(x):
    min1=min(products, key=products.get)
    max1=max(products, key=products.get)
    return min1, max1
products={"apple":100,"banana":80,"orange":120,"grape":90}
print(help(products))