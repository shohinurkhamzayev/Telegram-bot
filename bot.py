import telebot
from telebot import types

# 🔑 O'zingizning tokeningizni qo'ying
TOKEN = "8242321867:AAFaYuwFFuwLIasPD5WbPlnaAGnFANGvHXU"
ADMIN_CHAT_ID = 8170632684 # O'zingizning Telegram ID'ingiz

bot = telebot.TeleBot(TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💎 Telegram Premium", callback_data="premium")
    btn2 = types.InlineKeyboardButton("💳 To'lovlar", callback_data="tolovlar")
    btn3 = types.InlineKeyboardButton("👨‍💻 Admin bilan bog'lanish", callback_data="admin")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id,
                     "Assalomu alaykum! Botga xush kelibsiz 👋\nQuyidagi bo‘limlardan birini tanlang:",
                     reply_markup=markup)

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = call.from_user
    user_name = user.username or f"{user.first_name or ''} {user.last_name or ''}".strip()
    user_id = user.id

    if call.data == "premium":
        markup = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton("1️⃣ 1 oy – 30 000 so'm", callback_data="premium1")
        three = types.InlineKeyboardButton("3️⃣ 3 oy – 85 000 so'm", callback_data="premium3")
        twelve = types.InlineKeyboardButton("📅 12 oy – 300 000 so'm", callback_data="premium12")
        markup.add(one, three, twelve)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="💎 Premium variantlari:",
                              reply_markup=markup)

    elif call.data == "tolovlar":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="💳 To‘lov usullari:\n\nHamkor bank: 9860 1606 5188 8820")

    elif call.data == "admin":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="👨‍💻 Admin bilan bog‘lanish: @shoh1nur_khamzayev")

    # --- Premium sotib olish tugmalari ---
    elif call.data in ["premium1", "premium3", "premium12"]:
        plans = {
            "premium1": "1️⃣ 1 oylik Premium",
            "premium3": "3️⃣ 3 oylik Premium",
            "premium12": "📅 12 oylik Premium"
        }
        plan = plans[call.data]

        # Foydalanuvchiga javob
        bot.send_message(call.message.chat.id,
                         f"✅ So‘rovingiz qabul qilindi!\nSiz {plan} tanladingiz.\nAdmin tez orada tasdiqlaydi.")

        # Adminga xabar + Tasdiqlash tugmasi
        markup = types.InlineKeyboardMarkup()
        approve = types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}")
        markup.add(approve)

        bot.send_message(ADMIN_CHAT_ID,
                         f"📥 Yangi Premium so‘rovi:\n\n"
                         f"{plan}\n"
                         f"👤 Foydalanuvchi: {user_name} (@{user.username})\n"
                         f"🆔 ID: {user_id}\n"
                         f"💬 Chat ID: {call.message.chat.id}",
                         reply_markup=markup)

    # Admin tasdiqlaganda
    elif call.data.startswith("approve_"):
        user_id = int(call.data.split("_")[1])
        bot.send_message(user_id, "🎉 Premiumingiz faollashtirildi! Rahmat!")
        bot.answer_callback_query(call.id, "✅ Foydalanuvchiga Premium tasdiqlandi.")

# Ishga tushirish
if __name__ == "__main__":
    print("Bot ishlamoqda...")
    bot.polling(non_stop=True)