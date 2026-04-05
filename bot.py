import telebot
from src.client import BOT_TOKEN
from src.rag import ask_question

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Hello! I'm a Document Q&A Bot.\n\n"
        "Just send me any question and I'll answer it "
        "using the uploaded document.\n\n"
        "Example: *What is artificial intelligence?*",
        parse_mode="Markdown",
    )


@bot.message_handler(func=lambda message: True)
def handle_question(message):
    # Show "typing..." while processing
    bot.send_chat_action(message.chat.id, "typing")

    answer = ask_question(message.text)
    bot.reply_to(message, answer, parse_mode="Markdown")


if __name__ == "__main__":
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    bot.infinity_polling()