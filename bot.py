import telebot
import sqlite3
import time
import datetime
from mess import MESSAGES
from telebot.types import LabeledPrice, ShippingOption, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_token, ukassa_token

prices = [LabeledPrice(label='KokkaSun Pearl Capsules', amount=75000)]
#prices = [LabeledPrice(label='KokkaSun capsules', amount=7500), LabeledPrice('Подарочная упаковка', 500)]
shipping_options = [
    ShippingOption(id='instant', title='KokkaSun capsules').add_price(LabeledPrice('Capsules', 90000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 30000))]

bot = telebot.TeleBot(bot_token)

def save_stack(chat_id, num):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'UPDATE USERS SET Pos = ? WHERE User_id = ?'
    cursor.execute(query, (num, chat_id))
    conn.commit()
    conn.close()

def read_stack(chat_id):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM USERS WHERE User_id = ?'
    cursor.execute(query, (chat_id,))
    result = cursor.fetchall()  # читаем все
    conn.commit()
    conn.close()
    return result[0][6]

def check_art(message, Art_of_capsules):
    print("Art_of_capsules = ", Art_of_capsules.strip())
    msg = ""
    #if Art_of_capsules == 'English' or Art_of_capsules == 'Russian':

    #langv = read_langv(message.chat.id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM PRODUCTS WHERE Art = ?'
    cursor.execute(query,  (Art_of_capsules,))
    result = cursor.fetchall()  # читаем все
    #print(result[0][1], print[0][3])
    #print(result[1], result[3])
    if result:
        #msg = msg +"\n" + MESSAGES[Art_of_capsules + '_ru'] + "\n"
        bot.send_message(message.chat.id, MESSAGES[Art_of_capsules + '_ru'])
        bot.send_photo(message.chat.id, open('pic\\' + list(result[0])[1], 'rb'))
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text='Положить в корзину!', callback_data="cb_" + Art_of_capsules + "_MCI:"+ str(message.chat.id))
        markup.add(button)
        bot.send_message(message.chat.id, "Для покупки капсул...", reply_markup=markup)
    elif message.text == "Корзина":
        pass
    else:
        bot.send_message(message.chat.id, 'Введите пожалуйста код:')
    conn.close()
    return msg

