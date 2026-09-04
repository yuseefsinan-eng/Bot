import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def user_bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 سڵاڤ! ئەڤە بۆتا تە یە یا تایبەت کو ل سەر سێرڤەری هاتییە کارپێکرن.")

def main():
    if len(sys.argv) < 2:
        print("Token نەهاتییە دابینکرن!")
        return
        
    bot_token = sys.argv[1]
    
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", user_bot_start))
    
    print("بۆتا بەکارهێنەری دەست پێکر...")
    application.run_polling()

if __name__ == "__main__":
    main()
