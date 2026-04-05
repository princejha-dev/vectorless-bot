import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.client import BOT_TOKEN, DOC_ID
from src.rag import ask_question
from src.chat_api import ask_chat_api

bot = telebot.TeleBot(BOT_TOKEN)

# Store each user's chosen mode: "rag" or "chat_api"
user_mode = {}


def safe_reply(message, text):
    """Try sending with Markdown; fall back to plain text if it fails."""
    try:
        bot.reply_to(message, text, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, text)


# ── /start and /help ─────────────────────────────────────────────────────────
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Hello! I'm your *Academic Regulations 2025* Assistant.\n\n"
        "Ask me anything about academic rules, policies, "
        "grading, attendance, exams, and more!\n\n"
        "Use /mode to choose how I answer:\n"
        "• *RAG* — Groq LLM + document tree search (fast)\n"
        "• *Chat API* — PageIndex direct answer (detailed)\n\n"
        "Just type your question and send!",
        parse_mode="Markdown",
    )


# ── /mode — pick answer mode ─────────────────────────────────────────────────
@bot.message_handler(commands=["mode"])
def choose_mode(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🤖 RAG (Fast)", callback_data="mode_rag"),
        InlineKeyboardButton("⚡ Chat API (Detailed)", callback_data="mode_chat_api"),
    )
    current = user_mode.get(message.chat.id, "rag")
    label = "RAG (Fast)" if current == "rag" else "Chat API (Detailed)"
    bot.reply_to(
        message,
        f"Current mode: *{label}*\n\nChoose your answer mode:",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def handle_mode_callback(call):
    if call.data == "mode_rag":
        user_mode[call.message.chat.id] = "rag"
        bot.answer_callback_query(call.id, "✅ Switched to RAG mode")
        bot.edit_message_text(
            "✅ Mode set to *RAG (Fast)*\n\nSend me your question!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
        )
    elif call.data == "mode_chat_api":
        user_mode[call.message.chat.id] = "chat_api"
        bot.answer_callback_query(call.id, "✅ Switched to Chat API mode")
        bot.edit_message_text(
            "✅ Mode set to *Chat API (Detailed)*\n\nSend me your question!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
        )


# ── Handle questions ─────────────────────────────────────────────────────────
@bot.message_handler(func=lambda message: True)
def handle_question(message):
    bot.send_chat_action(message.chat.id, "typing")

    mode = user_mode.get(message.chat.id, "rag")

    if mode == "chat_api":
        answer = ask_chat_api(message.text, DOC_ID)
    else:
        answer = ask_question(message.text)

    safe_reply(message, answer)


if __name__ == "__main__":
    print("🤖 Academic Regulations Bot is running... Press Ctrl+C to stop.")
    bot.infinity_polling()