def add_user(message):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    langv = 'Ru'
    data_ = [message.chat.id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"), langv, message.from_user.first_name, message.from_user.last_name, message.from_user.username]
    cursor.execute("INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?);", data_)
    conn.commit()
    conn.close()
    return

def put_to_basket(call_data):
    Articule = call_data.split('_')[1]
    Id = int(call_data.split(':')[1])
    #Прочитаем стоимость этого Артикула
    print ("Art =",  Articule, "User_id =", Id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = "SELECT * FROM PRODUCTS WHERE Art = ?"
    cursor.execute(query, (Articule,))
    result_art = cursor.fetchall()
    Price = result_art[0][4]
    print(result_art, result_art[0][4])
    #Прочитать, что уже есть в корзине у этого покупателя

    query = "SELECT * FROM BASKET WHERE User_id = ? and Art = ?"
    cursor.execute(query, (Id, Articule))
    result = cursor.fetchall()
    if result ==[]:
        print("В корзине нет этого Артикула ", result)
        query = "INSERT INTO BASKET VALUES(?, ?, ?, ?)"
        data_ = [Id, Articule, 1, Price]
        cursor.execute(query, data_)
        conn.commit()

    else:
        print("В корзине уже есть этот Артикул ", result[0][2])
        Kol_ = result[0][2] + 1
        Amount = Kol_ * Price
        query = "UPDATE BASKET SET Kol = ?, Amount = ? WHERE Art = ? and User_id = ?"
        data_ = [Kol_, Amount, Articule, Id]
        cursor.execute(query, data_)
        conn.commit()
    bot.send_message(Id, "Капсулы добавлены в корзину. Вы можете продолжить выбирать товары или перейти в корзину для покупки!")
    conn.close()

def read_basket(message, silence):
    print(silence)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = "SELECT * FROM BASKET WHERE User_id = ?"
    cursor.execute(query, (message.chat.id,))
    result = cursor.fetchall()
    if result:
        #print(len(result))
        item = 0
        Amount = 0
        while item < len(result):
            #print(result[item][0], result[item][1], result[item][2], result[item][3] )
            if silence == 1:
                msg = "Капсулы: " + result[item][1] + "\nКол-во: " + str(result[item][2]) +" уп. " + " На сумму: " + \
                  str(result[item][3]) + " Руб."
                bot.send_message(message.chat.id, msg )
            Amount = Amount + result[item][3]
            item +=1
        if silence == 1:
            bot.send_message(message.chat.id, "Всего на сумму : " + str(Amount) + " Руб.")
            # нужно подумать!
            bot.send_message(message.chat.id, "Хотите изменить количество? Пришлите мне наименование "
                                          "капсул и количество упаковок через пробел, например: Green 4 или Pink 1. "
                                          "Чтобы удалить капсулы из корзины вместо количества введите 0")
    else:
        if silence == 1:
            bot.send_message(message.chat.id, "В корзине пока пусто!")
    return item

def read_user(message):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM USERS WHERE User_id = ?'
    cursor.execute(query,  (message.chat.id,))
    result = cursor.fetchall()  # читаем все
    if result == []:
        add_user(message)
    conn.commit()
    conn.close()
    return

def update_user(chat_id, langv):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'UPDATE USERS SET Langv = ? WHERE User_id = ?'
    cursor.execute(query, (langv, chat_id,))
    conn.commit()
    conn.close()

def check_code(message, text):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM CODE_TAB WHERE Code = ?'
    cursor.execute(query, (text,))
    res = cursor.fetchall()  # читаем все
    conn.close()
    if res:
        kol = list(res[0])[1]
        kol += 1
        conn = sqlite3.connect(r'db/kokka.db')
        cursor = conn.cursor()
        query = 'UPDATE CODE_TAB SET Count = ? WHERE Code = ?'
        cursor.execute(query, (kol, text,))
        conn.commit()
        conn.close()
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
#    print(text, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"))
    data_ = [text, message.from_user.id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")]
    cursor.execute("INSERT INTO USER_TAB VALUES(?, ?, ?);", data_)
    conn.commit()
    conn.close()
    return (res)

def make_menu(message, pos):
    kol_in_basket = read_basket(message, 0)  # Прочитать кооличество позиций в корзине и информацию на экран не выводить
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    if pos == 1:
        start_menu.row('Для лица', 'Вокруг глаз', 'Для тела', 'Для волос')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Доставка', 'О нас')
        bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
        bot.send_message(message.chat.id, MESSAGES['start_message_ru'], reply_markup=start_menu)
    elif pos == 11:
        start_menu.row('Для лица', 'Вокруг глаз', 'Для тела', 'Для волос')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Доставка', 'О нас')
        bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
        bot.send_message(message.chat.id, MESSAGES['help_message_ru'], reply_markup=start_menu)
    elif pos == 2:
        start_menu.row('Pearl', 'Pink', 'Violet', 'Grape')
        start_menu.row('Gold', 'White', 'Yellow')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Назад')
        bot.send_message(message.chat.id, "Капсулы для лица " + message.text, reply_markup=start_menu)
    elif pos == 3:
        start_menu.row('Purple', 'Rose' 'Grape')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Назад')
        bot.send_message(message.chat.id, "Капсулы для кожи вокруг глаз " + message.text, reply_markup=start_menu)
    elif pos == 4:
        start_menu.row('Grape', 'ET-Gold', 'ET-Purple')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Назад')
        bot.send_message(message.chat.id, "Капсулы для тела " + message.text, reply_markup=start_menu)
    elif pos == 5:
        start_menu.row('Green')
        start_menu.row('Корзина(' + str(kol_in_basket) + ')', 'Назад')
        bot.send_message(message.chat.id, "КоккаSun " + message.text, reply_markup=start_menu)
    elif pos == 6:
        start_menu.row('Редактировать')
        start_menu.row('Оплатить', 'Назад')
        bot.send_message(message.chat.id, "КоккаSun " + message.text, reply_markup=start_menu)
    # elif pos == 7 or pos == 8:
    #     start_menu.row('Назад')
    #     bot.send_message(message.chat.id, "КоккаSun " + message.text, reply_markup=start_menu)

# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     #markup.row_width = 2
#     markup.add(InlineKeyboardButton("Yes", callback_data="cb_basket"))
# #                               InlineKeyboardButton("No", callback_data="cb_no"))
#     #return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    read_user(message)
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, ' написал start')
    # сохраняем позицию для пользователя Позиция = 1
    save_stack(message.chat.id, 1)
    make_menu(message, 1)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "Капсулы в корзине!")
    # Кладем в корзину капсулы.
    #print(call.data)
    put_to_basket(call.data)
    if call.data == "cb_Pearl":

        bot.answer_callback_query(call.id, "Pearl-капсулы в корзине")
    elif call.data == "cb_Green":
        bot.answer_callback_query(call.id, "Green-капсулы в корзине")

@bot.message_handler(commands=['terms'])
def process_terms_command(message):
#    read_user(message)
    bot.send_message(message.chat.id, MESSAGES['terms'])
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
          ' написал terms')


