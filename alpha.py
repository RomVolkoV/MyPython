# Получаем алфавит
# alphabet = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)]
# print(alphabet)
# h1,m1,s1,h2,m2,s2 = [int(input()) for i in 'aaaaaa']
# print(h1,m1,s1,h2,m2,s2)
# h1,m1,s1,h2,m2,s2 = [int(input()) for _ in range(6)]
# print(h1,m1,s1,h2,m2,s2)

c = [x ** 3 for x in range(20) if x%2==1]
print(c)

b1 = True
b2 = True
print(b1 and b2)

array = [1,4,3,2.5,True,"romv"]
for i in list: print(i, " ", end="")

array = [i for i in range(1,20) if i%2 == 0]
print(array)