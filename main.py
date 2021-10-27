import csv
import json

# Версия от 27.10.2021

name_1 = "RomV"
name_2 = "EvgV"
data_names = ["oleg", "vera"]

with open ("proba.csv", "w") as file:
    writer = csv.writer(file, delimiter = ";")

    writer.writerow(
        ("user_name", "country")
    )

users_data = [
    ["user1", "country1"],
    ["user2", "country2"],
    ["user3", "country3"],
]

for user in users_data:
    with open("proba.csv","a") as file:
        writer = csv.writer(file, delimiter = ";")
        writer.writerow(user)

with open("data.csv", "w") as file:
    writer = csv.writer(file, delimiter = ";")
    writer.writerow(
        (
            "Цена",
            "Количество монет",
            "Итог"
        )
    )

#with open("data.txt") as file1:
#    src = json.load(file1)
#print(src)




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print_hi('RomV')
    print("Разбираюсь212")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
