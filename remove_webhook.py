import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # Tokenni Environment Variable sifatida qo'y
bot = telebot.TeleBot(TOKEN)

# Webhookni o'chirish
bot.remove_webhook()
print("✅ Webhook o'chirildi, endi polling ishlashi mumkin")