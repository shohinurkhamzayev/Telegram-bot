import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# Render env variables
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID", "8170632684")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Paketlar narxlari
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
    "stars_750": {"name": "750 ⭐", "price": "176 500 so'm"},
    "stars_1000": {"name": "1000 ⭐", "price": "234 500 so'm"},
    "stars_1500": {"name": "1500 ⭐", "price": "350 500 so'm"},
    "stars_2500": {"name": "2500 ⭐", "price": "580 500 so'm"},
    "stars_10000": {"name": "10000 ⭐", "price": "2 300 000 so'm"},
    "stars_25000": {"name": "25000 ⭐", "price": "5 800 000 so'm"},
}

# Asosiy menyu
def main_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Akkountga kirib", callback_data="account")],
        [InlineKeyboardButton("🎁 Sovg‘a sifatida", callback_data="gift")],
        [InlineKeyboardButton("⭐ Stars xizmatlar", callback_data="stars")],
        [InlineKeyboardButton("❓ Premium bot ishlamasa", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 Admin bilan aloqa", url=f"tg://user?id={8170632684}")],
    ]
    return InlineKeyboardMarkup(keyboard)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum!\nPremium xizmatlarni tanlang 👇",
        reply_markup=main_menu()
    )


# Callback handler
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "account":
        keyboard = [
            [InlineKeyboardButton("1 oylik Premium", callback_data="plan_1")],
            [InlineKeyboardButton("12 oylik Premium", callback_data="plan_12")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")],
        ]
        await query.edit_message_text("Akkount muddati tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "gift":
        keyboard = [
            [InlineKeyboardButton("3 oylik", callback_data="gift_3")],
            [InlineKeyboardButton("6 oylik", callback_data="gift_6")],
            [InlineKeyboardButton("12 oylik", callback_data="gift_12")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")],
        ]
        await query.edit_message_text("Sovg‘a muddati tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "stars":
        keyboard = [
            [InlineKeyboardButton("100 ⭐", callback_data="stars_100"),
             InlineKeyboardButton("150 ⭐", callback_data="stars_150")],
            [InlineKeyboardButton("250 ⭐", callback_data="stars_250"),
             InlineKeyboardButton("350 ⭐", callback_data="stars_350")],
            [InlineKeyboardButton("500 ⭐", callback_data="stars_500"),
             InlineKeyboardButton("750 ⭐", callback_data="stars_750")],
            [InlineKeyboardButton("1000 ⭐", callback_data="stars_1000"),
             InlineKeyboardButton("1500 ⭐", callback_data="stars_1500")],
            [InlineKeyboardButton("2500 ⭐", callback_data="stars_2500"),
             InlineKeyboardButton("10000 ⭐", callback_data="stars_10000")],

[InlineKeyboardButton("25000 ⭐", callback_data="stars_25000")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")],
        ]
        await query.edit_message_text("Stars paketini tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data in PLANS:
        plan = PLANS[data]
        await query.edit_message_text(
            f"✅ Siz tanladingiz: *{plan['name']}*\n"
            f"💵 Narxi: *{plan['price']}*\n\n"
            "ℹ️ To‘lov uchun karta: `8600 XXXX XXXX XXXX`\n"
            "Chekni yuboring va 1-2 daqiqa kuting, admin tasdiqlaydi.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📤 Chekni yubordim", callback_data="check_sent")],
                 [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]]
            ),
        )

    elif data == "check_sent":
        await query.edit_message_text(
            "⏳ Chek yuborildi. 1-2 daqiqa kuting, admin tekshiradi.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_main")]]
            ),
        )

    elif data == "help":
        await query.edit_message_text(
            "Agar bot ishlamay qolsa 👨‍💻 Admin bilan bog‘laning.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("👨‍💻 Admin bilan aloqa", url=f"https://t.me/{ADMIN_USERNAME}")],
                 [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]]
            ),
        )

    elif data == "back_main":
        await query.edit_message_text("Asosiy menyu:", reply_markup=main_menu())


def main():
    # Render uchun polling ishlatiladi (background worker sifatida)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.run_polling()


if __name__ == "__main__":
    main()