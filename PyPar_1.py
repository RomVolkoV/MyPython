from bs4 import BeautifulSoup
import re

with open("blank/index.html", encoding = 'utf-8') as file:
    src = file.read()

print(src)

soup = BeautifulSoup(src, "lxml")

title = soup.title
print(title)
print(title.text)
print(title.string)

# Методы .find()  .find_all() - решают 90 % задач парсинга

page_1 = soup.find_all("h1")
print(page_1)
for item in page_1:
    print(item.string)

# class - зарезервированное слово поэтому добавляем подчеркивание

user_name = soup.find("div").find_all(class_ = "user__city")
print(user_name)
for item in user_name:
     print(item.text)

social_links = soup.find("div").find(class_ = "social__networks").find("ul").find_all("a")
print(social_links)
for item in social_links:
    print("Text: ", item.text)
    print("Ссылка: ", item.get("href"))

user_name = soup.find("div", class_ = "user__name").find("span").text
print(user_name)

# Найдем все a
all_a = soup.find("a")
print(all_a.text, all_a.get("href"))
next_a = soup.find("a").next_element.text
print_next_a
for item in all_a:
    print(item.text, item.get("href"))

post_div = soup.find(class_ = "post__text")
post_div_parent = soup.find(class_ = "post__text").find_parent("div", "user__post")
print(f"{post_div}")
print("-----------")
print(f"{post_div_parent}")

post_div = soup.find(class_ = "post__text")
post_div_parent = soup.find(class_ = "post__text").find_parents()
print(f"{post_div}")
print("-----------")
print(f"{post_div_parent}")


# next_element previous_element
post_title = soup.find(class_ = "post__title").next_element.next_element.text
print(f"{post_title}")

# find_next()
post_title = soup.find(class_ = "post__title").find_next().text
print(f"{post_title}")

# .find_next_sibling() .find_previous_sibling()
next_sib = soup.find(class_="post__title").find_next_sibling()
print(next_sib)

prev_sib = soup.find(class_="post__date").find_previous_sibling()
print(prev_sib)

# Можно комбинировать методы
post_title = soup.find(class_="post__date").find_previous_sibling().find_next().text
print(post_title)

links = soup.find("div", class_ = "some__links").find_all("a")
print(links)

for item in links:
    link_text = item.text
    link_href = item["href"]
    link_data_attr = item.get("data-attr")
    print(f"{link_text}:{link_href}:{link_data_attr}")

# вместо метода get можно так
link_href = item.get("href")
link_href = item["href"]

find_a_by_text = soup.find("a", text = "Одежда")
print(find_a_by_text)

find_a_by_text = soup.find("a", text = "Одежда для взрослых")
print(find_a_by_text)

# модуль регулярных выражений re
find_a_by_text = soup.find("a", text = re.compile("Одежда"))
print(find_a_by_text)

find_a_by_text = soup.find("a", text = re.compile("([Оо]дежд)"))
print(find_a_by_text)