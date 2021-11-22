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

def choose_mess(message, Art_of_capsules):
    msg = ""
    langv = read_langv(message.chat.id)
    if langv == 'En':
        msg = msg + "\n" + MESSAGES[Art_of_capsules] + "\n"
    elif langv == 'Ru':
        msg = msg + "\n" + MESSAGES[Art_of_capsules + "_ru"] + "\n"
    return msg

def check_art(message, Art_of_capsules):
    print("Art_of_capsules = ", Art_of_capsules.strip())
    msg = ""
    #if Art_of_capsules == 'English' or Art_of_capsules == 'Russian':

    langv = read_langv(message.chat.id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM PRODUCTS WHERE Art = ?'
    cursor.execute(query,  (Art_of_capsules,))
    result = cursor.fetchall()  # читаем все
    #print(result[0][1], print[0][3])
    #print(result[1], result[3])
    if result:
        if langv == 'En':
            msg = msg +"\n" + MESSAGES[Art_of_capsules] + "\n"
        elif langv == 'Ru':
            msg = msg +"\n" + MESSAGES[Art_of_capsules + '_ru'] + "\n"
        bot.send_message(message.chat.id, msg)
        bot.send_photo(message.chat.id, open('pic\\' + list(result[0])[1], 'rb'))
        time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\' + list(result[0])[3], 'rb'))

        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text='Положить в корзину!', callback_data="cb_" + Art_of_capsules + "_MCI:"+ str(message.chat.id))
        markup.add(button)
        bot.send_message(message.chat.id, "Для покупки капсул...", reply_markup=markup)

    else:
        if langv == 'En':
            bot.send_message(message.chat.id, 'Enter the code please:')
        if langv == 'Ru':
            bot.send_message(message.chat.id, 'Введите пожалуйста код:')
    conn.close()
    return msg

def add_user(message):
    #print(chat_id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    langv = 'En'
    data_ = [message.chat.id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"), langv, message.from_user.first_name, message.from_user.last_name, message.from_user.username]
    cursor.execute("INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?);", data_)
    conn.commit()
    conn.close()
    return
#

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
    Amount = result_art[0][4]
    print(result_art, result_art[0][4])
    #Прочитать, что уже есть в корзине у этого покупателя

    query = "SELECT * FROM BASKET WHERE User_id = ? and Art = ?"
    cursor.execute(query, (Id, Articule))
    result = cursor.fetchall()
    if result ==[]:
        print("В корзине нет этого Артикула ", result)
        query = "INSERT INTO BASKET VALUES(?, ?, ?, ?)"
        data_ = [Id, Articule, 1, Amount]
        cursor.execute(query, data_)
        conn.commit()

    else:
        print("В корзине уже есть этот Артикул ", result[0][2])
        Kol_ = result[0][2] + 1
        query = "UPDATE BASKET SET Kol = ? WHERE Art = ?"
        data_ = [Kol_, Articule]
        cursor.execute(query, data_)
        conn.commit()
    bot.send_message(Id, "Капсулы добавлены в корзину. Вы можете продолжить выбирать товары или перейти в корзину для покупки!")
    conn.close()

def read_user(message):
     #print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
    #      'написал: ', message.text, datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S"))
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
#
def update_user(chat_id, langv):
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'UPDATE USERS SET Langv = ? WHERE User_id = ?'
    cursor.execute(query, (langv, chat_id,))
    conn.commit()
    conn.close()

def read_langv(chat_id):
    #print(chat_id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM USERS WHERE User_id = ?'
    cursor.execute(query,  (chat_id,))
    res = cursor.fetchall()  # читаем все
    result = list(res[0])[2]
    conn.commit()
    conn.close()
    return result

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

# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     #markup.row_width = 2
#     markup.add(InlineKeyboardButton("Yes", callback_data="cb_basket"))
# #                               InlineKeyboardButton("No", callback_data="cb_no"))
#     #return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    read_user(message)
    langv = read_langv(message.chat.id)
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, ' написал start')
#    save_stack(message.chat.id, 0) # сохраняем позицию для пользователя Позиция = 0
#    start_pic = 'C:\Users\Roman\Desktop\kokka\kokkasun.jpg'
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.row('Green', 'Pearl', 'Pink', 'Purple')
    start_menu.row('Violet', 'Grape', 'Gold')
    start_menu.row('Eng', 'Rus', 'Корзина')
    bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
    if langv == 'En':
        bot.send_message(message.chat.id, MESSAGES['start_message'], reply_markup=start_menu)
    elif langv == 'Ru':
        bot.send_message(message.chat.id, MESSAGES['start_message_ru'], reply_markup=start_menu)


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
#    read_user(message)
    #print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
