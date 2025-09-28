import telebot
import os
from telebot.types import ReplyKeyboardMarkup

# Environment variables
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)

# Oddiy DB
users = {}
otzivlar = []

# ---------- Menyular ----------

def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Premium xizmatlar", "Stars xizmatlar")
    markup.row("Admin bilan aloqa", "Otzivlar")
    return markup

def premium_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("1 oy - 40.000 so'm", "12 oy - 278.000 so'm")
    markup.row("Ortga")
    return markup

def gift_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("3 oy - 162.000 so'm", "6 oy - 215.000 so'm", "12 oy - 385.000 so'm")
    markup.row("Ortga")
    return markup

def stars_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⭐100", "⭐150", "⭐250")
    markup.row("⭐350", "⭐500", "⭐750")
    markup.row("⭐1000", "⭐1500", "⭐2500")
    markup.row("⭐5000", "⭐10000")
    markup.row("Ortga")
    return markup

def otziv_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Otziv qoldirish")
    markup.row("Ortga")
    return markup

# ---------- Narxlar ----------

stars_prices = {
    "⭐100": "26.000 so'm",
    "⭐150": "38.000 so'm",
    "⭐250": "61.000 so'm",
    "⭐350": "85.000 so'm",
    "⭐500": "119.000 so'm",
    "⭐750": "177.000 so'm",
    "⭐1000": "235.000 so'm",
    "⭐1500": "351.000 so'm",
    "⭐2500": "581.000 so'm",
    "⭐5000": "1.161.000 so'm",
    "⭐10000": "2.300.000 so'm"
}

premium_prices = {
    "1 oy - 40.000 so'm": "40.000 so'm",
    "12 oy - 278.000 so'm": "278.000 so'm"
}

gift_prices = {
    "3 oy - 162.000 so'm": "162.000 so'm",
    "6 oy - 215.000 so'm": "215.000 so'm",
    "12 oy - 385.000 so'm": "385.000 so'm"
}

# ---------- To'lov info ----------

def tolov_info(price):
    return f"""
Karta raqami: 8600 XXXX XXXX XXXX
Karta egasi: Shohinur Khamzayev
Ulangan raqam: +998901234567
To‘lov summasi: {price}

❗️ Chekni olishni unutmang
"""

# ---------- Start ----------

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Asosiy menyuga xush kelibsiz!", reply_markup=main_menu_markup())

# ---------- Menyularni boshqarish ----------

@bot.message_handler(func=lambda m: True)
def menu(message):
    chat_id = message.chat.id
    text = message.text

    # Asosiy menyu
    if text == "Premium xizmatlar":
        bot.send_message(chat_id, "Premium variantni tanlang:", reply_markup=premium_menu_markup())
    elif text == "Stars xizmatlar":
        bot.send_message(chat_id, "Stars paketini tanlang:", reply_markup=stars_menu_markup())
    elif text == "Admin bilan aloqa":
        bot.send_message(chat_id, "Iltimos faqat zarur bo‘lsa bezovta qiling\nhttps://t.me/shoh1nur_khamzayev")
    elif text == "Otzivlar":
        if otzivlar:
            msgs = "\n\n".join([f"Anonim: {o}" for o in otzivlar])
            bot.send_message(chat_id, msgs, reply_markup=otziv_menu_markup())
        else:
            bot.send_message(chat_id, "Hali otzivlar yo‘q", reply_markup=otziv_menu_markup())

    # Premium
    elif text in premium_prices:
        price = premium_prices[text]
        bot.send_message(chat_id, tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "account_premium", "price": price}

    # Sovg'a Premium
    elif text in gift_prices:
        price = gift_prices[text]
        bot.send_message(chat_id, tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "gift_premium", "price": price}

    # Stars
    elif text in stars_prices:
        price = stars_prices[text]
        bot.send_message(chat_id, f"{text} paketi tanlandi.\n\n" + tolov_info(price))
        bot.send_message(chat_id, "To‘lovni tasdiqlash tugmasini bosing /sendcheck")
        users[chat_id] = {"type": "stars", "price": price}

    # Ortga
    elif text == "Ortga":
        bot.send_message(chat_id, "Asosiy menyu:", reply_markup=main_menu_markup())
    # Otziv qoldirish
    elif text == "Otziv qoldirish":
        bot.send_message(chat_id, "Iltimos, fikringizni yozing:")
        users[chat_id] = {"type": "otziv"}

# ---------- Chek yuborish ----------

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
        bot.send_message(chat_id, "To‘lov tasdiqlandi. Keyingi qadamni kuting ✅")
        users.pop(chat_id)

# ---------- Otzivlar ----------

@bot.message_handler(func=lambda m: True)
def follow_up(message):
    chat_id = message.chat.id
    if chat_id not in users: return
    if users[chat_id].get("type") == "otziv":
        otzivlar.append(message.text)
        bot.send_message(chat_id, "Otzivingiz qabul qilindi, rahmat ✅")
        users.pop(chat_id)

# ---------- Polling bilan ishga tushirish ----------

if __name__ == "__main__":
    print("Bot polling bilan ishga tushdi...")
    bot.infinity_polling(skip_pending=True)