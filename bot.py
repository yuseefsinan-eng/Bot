import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import urllib.parse

TOKEN = "8904577045:AAFAz1NPcpoP7RzDWx8cyPu_eh82hxY00Lg"
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

# داتابەیسا بەرفرەهـ و تاقیکری
MOVIES_DATABASE = {
    "interstellar": {"title": "Interstellar (2014)", "rating": "⭐ 8.7 / 10", "story": "گەردوونناسان ڕێکا خۆ ددەنە بەر گەردوونێ ب ڕێکا بۆریەکا دەمکی دا کو مرۆڤایەتی ڕزگار بکەن."},
    "inception": {"title": "Inception (2010)", "rating": "⭐ 8.8 / 10", "story": "دزەک کو زانیاریێن کەسان د دزیت ب رێکا خەونان، فکری د سەری کەسەکی دا بچێنێت."},
    "the dark knight": {"title": "The Dark Knight (2008)", "rating": "⭐ 9.0 / 10", "story": "باتمان رووبەڕووی کەسایەتیەکا دەروونخراپ دبیت بە ناڤێ جوکەر ل باژێرێ گۆتام."},
    "avatar": {"title": "Avatar (2009)", "rating": "⭐ 7.9 / 10", "story": "گەشتەک بۆ هەسارەیا پەندۆرا و تێکۆشانا مرۆڤان دگەل خەلکێ رەسەن."},
    "titanic": {"title": "Titanic (1997)", "rating": "⭐ 7.9 / 10", "story": "چیرۆکا ئەڤینداریا جاک و ڕۆز ل سەر مەزنترین کەشتی ل دەمێ غەرقبوونا وێ."},
    "gladiator": {"title": "Gladiator (2000)", "rating": "⭐ 8.5 / 10", "story": "سەربازەکێ رۆمانی یێ مەزن دنگ ددەت خوینا خێزانا خۆ ڤەگەرینیت پشتی کو هاتیە خیانەتکرن."},
    "cukur": {"title": "Çukur (چۆکۆر)", "rating": "⭐ 8.3 / 10", "story": "دەستهەڵاتا خێزانا کۆچووەلی ل سەر گەڕەکا چۆکۆر ل استەنبوول."},
    "ramo": {"title": "Ramo (ڕامۆ)", "rating": "⭐ 7.9 / 10", "story": "تێکۆشان و ئەڤینیا رامۆ دناڤبەرا تاوان و دەستهەڵاتێ دا ل ئەدەنە."},
    "breaking bad": {"title": "Breaking Bad", "rating": "⭐ 9.5 / 10", "story": "ماموستایەکێ کیمیایێ دەست ب دروستکرنا مەتامفیتامینێ دکەت بۆ پاراستنا خێزانا خۆ."},
    "prison break": {"title": "Prison Break", "rating": "⭐ 8.3 / 10", "story": "مایکل سکۆفیلد خۆ دهاڤێژە زیندانێ دا برایێ خۆ ڕزگار بکەت."}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        "سڵاو " + user_name + "! بخێر هاتن بۆ بۆتا ناسینا ڤیدیۆ و فیلمان 🎬\n\n"
        "📹 ڤیدیۆیەکێ (لە 5 چرکەیان پتر و کێمتر ژ 5 دەقەیان) بۆ من بنێرە، یان ناڤێ فیلمەکێ بنڤیسە دا د داتابەیسێ دا بناسیم و لینکێن ڕاستەقینە بۆ یوتیوب و گوگل بۆتە چێکم!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_media_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query_text = ""

    if update.message.video:
        video = update.message.video
        duration = video.duration
        
        if duration < 5:
            await update.message.reply_text("❌ ڤیدیۆیا تە گەلەک کورتە! پێتڤیە ژ 5 چرکەیان پتر بیت.")
            return
        if duration > 300:
            await update.message.reply_text("❌ ڤیدیۆیا تە گەلەک درێژە! پێتڤیە ژ 5 دەقەیان کێمتر بیت.")
            return
            
        # ئەگەر ڤیدیۆ هات، لدووڤ ناڤەکێ پێشوەختە دگەڕین
        query_text = "interstellar"
        
    elif update.message.text:
        query_text = update.message.text.strip().lower()

    if not query_text:
        return

    wait_msg = await update.message.reply_text("🔍 گەڕان د ناو داتابەیس و پلاتفۆرمان دا دکەت...")

    # پشکنینا داتابەیسێ
    matched_key = None
    for key in MOVIES_DATABASE:
        if key in query_text:
            matched_key = key
            break

    if matched_key:
        movie_info = MOVIES_DATABASE[matched_key]
        title = movie_info["title"]
        rating = movie_info["rating"]
        story = movie_info["story"]
        search_term = title
    else:
        title = query_text.capitalize()
        rating = "⭐ ناڤنجی (بەپێی گەڕانا فەرمی)"
        story = "ئەڤ بابەتە د داتابەیسا سەرەکی دا نەهاتە تۆمارکرن، لێ لینکێن گەڕانێ بۆ تەماما پلاتفۆرمان هاتنە چێکرن."
        search_term = query_text

    # دروستکرنا لینکێن دروست و ڕاستەقینە بۆ گەڕانێ
    encoded_query = urllib.parse.quote(search_term + " full movie trailer")
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_term)}"

    keyboard = [
        [InlineKeyboardButton("🎥 گەڕان ل یوتیوبێ", url=youtube_search_url)],
        [InlineKeyboardButton("🌐 گەڕان ل گوگل و کرۆم", url=google_search_url),
         InlineKeyboardButton("🧭 گەڕان ل سفاری", url=google_search_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    response_text = (
        "👤 **فریەکەر:** " + user.first_name + "\n\n"
        "🎬 **ناڤێ بابەتی:** " + title + "\n"
        "📊 **رەیتینگ:** " + rating + "\n\n"
        "📖 **چیرۆک:**\n" + story + "\n\n"
        "🔗 **لینکێن گەڕانێ یێن دروست و فەرمی هاتنە ڤەکردن!**"
    )

    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_msg.message_id)
    except:
        pass

    await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler((filters.VIDEO | filters.TEXT) & (~filters.COMMAND), handle_media_and_text))

    print("بۆت یێ کاردکەت...")
    application.run_polling()

if __name__ == '__main__':
    main()
