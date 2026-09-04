import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Token (باشترە ل Railway ل Environment Variables ب دانەی ب ناڤێ BOT_TOKEN)
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Profile Data & Text
    profile_text = (
        f"👤 **پروفایلا تە (User Profile)**\n\n"
        f"• **ناڤ:** {user.first_name}\n"
        f"• **یوزرنەیم:** @{user.username or 'نەهاتییە دانان'}\n"
        f"• **ایدی:** `{user.id}`\n\n"
        f"🤖 بۆت یێ ئامادەیە و ب سەرکەفتیانە ل سەر سێرڤەری کار دکەت!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📁 برڤەبرنا فایلان (Files)", callback_data="files_menu")],
        [InlineKeyboardButton("⚙️ ڕێکخستن (Settings)", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(profile_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(profile_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "files_menu":
        keyboard = [
            [InlineKeyboardButton("⬅️ ڤەگەر بۆ پروفایلی", callback_data="back_to_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📁 **بەڕێوەبرنا فایلان**\n\n"
            "• **سنۆرێ فایلان:** مەزنترین قەبارە و هژمار د هێنە کۆنترۆلکرن.\n"
            "• فایل ل سەر سێرڤەری ب شێوەیەکێ پاراستی دهێنە ڕێڤەبرن.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == "back_to_profile":
        await start(update, context)

def main():
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("هۆشیاری: پێدڤییە Tokenێ بۆتی دابنەی!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("بۆت دەست پێکر و ل چاڤەڕێیا پەیامانە...")
    application.run_polling()

if __name__ == "__main__":
    main()