@bot.message_handler(commands=['help'])
def help_message(message):
    save_stack(message.chat.id, 1)
    make_menu(message, 11)


@bot.message_handler(commands=['pay'])
def process_buy_command(message):
    if ukassa_token.split(':')[1] == 'TEST':
        bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'], parse_mode='Markdown')
#        print(ukassa_token)
        #bot.send_invoice()
    bot.send_invoice(message.chat.id,
                           title = MESSAGES['tm_title'],
                           description = MESSAGES['tm_description'],
                           provider_token = ukassa_token,
                           currency = 'RUB',
                           #photo_url=TIME_MACHINE_IMAGE_URL,
                           #photo_height=512,  # !=0/None, иначе изображение не покажется
                           #photo_width=512,
                           #photo_size=512,
                           is_flexible = True,  # True если конечная цена зависит от способа доставки
                           prices = prices,
                           start_parameter = 'kokkasun-caps',
                           invoice_payload = '00007')
    print("Цена - ", prices)

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Благодарим за оплату. Ваш заказ на сумму `{} {}` уже в обработке! '
                     'Наши менеджеры свяжутся с Вами в ближайшее время!'
                     'Будьте на связи.\n\n'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')

@bot.message_handler(content_types = ['text'])
def send_text(message):
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'написал: ', message.text,datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S"))
    read_user(message)
    # start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    # start_menu.row('Green', 'Pearl', 'Pink', 'Purple')
    # start_menu.row('Violet', 'Grape', 'Gold')
    # start_menu.row('Корзина')
    #bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
    # if message.text == 'Eng':
    #     update_user(message.chat.id, 'En')
    #     bot.send_message(message.chat.id, MESSAGES['start_message'], reply_markup=start_menu)
    # if message.text == 'Rus':
    #     update_user(message.chat.id, 'Ru')
    #bot.send_message(message.chat.id, "КоккаSun " + message.text, reply_markup=start_menu)
    #bot.send_message(message.chat.id, MESSAGES['text_message_ru'] + message.text, reply_markup=start_menu)

    #langv = read_langv(message.chat.id)

    result = check_code(message, message.text)
    #print(result, len(result))
    if result:
        for i in range(0, len(result)):
            code = list(result[i])[0]
            kol = list(result[i])[1] + 1
            art = list(result[i])[2]
            photo = list(result[i])[3]
            batch = list(result[i])[4]
            data_mfg = list(result[i])[5]
            data_exp = list(result[i])[6]
            barcode = list(result[i])[7]
            bc_pic = list(result[i])[8]
            fio = list(result[i])[9]
        #print(code," ", kol, " ", art, " ", photo, " ", batch, " ", data_mfg, " ", data_exp, " ", barcode, " ", bc_pic, " ", fio)
        # if langv == 'En':
        #     bot.send_message(message.chat.id, 'Congratulations on your purchase dear friend!'+ '\n' +'Wait a moment, please, I`m checking you code...')
        #     msg = "Code " + code + ". Information: "
        # elif langv == 'Ru':
        bot.send_message(message.chat.id, 'Поздравляем вас с покупкой!' + '\n' + 'Секундочку, я проверяю ваш код...')
        msg = "Код " + code + ". Информация: "
        time.sleep(1)
        #msg = msg + check_art(message,art)
        #msg = msg + choose_mess(message, art)
        msg = msg + "\n" + MESSAGES[art + "_ru"] + "\n"
        # if langv == 'En':
        #     msg = msg + "Batch - " + batch + "\n" + "MFG - " + data_mfg + "\n" + "EXP - " + data_exp + "\n"
        # elif langv == 'Ru':
        msg = msg + "Серия - " + batch + "\n" + "Произведено - " + data_mfg + "\n" + "Годен до - " + data_exp + "\n"
        bot.send_message(message.chat.id, msg)
        #time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\'+ photo, 'rb'))
        #time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\' + bc_pic, 'rb'))
        if kol == 1:
            time.sleep(1)
            # if langv == 'En':
            #     msg_ = 'ATTENTION! This code is checked for the FIRST time!' + '\n' + 'No one else has seen him!' + '\n'
            #     msg_ = msg_ + 'Save this code to participate in the KokkaSun promotions!'
            # elif langv == 'Ru':
            msg_ = 'ВНИМАНИЕ! Этот код проверяется впервые!' + '\n' + 'Никто не вводил его до вас!' + '\n' + 'Поздравляем вас с приобретением оригинального продукта КоккаSun.' + '\n'
            msg_ = msg_ + 'Сохраните этот код для дальнейшего участия в акциях КоккаSun!'
            bot.send_message(message.chat.id, msg_)
        else:
            #time.sleep(1)
            # if langv == 'En':
            #     bot.send_message(message.chat.id, "The code was checked " + str(kol) + " times")
            # elif langv == 'Ru':
            bot.send_message(message.chat.id, "Код был проверен " + str(kol) + " раз")
    elif message.text == "Назад":
        pos = read_stack(message.chat.id)
        print("Позиция : ", pos)
        if pos == 2 or pos == 3 or pos == 4 or pos == 5:
            make_menu(message, 1)
            save_stack(message.chat.id, 1)
        else:
            make_menu(message, pos - 6)
            save_stack(message.chat.id, pos-6)
    elif message.text == "Для лица":
        # Меню с капсулами Pearl, Pink, Violet, Grape
        # Текущая поза = 1, сохраняем 3
        save_stack(message.chat.id,2)
        make_menu(message, 2)
    elif message.text == "Вокруг глаз":
        # Меню с капсулами Purple, Grape
        save_stack(message.chat.id, 3)
        make_menu(message, 3)
    elif message.text == "Для тела":
        # Меню с капсулами Grape, ET-Gold, ET-Purple
        save_stack(message.chat.id, 4)
        make_menu(message,4)
    elif message.text == "Для волос":
        save_stack(message.chat.id, 5)
        make_menu(message, 5)
        # Меню с капсулами Green
    elif message.text == "Доставка":
        # make_menu(message, 7)
        pass # Вывести текстовку о доставке

    elif message.text == "О нас":
        # make_menu(message, 8)
        pass # Вывести текстовку о нас

    elif message.text.split('(')[0] == "Корзина": # Articule = call_data.split('_')[1]
        pos = read_stack(message.chat.id)
        print("Текущая позиция", pos)
        read_basket(message,1)
        make_menu(message, 6)
        save_stack(message.chat.id, 6 + pos)

    else:
        check_art(message, message.text)

if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
