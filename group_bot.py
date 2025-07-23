from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8085465476:AAHWrYGQMMOO318qS2xFyZeKkflzkuwnEfE'

# خوش‌آمدگویی
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🎉 خوش اومدی {member.full_name}!")

# فیلتر لینک و حذف
async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http" in update.message.text or "t.me" in update.message.text:
        await update.message.delete()

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات مدیریت گروه فعال است.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), anti_link))

    print("ربات فعال شد...")
    app.run_polling()
