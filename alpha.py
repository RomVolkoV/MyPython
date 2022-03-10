#Получаем алфавит
alphabet = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)]
print(alphabet)
h1,m1,s1,h2,m2,s2 = [int(input()) for i in 'aaaaaa']
print(h1,m1,s1,h2,m2,s2)
h1,m1,s1,h2,m2,s2 = [int(input()) for _ in range(6)]
print(h1,m1,s1,h2,m2,s2)