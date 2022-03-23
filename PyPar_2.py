from bs4 import BeautifulSoup
import json
import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('Началось')


url = "https://cbr.ru/currency_base/daily/"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36"
}

req = requests.get(url, headers = headers)
src = req.text
# print(src)

# with open("cbr_.html","w", encoding = 'utf-8') as file:
#     file.write(src)

# with open("cbr_.html","r", encoding = 'utf-8') as file:
#      src = file.read()

# Получаем
soup = BeautifulSoup(src,"lxml")
# all_currency = soup.find_all(class_ = "data").find("tr").find_all("th")
# title = soup.find_all(class_ = "data").find("th")
# title = soup.find(class_ = "data").find_all("th")
#
# i = 0
# title_array = []
# for item in title:
#     title_array.append(item.text)
# print(title_array)

all_currency = soup.find(class_ = "data").find_all("td")

data_array=[]
for item in all_currency:
    data_array.append(item.text)

i = 0
for item in data_array:
    if item == "Евро":
        print("Курс " + item + " : ", data_array[i+1])
    i += 1
    # str_=""
    # for _ in range(0,5):
    #     str_= str_+ " " + data_array[i]
    #     i +=1
    # print(str_)
    # print(data_array)

# all_categories_dict = {}
# for item in all_products_href:
#     item_text = item.text
#     item_href = "http://health-diet.ru" + item["href"]
#     #print(f"{item_text}: {item_href}")
#     all_categories_dict[item_text] = item_href
# #     i += 1
# # print(i)
# with open("blank/all_categories_dict.json","w") as file:
#     json.dump(all_categories_dict, file, indent = 4, ensure_ascii = False)
#     # параментр indent - это отступ. Если убрать, то все пишется в одну строку
#     # enshure_ascii с флагом False - не экранирует символы и отображает кирилицу норм

# with open("blank/all_categories_dict.json") as file:
#     all_categories = json.load(file)
# # Убедимся, что файл прочитан
# #print(all_categories)
#
# count = 0
# for category_name, category_href in all_categories.items():

 #Для удобства чтения - заменить символы: зпт, тире, пробел и верхняя ковычка на нажнее подчеркивание
    # if count == 0:
    #     rep = [",", "-", " ", "'"] # Список из символов, которые хоти заменить
    #     for item in rep:
    #         if item in category_name:
    #             category_name = category_name.replace(item, "_")
    #     #print(category_name)
    #
    #     req = requests.get(url = category_href, headers = headers)
    #     src = req.text
    #
    #     with open(f"blank/{count}_{category_name}.html","w",encoding = 'utf-8') as file:
    #         file.write(src)
    #
    #     with open(f"blank/{count}_{category_name}.html",encoding = 'utf-8') as file:
    #         src = file.read()
    #     soup = BeautifulSoup(src, "lxml")

# Собираем заголовки таблицы
#         table_head = soup.find(class_ = "uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find("tr").find_all("th")
#         product = table_head[0].text
#         calories = table_head[1].text
#         proteins = table_head[2].text
#         fats = table_head[3].text
#         carbohydrates = table_head[4].text
#         print(carbohydrates)
#         count += 1