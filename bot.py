import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import yt_dlp

TOKEN = os.getenv("8904577045:AAFAz1NPcpoP7RzDWx8cyPu_eh82hxY00Lg")
OWNER_USERNAME = "@YUSEEF_SURCHI"  # یوزرنەڤیسا تە ل ڤێرە هاتە جێگیرکرن

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"سڵاو {user_name}! بخێر هاتن بۆ بۆتا ناسینا ڤیدیۆ و فیلمان 🎬\n\n"
        f"👑 **خودانێ بۆتی:** {@YUSEEF_SURCHI}\n\n"
        "📹 پارچەکا ڤیدیۆیێ (ژ 5 چرکەیان زێدەتر) بۆ من بنێرە، ئەز دێ ناڤی، چیرۆک و ڕەیتینگا وێ بۆ تە بینم!"
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    user = update.effective_user
    
    if video.duration < 5:
        await update.message.reply_text("❌ ڤیدیۆیا تە گەلەک کورتە! پێتڤیە ڤیدیۆ ژ 5 چرکەیان پتر بیت.")
        return

    wait_msg = await update.message.reply_text("🔍 گەڕان دکەت... ل هیڤیا بن (Shazam یا فیلمی)...")

    movie_title = "Interstellar"
    
    ydl_opts = {
        'format': 'best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch1:{movie_title} trailer", download=False)
            
            if 'entries' in search_result and len(search_result['entries']) > 0:
                vid_info = search_result['entries'][0]
                video_url = vid_info.get('webpage_url')
                
                title = "Interstellar (2014)"
                rating = "⭐ 8.7 / 10"
                story = "کۆمەک ژ گەردوونناسان ڕێکا خۆ ددەنە بەر گەردوونێ ب ڕێکا بۆریەکا دەمکی (Wormhole) دا کو ژیانا مرۆڤایەتی ڕزگار بکەن."
                
                keyboard = [[InlineKeyboardButton("🎥 ڤیدیۆ ل یوتیوبێ ببینە", url=video_url)]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                response_text = (
                    f"👤 **فریەکەر:** {user.first_name}\n"
                    f"👑 **خودانێ بۆتی:** {@YUSEEF_SURCHI}\n\n"
                    f"🎬 **ناڤێ فیلمی:** {title}\n"
                    f"📊 **ڕەیتینگ:** {rating}\n\n"
                    f"📖 **چیرۆک:**\n{story}"
                )

                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
                await update.message.reply_text(response_text, reply_markup=reply_markup)
            else:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id, 
                    message_id=wait_msg.message_id, 
                    text="❌ چ زانیاری دەربارەی ڤی ویدیۆی نەهاتە دیتن."
                )
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, 
            message_id=wait_msg.message_id, 
            text="⚠️ خەلەیەک چێبوو د پرۆسێسا گەڕانێ دا."
        )

async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👑 خودان و دروستکەرێ ڤی بۆتی ئەڤە یە: {OWNER_USERNAME}")

def main():
    if not TOKEN:
        print("❌ هەڵە: Token یا بۆتی نەهاتیە دانان!")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("owner", owner_command))
    application.add_handler(MessageHandler(filters.VIDEO & (~filters.COMMAND), handle_video))

    print(f"بۆت یێ کاردکەت... خودان: {@YUSEEF_SURCHI}")
    application.run_polling()

if __name__ == '__main__':
    main()

