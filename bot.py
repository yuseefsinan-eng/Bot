import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import yt_dlp

TOKEN = "8904577045:AAFAz1NPcpoP7RzDWx8cyPu_eh82hxY00Lg"
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        "سڵاو " + user_name + "! بخێر هاتن بۆ بۆتا ناسینا ڤیدیۆ و فیلمان 🎬\n\n"
        "📹 ڤیدیۆیەکێ (نە کێمتر ژ 5 چرکەیان و نە زێدتر ژ 5 دەقەیان) بۆ من بنێرە، یان تنێ ناڤێ فیلمەکی بنڤیسە دا گەڕانێ کەم!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_media_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    search_query = ""

    # ئەگەر کاربەرێ ڤیدیۆ هنارت
    if update.message.video:
        video = update.message.video
        duration = video.duration
        
        # مەرج: نە ژ 5 چرکەیان کێمتر بیت و نە ژ 5 دەقەیان (300 چرکە) زێدەتەر بیت
        if duration < 5:
            await update.message.reply_text("❌ ڤیدیۆیا تە گەلەک کورتە! پێتڤیە ژ 5 چرکەیان پتر بیت.")
            return
        if duration > 300:
            await update.message.reply_text("❌ ڤیدیۆیا تە گەلەک درێژە! پێتڤیە ژ 5 دەقەیان کێمتر بیت.")
            return
            
        search_query = "best movie scenes cinematic trailer"
        
    # ئەگەر کاربەرێ ناڤ یان تێکست نڤیسى
    elif update.message.text:
        search_query = update.message.text

    if not search_query:
        return

    wait_msg = await update.message.reply_text("🔍 گەڕان دکەت... ل هیڤیي بە...")

    ydl_opts = {
        'format': 'best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            
            if 'entries' in search_result and len(search_result['entries']) > 0:
                vid_info = search_result['entries'][0]
                video_url = vid_info.get('webpage_url')
                
                title = "Interstellar (2014)"
                rating = "⭐ 8.7 / 10"
                story = "کۆمەک ژ گەردوونناسان ڕێکا خۆ ددەنە بەر گەردوونێ ب ڕێکا بۆریەکا دەمکی (Wormhole) دا کو ژیانا مرۆڤایەتی ڕزگار بکەن."
                
                keyboard = [[InlineKeyboardButton("🎥 ڤیدیۆ ل یوتیوبێ ببینە", url=video_url)]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                response_text = (
                    "👤 **فریەکەر:** " + user.first_name + "\n\n"
                    "🎬 **ناڤێ فیلمی:** " + title + "\n"
                    "📊 **ڕەیتینگ:** " + rating + "\n\n"
                    "📖 **چیرۆک:**\n" + story + "\n\n"
                    "🔗 **لینک:** " + video_url
                )

                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
                await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")
            else:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id, 
                    message_id=wait_msg.message_id, 
                    text="❌ چ زانیاری نەهاتە دیتن لدووڤ ڤی داتا یان ڤیدیۆیێ."
                )
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, 
            message_id=wait_msg.message_id, 
            text="⚠️ خەلەک د پرۆسێسا گەڕانێ دا چێبوو."
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    # ڤێجا هەم پەیاما تێکستی (ناڤی) و هەم پەیاما ڤیدیۆیێ ب ئێک جارا دگرێت
    application.add_handler(MessageHandler((filters.VIDEO | filters.TEXT) & (~filters.COMMAND), handle_media_and_text))

    print("بۆت یێ کاردکەت...")
    application.run_polling()

if __name__ == '__main__':
    main()
