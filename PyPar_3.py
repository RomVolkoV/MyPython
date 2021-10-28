import math
e = 0
x = 1
n = int(input("Введите число: "))
for i in range(0, n):
    print("i = ", i)
    x = x**i
    print("x = ",x)
    e = x / math.factorial(i)
    print("e = ",e)
    e += e
    print("einc = ",e)
    i += 1
    print(i)
print(e)