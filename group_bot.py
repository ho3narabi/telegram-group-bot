import os
from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from collections import defaultdict

BOT_TOKEN ='8085465476:AAHWrYGQMMOO318qS2xFyZeKkflzkuwnEfE'' ' os.environ.get("BOT_TOKEN")

# دیتابیس ساده هشدارها (در حافظه)
warnings = defaultdict(int)

# لیست کلمات ممنوعه
bad_words = ["فحش", "کلمه_بد", "فحش2", "فحش3"]

# بررسی ادمین بودن کاربر
async def is_admin(update: Update):
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# ✅ start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات مدیریت گروه فعاله!")

# ℹ️ help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 دستورات ربات:\n"
        "/start - تست فعال بودن ربات\n"
        "/help - راهنمای دستورات\n"
        "/rules - نمایش قوانین گروه\n"
        "/warn - اخطار دادن (با ریپلای)\n"
        "/ban - بن کردن کاربر (با ریپلای)\n"
    )

# 📜 rules
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 قوانین گروه:\n"
        "1. احترام به دیگران\n"
        "2. ممنوعیت لینک و تبلیغات\n"
        "3. ارسال نکردن فحش یا پیام توهین‌آمیز"
    )

# 🎉 خوش‌آمدگویی
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🎉 خوش اومدی {member.full_name}!")

# 🧹 فیلتر لینک
async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "http" in text or "t.me" in text or "@" in text:
        await update.message.delete()

# 🚫 فیلتر فحش
async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for word in bad_words:
        if word in update.message.text.lower():
            await update.message.delete()
            await update.message.reply_text("❗ پیام حاوی کلمات نامناسب بود و حذف شد.")
            break

# ⚠️ اخطار دادن
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("لطفاً روی پیام کاربر ریپلای کن.")
        return

    user_id = update.message.reply_to_message.from_user.id
    warnings[user_id] += 1
    count = warnings[user_id]

    await update.message.reply_text(f"⚠️ به {update.message.reply_to_message.from_user.full_name} هشدار داده شد. تعداد هشدارها: {count}")

    if count >= 3:
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text(f"🚫 کاربر بعد از 3 هشدار بن شد.")

# 🔨 بن کردن کاربر
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("لطفاً روی پیام کاربر ریپلای کن.")
        return

    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
    await update.message.reply_text(f"❌ کاربر {update.message.reply_to_message.from_user.full_name} بن شد.")

# شروع اپ
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), anti_link))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filter_bad_words))

    print("🤖 ربات فعال شد...")
    app.run_polling()

