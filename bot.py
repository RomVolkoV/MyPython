import telebot
import sqlite3
import time
import datetime
from mess import MESSAGES
from telebot.types import LabeledPrice, ShippingOption

bot_token = '1833545970:AAG9lOO9PZ8Yur3gu--N8GTcQkNc4ALg8dI'
ukassa_token = '381764678:TEST:30583'
prices = [LabeledPrice(label='KokkaSun capsules', amount=750), LabeledPrice('Gift wrapping', 500)]
shipping_options = [
    ShippingOption(id='instant', title='KokkaSun capsules').add_price(LabeledPrice('Capsules', 900)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

bot = telebot.TeleBot(bot_token)

def chose_mess(message, Art_of_capsules):
    msg = ""
    langv = read_langv(message.chat.id)
    if langv == 'En':
        msg = msg + "\n" + MESSAGES[Art_of_capsules] + "\n"
    elif langv == 'Ru':
        msg = msg + "\n" + MESSAGES[Art_of_capsules] + "\n"
    return msg

def check_art(message, Art_of_capsules):
    print("Art_of_capsules = ", Art_of_capsules)
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
            msg = MESSAGES[Art_of_capsules] + "\n"
        elif langv == 'Ru':
            msg = MESSAGES[Art_of_capsules + '_ru'] + "\n"
        bot.send_message(message.chat.id, msg)
        bot.send_photo(message.chat.id, open('pic\\' + list(result[0])[1], 'rb'))
        time.sleep(1)
        bot.send_photo(message.chat.id, open('pic\\' + list(result[0])[3], 'rb'))
    else:
        if langv == 'En':
            bot.send_message(message.chat.id, 'Enter the code please:')
        if langv == 'Ru':
            bot.send_message(message.chat.id, 'Введите пожалуйста код:')
            #print("Нет такого цвета!")

    #conn.commit()
    conn.close()

    return

def add_user(message):
    #print(chat_id)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    langv = 'En'
    data_ = [message.chat.id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"), langv, message.from_user.first_name, message.from_user.last_name, message.from_user.username]
    cursor.execute("INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?);", data_)
    #cursor.execute(query, (chat_id))
    #result = cursor.fetchall()  # читаем все
    conn.commit()
    conn.close()
    return
#
def read_user(message):
    #for item in message:
    #    print(item.text)
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
#    print(text)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM CODE_TAB WHERE Code = ?'
    cursor.execute(query, (text,))
    res = cursor.fetchall()  # читаем все
    conn.close()
    if res:
        kol = list(res[0])[1]
        #print(kol, type(kol))
        kol += 1
        conn = sqlite3.connect(r'db/kokka.db')
        cursor = conn.cursor()
        query = 'UPDATE CODE_TAB SET Count = ? WHERE Code = ?'
        cursor.execute(query, (kol, text,))
        conn.commit()
        conn.close()
#    print(res)
    conn = sqlite3.connect(r'db/kokka.db')
    cursor = conn.cursor()
#    print(text, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"))
    data_ = [text, message.from_user.id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")]
    cursor.execute("INSERT INTO USER_TAB VALUES(?, ?, ?);", data_)
    conn.commit()
    conn.close()
    return (res)

# @bot.message_handler(commands=['start'])
# def command_start(message):
#     bot.send_message(message.chat.id,
#                      "Hello, I'm the demo merchant bot."
#                      " I can sell you a Time Machine."
#                      " Use /buy to order one, /terms for Terms and Conditions")

@bot.message_handler(commands=['start'])
def start_message(message):
    read_user(message)
    langv = read_langv(message.chat.id)
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, ' написал start')
#    save_stack(message.chat.id, 0) # сохраняем позицию для пользователя Позиция = 0
#    start_pic = 'C:\Users\Roman\Desktop\kokka\kokkasun.jpg'
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.add('Blue', 'Gold', 'Green', 'Pearl', 'Pink', 'Purple', 'Rose', 'Violet', 'White', 'Yellow')
    start_menu.row('English', 'Russian')
    bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
    if langv == 'En':
        bot.send_message(message.chat.id, MESSAGES['start_message'], reply_markup=start_menu)
    elif langv == 'Ru':
        bot.send_message(message.chat.id, MESSAGES['start_message_ru'], reply_markup=start_menu)

@bot.message_handler(commands=['terms'])
def process_terms_command(message):
#    read_user(message)
    bot.send_message(message.chat.id, MESSAGES['terms'])
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
          ' написал terms')


@bot.message_handler(commands=['help'])
def help_message(message):
#    read_user(message)
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username,
          ' написал help')
#    langv = read_langv(message.chat.id)
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.add('Blue', 'Gold', 'Green', 'Pearl', 'Pink', 'Purple', 'Rose', 'Violet', 'White', 'Yellow')
    start_menu.row('English', 'Russian')
    #start_menu.add('Blue','Gold','Green','Pearl','Pink','Purple', 'Rose', 'Violet', 'White','Yellow')
    #bot.send_message(message.chat.id, MESSAGES['help_message'])
    # if langv == 'En':
    #     bot.send_message(message.chat.id, MESSAGES['help_message'], reply_markup=start_menu)
    # elif langv == 'Ru':
    bot.send_message(message.chat.id, MESSAGES['help_message_ru'], reply_markup=start_menu)

@bot.message_handler(commands=['pay'])
def process_buy_command(message):
    if ukassa_token.split(':')[1] == 'TEST':
        bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'], parse_mode='Markdown')
        print(ukassa_token)

        #bot.send_invoice()
    bot.send_invoice(message.chat.id,
                           title = 'title', #MESSAGES['tm_title'],
                           description = 'descr', #MESSAGES['tm_description'],
                           provider_token = ukassa_token,
                           currency = 'RUB',
                           #photo_url=TIME_MACHINE_IMAGE_URL,
                           #photo_height=512,  # !=0/None, иначе изображение не покажется
                           #photo_width=512,
                           #photo_size=512,
                           is_flexible = False,  # True если конечная цена зависит от способа доставки
                           prices = prices,
                           start_parameter = 'time-machine-example',
                           invoice_payload = '12345')

# @bot.message_handler(commands=['buy'])
# def command_pay(message):
#     bot.send_message(message.chat.id,
#                      "Real cards won't work with me, no money will be debited from your account."
#                      " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
#                      "\n\nThis is your demo invoice:", parse_mode='Markdown')
#     bot.send_invoice(message.chat.id, title='Working Time Machine',
#                      description='Want to visit your great-great-great-grandparents?'
#                                  ' Make a fortune at the races?'
#                                  ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
#                                  ' Order our Working Time Machine today!',
#                      provider_token=ukassa_token,
#                      currency='RUB',
#                      #photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
#                      #photo_height=512,  # !=0/None or picture won't be shown
#                      #photo_width=512,
#                      #photo_size=512,
#                      is_flexible=False,  # True If you need to set up Shipping Fee
#                      prices=prices,
#                      start_parameter='time-machine-example',
#                      invoice_payload='HAPPY FRIDAYS COUPON')

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
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


@bot.message_handler(content_types = ['text'])
def send_text(message):
    print(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 'написал: ', message.text,datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S"))
    read_user(message)
    start_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    start_menu.add('Blue', 'Gold', 'Green', 'Pearl', 'Pink', 'Purple', 'Rose', 'Violet', 'White', 'Yellow')
    start_menu.row('English', 'Russian')
    bot.send_photo(message.chat.id, open('pic\\kokkasun.png', 'rb'))
    if message.text == 'English':
        update_user(message.chat.id, 'En')
        bot.send_message(message.chat.id, MESSAGES['start_message'], reply_markup=start_menu)
    if message.text == 'Russian':
        update_user(message.chat.id, 'Ru')
        bot.send_message(message.chat.id, MESSAGES['start_message_ru'], reply_markup=start_menu)

    langv = read_langv(message.chat.id)

    result = check_code(message, message.text)
    print(result, len(result))
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
        time.sleep(3)
        msg = msg + chose_mess(message, art)
        if langv == 'En':
            msg = msg + "Batch - " + batch + "\n" + "MFG - " + data_mfg + "\n" + "EXP - " + data_exp + "\n"
        elif langv == 'Ru':
            msg = msg + "Серия - " + batch + "\n" + "Произведено - " + data_mfg + "\n" + "Годен до - " + data_exp + "\n"
        bot.send_message(message.chat.id, msg)
        time.sleep(2)
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
            #bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAMfX6l2gHwi4oltB9tGTRbqo8jzr3sAAhQAA8A2TxOtZZnkuTD2Ph4E')
        #else:
        #    bot.send_message(message.chat.id, "The code was checked more than 10 times")
#             #bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMfX6l2gHwi4oltB9tGTRbqo8jzr3sAAhQAA8A2TxOtZZnkuTD2Ph4E')
# #-------------------------------------------
#     elif message.text.lower() == 'pearl' or message.text.lower() == 'pear' or message.text.lower() == 'pea' or message.text.lower() == 'pe'\
#             or message.text.lower() == 'perl' or message.text.lower() == 'per':
#         if langv == 'En':
#             msg = MESSAGES['Pearl'] + "\n"
#         elif langv == 'Ru':
#             msg =  MESSAGES['Pearl_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'pearl.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436638.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'purple' or message.text.lower() == 'purpl' or message.text.lower() == 'purp' or message.text.lower() == 'pur' or message.text.lower() == 'pu':
#         if langv == 'En':
#             msg = MESSAGES['Purple'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Purple_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'purple.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436652.png', 'rb'))
# # -------------------------------------------




#     elif message.text.lower() == 'pink' or message.text.lower() == 'pin' or message.text.lower() == 'pi':
#         if langv == 'En':
#             msg = MESSAGES['Pink'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Pink_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'pink.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436669.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'gold' or message.text.lower() == 'gol' or message.text.lower() == 'go':
#         if langv == 'En':
#             msg = MESSAGES['Gold'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Gold_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'gold.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436645.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'green' or message.text.lower() == 'gree' or message.text.lower() == 'gre' or message.text.lower() == 'gr':
#         if langv == 'En':
#             msg = MESSAGES['Green'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Green_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'green.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436676.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'white' or message.text.lower() == 'whit' or message.text.lower() == 'whi' or message.text.lower() == 'wh' or message.text.lower() == 'w':
#         if langv == 'En':
#             msg = MESSAGES['White'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['White_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         # bot.send_photo(message.chat.id, open('pic\\' + 'white.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436683.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'blue' or message.text.lower() == 'blu' or message.text.lower() == 'bl' or message.text.lower() == 'b':
#         if langv == 'En':
#             msg = MESSAGES['Blue'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Blue_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'blue.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436744.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'yellow' or message.text.lower() == 'yello' or message.text.lower() == 'yell'\
#             or message.text.lower() == 'yel' or message.text.lower() == 'ye' or message.text.lower() == 'y':
#         if langv == 'En':
#             msg = MESSAGES['Yellow'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Yellow_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'yellow.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436751.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'violet' or message.text.lower() == 'viole' or message.text.lower() == 'viol' \
#              or message.text.lower() == 'vio' or message.text.lower() == 'vi' or message.text.lower() == 'v':
#         if langv == 'En':
#             msg = MESSAGES['Violet'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Violet_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         bot.send_photo(message.chat.id, open('pic\\' + 'violet.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436768.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'rose' or message.text.lower() == 'ros' or message.text.lower() == 'ro':
#         if langv == 'En':
#             msg = MESSAGES['Rose'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Rose_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         #bot.send_photo(message.chat.id, open('pic\\' + 'rose.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436737.png', 'rb'))
# # -------------------------------------------
#     elif message.text.lower() == 'red' or message.text.lower() == 're':
#         if langv == 'En':
#             msg = MESSAGES['Red'] + "\n"
#         elif langv == 'Ru':
#             msg = MESSAGES['Red_ru'] + "\n"
#         bot.send_message(message.chat.id, msg)
#         # bot.send_photo(message.chat.id, open('pic\\' + 'red.jpg', 'rb'))
#         time.sleep(1)
#         bot.send_photo(message.chat.id, open('pic\\' + '8803720436737.png', 'rb'))
# # -------------------------------------------
#
    else:
        print("прошел")
        check_art(message, message.text)

#
#
#


# bot.skip_pending = True
# bot.polling(none_stop=True)
bot.polling()