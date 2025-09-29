import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment variables
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")  # Default admin ID

bot = telebot.TeleBot(TOKEN)

# Paketlar va narxlari
PLANS = {
    "plan_1": {"name": "1 oylik Premium", "price": "40 000 so'm"},
    "plan_12": {"name": "12 oylik Premium", "price": "275 000 so'm"},
    "gift_3": {"name": "Sovg‘a 3 oylik", "price": "160 000 so'm"},
    "gift_6": {"name": "Sovg‘a 6 oylik", "price": "215 000 so'm"},
    "gift_12": {"name": "Sovg‘a 12 oylik", "price": "385 000 so'm"},
    "stars_100": {"name": "100 ⭐", "price": "26 000 so'm"},
    "stars_150": {"name": "150 ⭐", "price": "37 500 so'm"},
    "stars_250": {"name": "250 ⭐", "price": "60 500 so'm"},
    "stars_350": {"name": "350 ⭐", "price": "84 500 so'm"},
    "stars_500": {"name": "500 ⭐", "price": "118 500 so'm"},
}

# Asosiy menyu
def main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("👤 Akkountga kirib", callback_data="account"))
    keyboard.add(InlineKeyboardButton("🎁 Sovg‘a sifatida", callback_data="gift"))
    keyboard.add(InlineKeyboardButton("⭐ Stars xizmatlar", callback_data="stars"))
    keyboard.add(InlineKeyboardButton("❓ Premium bot ishlamasa", callback_data="help"))
    keyboard.add(InlineKeyboardButton("👨‍💻 Admin bilan aloqa", url=f"tg://user?id={ADMIN_ID}"))
    return keyboard

# /start handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\nPremium xizmatlarni tanlang 👇",
        reply_markup=main_menu()
    )

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    data = call.data

    if data == "account":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("1 oylik Premium", callback_data="plan_1"))
        keyboard.add(InlineKeyboardButton("12 oylik Premium", callback_data="plan_12"))
        keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        bot.edit_message_text("Akkount muddati tanlang:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif data == "gift":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("3 oylik", callback_data="gift_3"))
        keyboard.add(InlineKeyboardButton("6 oylik", callback_data="gift_6"))
        keyboard.add(InlineKeyboardButton("12 oylik", callback_data="gift_12"))
        keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        bot.edit_message_text("Sovg‘a muddati tanlang:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif data == "stars":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("100 ⭐", callback_data="stars_100"))
        keyboard.add(InlineKeyboardButton("150 ⭐", callback_data="stars_150"))
        keyboard.add(InlineKeyboardButton("250 ⭐", callback_data="stars_250"))
        keyboard.add(InlineKeyboardButton("350 ⭐", callback_data="stars_350"))
        keyboard.add(InlineKeyboardButton("500 ⭐", callback_data="stars_500"))
        keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        bot.edit_message_text("Stars paketini tanlang:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif data in PLANS:
        plan = PLANS[data]
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📤 Chekni yubordim", callback_data="check_sent"))
        keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        bot.edit_message_text(
            f"✅ Siz tanladingiz: {plan['name']}\n💵 Narxi: {plan['price']}\n\n"
            "ℹ️ To‘lov uchun karta: `8600 XXXX XXXX XXXX`\nChekni yuboring va 1-2 daqiqa kuting, admin tasdiqlaydi.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    elif data == "check_sent":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_main"))
        bot.edit_message_text(
            "⏳ Chek yuborildi. 1-2 daqiqa kuting, admin tekshiradi.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif data == "help":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("👨‍💻 Admin bilan aloqa", url=f"tg://user?id={ADMIN_ID}"))
        keyboard.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        bot.edit_message_text(
            "Agar bot ishlamay qolsa 👨‍💻 Admin bilan bog‘laning.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif data == "back_main":
        bot.edit_message_text("Asosiy menyu:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())

# Botni ishga tushurish
bot.infinity_polling()