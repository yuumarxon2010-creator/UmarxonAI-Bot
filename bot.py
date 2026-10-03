import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Assalomu alaykum! Xush kelibsiz!\n\n"
        "Men UmarxonAI - AI botman.\n"
        "Google Gemini AI bilan ishlaymanman.\n\n"
        "💬 Savol bering - men javob beraman!\n"
        "📝 Matnni tahlil qilaman\n"
        "💻 Kod yozaman\n"
        "🧠 Har qanday savollarga javob beraman\n\n"
        "Shunchaki xat yozing yoki /help bosing."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Buyruqlar:\n"
        "/start - Botni boshlash\n"
        "/help - Yordam\n"
        "/info - Bot haqida\n\n"
        "Yoki shunchaki savol yozing! 😊"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Bot haqida:\n\n"
        "📛 Nomi: UmarxonAI\n"
        "🧠 AI Model: Google Gemini 1.5\n"
        "⏰ Vaqt: 24/7 online\n"
        "🌐 Platform: Telegram\n\n"
        "Bu bot barcha savollarga AI kabi javob berada oladi!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    await update.message.chat.send_action("typing")

    try:
        response = model.generate_content(text)
        answer = response.text
        
        if not answer:
            answer = "Kechirasiz, javobni olishda muammo yuz berdi. Keyinroq urinib ko'ring."

        # Agar javob uzun bo'lsa, bo'lib yuborish
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await update.message.reply_text(answer[i:i+4000])
        else:
            await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Xatolik yuz berdi!\n\n"
            f"Xato: {str(e)}\n\n"
            f"Keyinroq urinib ko'ring."
        )

def main():
    if not TOKEN or not API_KEY:
        raise ValueError("TELEGRAM_TOKEN yoki GEMINI_API_KEY topilmadi!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 UmarxonAI Bot ishga tushdi! 24/7 online...")
    app.run_polling()

if __name__ == "__main__":
    main()