#         ' написал help')
    langv = read_langv(message.chat.id)
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    #start_menu.add('Для лица', 'Для тела', 'Для волос')
    start_menu.row('Eng', 'Rus')
    if langv == 'En':
        bot.send_message(message.chat.id, MESSAGES['help_message'], reply_markup=start_menu)
    elif langv == 'Ru':
        bot.send_message(message.chat.id, MESSAGES['help_message_ru'], reply_markup=start_menu)

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
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.row('Blue', 'Gold', 'Green', 'Pearl')
    start_menu.row('Pink', 'Purple', 'Rose', 'Violet')
    start_menu.row('White', 'Yellow', 'Eng', 'Rus')
    #bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
    if message.text == 'Eng':
        update_user(message.chat.id, 'En')
        bot.send_message(message.chat.id, MESSAGES['start_message'], reply_markup=start_menu)
    if message.text == 'Rus':
        update_user(message.chat.id, 'Ru')
        bot.send_message(message.chat.id, MESSAGES['start_message_ru'], reply_markup=start_menu)

    langv = read_langv(message.chat.id)

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
        print(code," ", kol, " ", art, " ", photo, " ", batch, " ", data_mfg, " ", data_exp, " ", barcode, " ", bc_pic, " ", fio)
        if langv == 'En':
            bot.send_message(message.chat.id, 'Congratulations on your purchase dear friend!'+ '\n' +'Wait a moment, please, I`m checking you code...')
            msg = "Code " + code + ". Information: "
        elif langv == 'Ru':
            bot.send_message(message.chat.id, 'Поздравляем вас с покупкой!' + '\n' + 'Секундочку, я проверяю ваш код...')
            msg = "Код " + code + ". Информация: "
        time.sleep(1)
        #msg = msg + check_art(message,art)
        msg = msg + choose_mess(message, art)
        if langv == 'En':
            msg = msg + "Batch - " + batch + "\n" + "MFG - " + data_mfg + "\n" + "EXP - " + data_exp + "\n"
        elif langv == 'Ru':
            msg = msg + "Серия - " + batch + "\n" + "Произведено - " + data_mfg + "\n" + "Годен до - " + data_exp + "\n"
        bot.send_message(message.chat.id, msg)
        time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\'+ photo, 'rb'))
        time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\' + bc_pic, 'rb'))
        if kol == 1:
            time.sleep(1)
            if langv == 'En':
                msg_ = 'ATTENTION! This code is checked for the FIRST time!' + '\n' + 'No one else has seen him!' + '\n'
                msg_ = msg_ + 'Save this code to participate in the KokkaSun promotions!'
            elif langv == 'Ru':
                msg_ = 'ВНИМАНИЕ! Этот код проверяется впервые!' + '\n' + 'Никто не вводил его до вас!' + '\n' + 'Поздравляем вас с приобретением оригинального продукта КоккаSun.' + '\n'
                msg_ = msg_ + 'Сохраните этот код для дальнейшего участия в акциях КоккаSun!'
            bot.send_message(message.chat.id, msg_)
        else:
            time.sleep(1)
            if langv == 'En':
                bot.send_message(message.chat.id, "The code was checked " + str(kol) + " times")
            elif langv == 'Ru':
                bot.send_message(message.chat.id, "Код был проверен " + str(kol) + " раз")
    else:
        #print("прошел")
        check_art(message, message.text)

if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
