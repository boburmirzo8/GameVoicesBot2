from datetime import time

print("BOT KODI ISHLAYAPTI")

from games import get_game
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN, CHANNEL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 GameVoices bot ishlayapti!"
    )


async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE):

    game = get_game()

    if not game:
        await update.message.reply_text("❌ O‘yin topilmadi")
        return

    caption = f"""
🎮 Yangi o‘yin

🔥 {game['title']}

💰 Narxi: {game['price']}$

🏷 Chegirma: {game['discount']}%

💻 Platforma: PC

🎮 @gamevoices1
"""

    await context.bot.send_photo(
        chat_id=CHANNEL,
        photo=game["image"],
        caption=caption
    )

    await update.message.reply_text(
        "✅ Rasmli o‘yin posti yuborildi"
    )


async def auto_post(context: ContextTypes.DEFAULT_TYPE):

    game = get_game()

    if not game:
        print("❌ O‘yin topilmadi")
        return

    caption = f"""
🎮 Yangi o‘yin

🔥 {game['title']}

💰 Narxi: {game['price']}$

🏷 Chegirma: {game['discount']}%

💻 Platforma: PC

🎮 @gamevoices1
"""

    await context.bot.send_photo(
        chat_id=CHANNEL,
        photo=game["image"],
        caption=caption
    )

    print("✅ Avtomatik post yuborildi")


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post_now))

    # Har kuni 18:00 da post
    app.job_queue.run_daily(
        auto_post,
        time(hour=18, minute=0)
    )

    print("🤖 GameVoices ishga tushdi")

    app.run_polling()


if __name__ == "__main__":
    main()