#Получаем алфавит
# alphabet = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)]
# print(alphabet)
# h1,m1,s1,h2,m2,s2 = [int(input()) for i in 'aaaaaa']
# print(h1,m1,s1,h2,m2,s2)
# a,b,c,d,e,f = [int(input()) for _ in range(6)]
# print(a,b,c,d,e,f)

c = [x ** 3 for x in range(20) if x%2==1]
print(c)

b1 = True
b2 = True
print(b1 and b2)

array = [1,4,3,2.5,True,"romv"]
for i in array: print(i, " ", end=" ")
print()
array = [i for i in range(1,20) if i%2 == 0]
print(array)

d = {'a': 11, 'b': 22, 'c': 33}
print(d[list(d)[0]])
print(d[list(d.keys())[1]])
