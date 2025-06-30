from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

BOT_TOKEN = "8031570942:AAGAK2QzgSfJ132zBNFO8OsD__Z-kC9Qmyg"
ADMIN_ID = 8031570942  # твой Telegram ID

# Этапы формы
NAME, CONTACT, MESSAGE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот Su Jok Assistant 🤲🌿\n\n"
                                    "Команды:\n"
                                    "/feedback — оставить сообщение\n"
                                    "/pay — перейти к оплате")

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💳 Оплатить", url="https://forms.gle/BMAPZ8WQYiQxP3fL6")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите кнопку, чтобы перейти к оплате:", reply_markup=reply_markup)

async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как вас зовут?")
    return NAME

async def feedback_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Как с вами связаться? (email, @username или номер)")
    return CONTACT

async def feedback_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("Опишите ваш вопрос:")
    return MESSAGE

async def feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text

    name = context.user_data["name"]
    contact = context.user_data["contact"]
    message = context.user_data["message"]

    feedback = f"📩 Новое сообщение от клиента:\n\n" \
               f"👤 Имя: {name}\n📱 Контакт: {contact}\n💬 Сообщение:\n{message}"

    await context.bot.send_message(chat_id=ADMIN_ID, text=feedback)
    await update.message.reply_text("Спасибо! Ваше сообщение отправлено.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pay", pay))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_contact)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()