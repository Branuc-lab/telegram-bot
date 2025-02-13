import telebot

TOKEN = "7949486941:AAFFv7A4fxvdvnhyvSzYqUwA2Um92BDAMbg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salut ! Je suis ton bot Telegram 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

print("✅ Bot en ligne...")

bot.polling()
