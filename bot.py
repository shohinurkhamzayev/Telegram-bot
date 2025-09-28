import telebot
from flask import Flask, request
import os

# Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Oddiy DB
users = {}
otzivlar = []

# Menyular
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row("Premium xizmatlar", "Stars xizmatlar")
main_menu.row("Admin bilan aloqa", "Otzivlar")

premium_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
premium_menu.row("1 oy - 40.000 so'm", "12 oy - 278.000 so'm")
premium_menu.row("Ortga")

gift_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
gift_menu.row("3 oy - 162.000 so'm", "6 oy - 215.000 so'm", "12 oy - 385.000 so'm")
gift_menu.row("Ortga")

stars_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
stars_menu.row("⭐100", "⭐200", "⭐500")
stars_menu.row("⭐1000", "⭐5000", "⭐10000")
stars_menu.row("Ortga")

contact_admin = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
contact_admin.row("Admin bilan aloqa")
contact_admin.row("Ortga")

otziv_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
otziv_menu.row("Otziv qoldirish")
otziv_menu.row("Ortga")

# To'lov ma'lumotlari
def tolov_info(price):
    return f"""
Karta raqami: 8600 XXXX XXXX XXXX
Karta egasi: Shohinur Khamzayev
Ulangan raqam: +998901234567
To‘lov summasi: {price}

❗️ Chekni olishni unutmang
"""

# Start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Asosiy menyuga xush kelibsiz!", reply_markup=main_menu)

# Asosiy menyu va variantlar
@bot.message_handler(func=lambda m: True)
def menu(message):
    chat_id = message.chat.id
    text = message.text

    # Asosiy menyu
    if text == "Premium xizmatlar":
        bot.send_message(chat_id, "Premium variantni tanlang:", reply_markup=premium_menu)
    elif text == "Stars xizmatlar":
        bot.send_message(chat_id, "Stars paketini tanlang:", reply_markup=stars_menu)
    elif text == "Admin bilan aloqa":
        bot.send_message(chat_id, "Iltimos faqat zarur bo‘lsa bezovta qiling\nhttps://t.me/shoh1nur_khamzayev")
    elif text == "Otzivlar":
        if otzivlar:
            msgs = "\n\n".join([f"Anonim: {o}" for o in otzivlar])
            bot.send_message(chat_id, msgs, reply_markup=otziv_menu)
        else:
            bot.send_message(chat_id, "Hali otzivlar yo‘q", reply_markup=otziv_menu)

    # Premium variantlar
    elif text in ["1 oy - 40.000 so'm", "12 oy - 278.000 so'm"]:
        price = text.split("-")[1].strip()
        bot.send_message(chat_id, tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "account_premium", "price": price}

    # Sovg'a Premium
    elif text in ["3 oy - 162.000 so'm", "6 oy - 215.000 so'm", "12 oy - 385.000 so'm"]:
        price = text.split("-")[1].strip()
        bot.send_message(chat_id, tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "gift_premium", "price": price}

    # Stars
    elif text in ["⭐100", "⭐200", "⭐500", "⭐1000", "⭐5000", "⭐10000"]:
        price = text.split(" ")[1]
        bot.send_message(chat_id, tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "stars", "price": price}

    # Ortga
    elif text == "Ortga":
        bot.send_message(chat_id, "Asosiy menyu:", reply_markup=main_menu)
    # Otziv qoldirish
    elif text == "Otziv qoldirish":
        bot.send_message(chat_id, "Iltimos, fikringizni yozing:")
        users[chat_id] = {"type": "otziv"}

# Chek yuborish
@bot.message_handler(commands=['sendcheck'])
def sendcheck(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Iltimos, to‘lov chekini rasm yoki PDF shaklida yuboring.")

@bot.message_handler(content_types=['photo', 'document'])
def check_handler(message):
    chat_id = message.chat.id
    if chat_id in users:
        user_data = users[chat_id]
        user_type = user_data.get("type")
        bot.send_message(ADMIN_ID, f"Foydalanuvchi {chat_id} {user_type} to‘lov chekini yubordi: {user_data.get('price','')}")
        if user_type == "account_premium":
            bot.send_message(chat_id, "To‘lov tasdiqlandi. Endi Premium olmoqchi bo‘lgan Telegram akkauntingizni telefon raqamini +998 XX XXX XX XX formatda yuboring.")
            users[chat_id]["step"] = "await_phone"
        elif user_type in ["gift_premium", "stars"]:
            bot.send_message(chat_id, "To‘lov tasdiqlandi. Endi username ni yuboring (masalan: @username)")
            users[chat_id]["step"] = "await_username"
        else:
            bot.send_message(chat_id, "Chek adminga yuborildi, tasdiqlanishini kuting ✅")

# Telefon raqam va username qabul qilish
@bot.message_handler(func=lambda m: True)
def follow_up(message):
    chat_id = message.chat.id
    if chat_id not in users: return
    step = users[chat_id].get("step")

    if step == "await_phone":
        users[chat_id]["phone"] = message.text
        bot.send_message(chat_id, "Rahmat! Endi Telegram’dan borgan kodni shu ko‘rinishda yuboring: 12.345")
        users[chat_id]["step"] = "await_code"
    elif step == "await_code":
        users[chat_id]["code"] = message.text
        bot.send_message(ADMIN_ID, f"Foydalanuvchi {chat_id} kodi yubordi: {message.text}")
        bot.send_message(chat_id, "Xaridingiz uchun rahmat! Premiumingiz faollashdi 🎉\nKeyingi xaridingizni kutib qolamiz.")
        users.pop(chat_id)
    elif step == "await_username":
        users[chat_id]["username"] = message.text
        bot.send_message(ADMIN_ID, f"Foydalanuvchi {chat_id} username yubordi: {message.text}")
        bot.send_message(chat_id, "Sovg‘a/Stars faollashdi ✅")
        users.pop(chat_id)
    elif users[chat_id].get("type") == "otziv":
        otzivlar.append(message.text)
        bot.send_message(chat_id, "Otzivingiz qabul qilindi, rahmat ✅")
        users.pop(chat_id)

# Flask webhook
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "ok", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://YOUR_RENDER_APP_URL/" + TOKEN)
    return "Webhook set", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))