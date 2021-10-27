from bs4 import BeautifulSoup

with open("blank/index.html", encoding = 'utf-8') as file:
    src = file.read()
#print(src)

soup = BeautifulSoup(src, "lxml")

# title = soup.title
# print(title)
# print(title.text)
# print(title.string)

#Методы .find()  .find_all()

# page_1 = soup.find_all("h1")
# print(page_1)
# for item in page_1:
#     print(item.string)

# user_name = soup.find("div").find_all(class_ = "user__city")
# print(user_name)
# for item in user_name:
#      print(item.text)
#
# social_links = soup.find("div").find(class_ = "social__networks").find("ul").find_all("a")
# print(social_links)
# for item in social_links:
#     print("Text: ", item.text)
#     print("Ссылка: ", item.get("href"))

# Найдем все a
all_a = soup.find("a")
print(all_a.text, all_a.get("href"))
# next_a = soup.find("a").next_element.text
# print_next_a
# for item in all_a:
#     print(item.text, item.get("href"))

