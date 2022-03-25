array_ = ["1","2","3","4","5"]
i=0
sum=0
str1 = array_[0]
for i in range(len(array_)):
    print('Индекс', i)

i = int(input('Введите число '))
print('Для индекса ', i, 'значение будет', array_[i])

for j in range(0,i):
    pass


if i == 0:
    print('Для индекса ноль значение будет', array_[0])
elif i == 1:
    print('Для индекса один значение будет', array_[1])
else:
    print('Неправильный индекс')
