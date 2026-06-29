import os
from flask import Flask
from threading import Thread
from datetime import time

print("BOT KODI ISHLAYAPTI")

from games import get_game
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN, CHANNEL


# Render uchun web server
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "GameVoices bot ishlayapti!"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_web)
    t.start()


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 GameVoices bot ishlayapti!"
    )


# Qo'lda post tashlash
async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE):

    game = get_game()

    if not game:
        await update.message.reply_text(
            "❌ O‘yin topilmadi"
        )
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


# Avtomatik post
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

    # Render port ishga tushadi
    keep_alive()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("post", post_now)
    )


    # Har kuni 18:00 post
    app.job_queue.run_daily(
        auto_post,
        time(hour=18, minute=0)
    )


    print("🤖 GameVoices ishga tushdi")

    app.run_polling()


if __name__ == "__main__":
    main()