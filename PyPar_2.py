from bs4 import BeautifulSoup
import json
import requests

url = "http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36"
}

# req = requests.get(url, headers = headers)
# src = req.text
#print(src)

# with open("index3.html","w", encoding = 'utf-8') as file:
#     file.write(src)
#
# with open("blank/index3.html","r", encoding = 'utf-8') as file:
#      src = file.read()
#
# soup = BeautifulSoup(src,"lxml")
# all_products_href = soup.find_all(class_ = "mzr-tc-group-item-href")
# #i = 0
#
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
#     # enshure_ascii - не экранирует символы и отображает кирилицу норм

with open("blank/all_categories_dict.json") as file:
    all_categories = json.load(file)

count = 0
for category_name, category_href in all_categories.items():

    if count == 0:
        rep = [",", "-", " ", "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")
        #print(category_name)

        req = requests.get(url = categiry_href, headers = headers)
        src = reg.text

        with open(f"blank/{count}_{category_name.html}","w",encoding = 'utf-8') as file:
            file.write(src)

        count += 1