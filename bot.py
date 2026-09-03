import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import urllib.parse

TOKEN = "8904577045:AAFAz1NPcpoP7RzDWx8cyPu_eh82hxY00Lg"
API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"

# داتابەیسا بەرفرەهـ و مەزن (نێزیکی 50 فیلم و سریالێن ناودار)
MOVIES_DATABASE = {
    # فیلمێن جیهانی
    "interstellar": {"title": "Interstellar (2014)", "rating": "⭐ 8.7 / 10", "story": "گەردوونناسان ڕێکا خۆ ددەنە بەر گەردوونێ ب ڕێکا بۆریەکا دەمکی دا کو مرۆڤایەتی ڕزگار بکەن."},
    "inception": {"title": "Inception (2010)", "rating": "⭐ 8.8 / 10", "story": "دزەک کو زانیاریێن کەسان د دزیت ب رێکا خەونان، فکری د سەری کەسەکی دا بچێنێت."},
    "the dark knight": {"title": "The Dark Knight (2008)", "rating": "⭐ 9.0 / 10", "story": "باتمان رووبەڕووی کەسایەتیەکا دەروونخراپ دبیت بە ناڤێ جوکەر ل باژێرێ گۆتام."},
    "avatar": {"title": "Avatar (2009)", "rating": "⭐ 7.9 / 10", "story": "گەشتەک بۆ هەسارەیا پەندۆرا و تێکۆشانا مرۆڤان دگەل خەلکێ رەسەن."},
    "titanic": {"title": "Titanic (1997)", "rating": "⭐ 7.9 / 10", "story": "چیرۆکا ئەڤینداریا جاک و ڕۆز ل سەر مەزنترین کەشتی ل دەمێ غەرقبوونا وێ."},
    "gladiator": {"title": "Gladiator (2000)", "rating": "⭐ 8.5 / 10", "story": "سەربازەکێ رۆمانی یێ مەزن دنگ ددەت خوینا خێزانا خۆ ڤەگەرینیت پشتی کو هاتیە خیانەتکرن."},
    "avengers endgame": {"title": "Avengers: Endgame (2019)", "rating": "⭐ 8.4 / 10", "story": "شەرێ دووماهیێ یێ قارەمانێن مارڤل دژی تانۆس بۆ ڤەگەراندنا نیڤا مرۆڤێن جیهانێ."},
    "joker": {"title": "Joker (2019)", "rating": "⭐ 8.4 / 10", "story": "چیرۆکا کەسەکی تنێ ب ناڤێ ئارسەر فلێک کو دکەڤیتە نێڤ دلێ شێتاتیێ و ناسناما جوکەر وەرگرت."},
    "matrix": {"title": "The Matrix (1999)", "rating": "⭐ 8.7 / 10", "story": "هوشیاربوونا نێۆ و زانینا کو جیهانا ئەم تێدا دژین تنێ سیستەمەکی کۆمپیوتەری یە."},
    "fight club": {"title": "Fight Club (1999)", "rating": "⭐ 8.8 / 10", "story": "کارمەندەکێ نڤیسینگەیێ ب نەخۆشا خەوزەندێ تووشبووی یانا شەڕی پێک دئینێت."},
    "forrest gump": {"title": "Forrest Gump (1994)", "rating": "⭐ 8.8 / 10", "story": "چیرۆکا ژیانا فۆڕێست گەمپ، کەسەکی سادە لێ ب پشکداریەکا مەزن د دیرۆکا ئەمریکایێ دا."},
    "spider-man": {"title": "Spider-Man: No Way Home", "rating": "⭐ 8.2 / 10", "story": "هاتنا پاشایێن فرە-گەردوونێ و ئاشکرابوونا رازێن سپایدەرمان."},
    "thor": {"title": "Thor: Ragnarok", "rating": "⭐ 7.9 / 10", "story": "تۆر دڤێت ئەسگارد ژ هەلوەشینێ و هێزا هەلا پاریزیت."},
    "fast and furious": {"title": "Fast & Furious", "rating": "⭐ 7.1 / 10", "story": "زنجیرەیا ماشێن و لەزاتیا بلید و خێزانا دۆم تۆرێتۆ."},
    "john wick": {"title": "John Wick (2014)", "rating": "⭐ 7.4 / 10", "story": "کوشتکارێ خانەنشینکری دزڤڕیتە ڤە بۆ تۆلاتندنێ پشتی کو کوشتنا سەگێ وی."},
    "oppenheimer": {"title": "Oppenheimer (2023)", "rating": "⭐ 8.9 / 10", "story": "چیرۆکا زانایێ ئەتۆمی جەی ڕۆبەرت ئۆپینهایمەر و دروستکرنا بۆمبا ئەتۆمی."},
    "barbie": {"title": "Barbie (2023)", "rating": "⭐ 6.8 / 10", "story": "گەشتەکا پڕ ڕەنگ و فەلسەفی یا باربی ژ جیهانا پەمپی بۆ جیهانا ڕاستەقینە."},
    "dune": {"title": "Dune: Part Two", "rating": "⭐ 8.6 / 10", "story": "پۆل ئاتریدیس هەڤپشکیا هۆزێن بیابانێ دکەت بۆ تۆرانا دوژمنێن خێزانا خۆ."},
    "the batman": {"title": "The Batman (2022)", "rating": "⭐ 7.8 / 10", "story": "باتمان لدووڤ گەندەلیێن باژێرێ گۆتام دگەڕێت و رووبەڕووی ریدلەر دبیت."},
    "aquaman": {"title": "Aquaman (2018)", "rating": "⭐ 6.9 / 10", "story": "شاهێ دەریایان شەرێ پاراستنا ئاتلانتس و رویی دکەت."},

    # سریالێن جیهانی
    "breaking bad": {"title": "Breaking Bad", "rating": "⭐ 9.5 / 10", "story": "ماموستایەکێ کیمیایێ دەست ب دروستکرنا مەتامفیتامینێ دکەت بۆ پاراستنا خێزانا خۆ."},
    "game of thrones": {"title": "Game of Thrones", "rating": "⭐ 9.2 / 10", "story": "خێزانێن پاشایەتی شەرێ گرتنا تەختێ آسنی ل جیهانەکا خیالی دکەن."},
    "prison break": {"title": "Prison Break", "rating": "⭐ 8.3 / 10", "story": "مایکل سکۆفیلد خۆ دهاڤێژە زیندانێ دا برایێ خۆ ڕزگار بکەت."},
    "dark": {"title": "Dark", "rating": "⭐ 8.7 / 10", "story": "ونبوونا زارۆکان ل باژێرەکە ئەڵمانی و پهەیوەندیا وێ ب گەشتکرنا دەمی."},
    "peaky blinders": {"title": "Peaky Blinders", "rating": "⭐ 8.8 / 10", "story": "خێزانا شێڵبی و دەستهەڵاتا وان ل باژێرێ برمینگهام ل انگلتەرا."},
    "money heist": {"title": "Money Heist (La Casa de Papel)", "rating": "⭐ 8.2 / 10", "story": "پلانا مەزن یا دزیتا بانکا مرکزی یا اسپانیا ب سەرۆکایەتیا پڕۆفیسۆر."},
    "stranger things": {"title": "Stranger Things", "rating": "⭐ 8.7 / 10", "story": "زارۆکێن باژێرەکێ بچووک رووبەڕووی تاقیگەهێن نهێنی و جیهانا پێچەوانە دبەن."},
    "the witcher": {"title": "The Witcher", "rating": "⭐ 8.0 / 10", "story": "گەشتەکا گێراڵتێ ریویا ل ناڤبەرا دڕندە و ئەحکامێن جیهانەکا خیالی."},
    "vikings": {"title": "Vikings", "rating": "⭐ 8.5 / 10", "story": "چیرۆکا رارنار لۆدبڕۆک و گەشتێن وایکانگ بۆ داگیرکرنا ولاتێن نوو."},
    "sherlock": {"title": "Sherlock", "rating": "⭐ 9.1 / 10", "story": "ڤەکۆلینێن زیرەکێن شەرلۆک هۆڵمز ل سەردەمێ نوو ل لندن."},

    # سریالێن ترکی
    "cukur": {"title": "Çukur (چۆکۆر)", "rating": "⭐ 8.3 / 10", "story": "دەستهەڵاتا خێزانا کۆچووەلی ل سەر گەڕەکا چۆکۆر ل استەنبوول."},
    "ramo": {"title": "Ramo (ڕامۆ)", "rating": "⭐ 7.9 / 10", "story": "تێکۆشان و ئەڤینیا رامۆ دناڤبەرا تاوان و دەستهەڵاتێ دا ل ئەدەنە."},
    "kurtlar vadisi": {"title": "Kurtlar Vadisi (قۆناغا گورگان)", "rating": "⭐ 8.5 / 10", "story": "چیرۆکا پۆلات ئەلەمدار و مژارێن مافیا و دەزگەهێن هەواڵگریێ."},
    "sifir بير": {"title": "Sıfır Bir", "rating": "⭐ 8.1 / 10", "story": "کۆمەک گەنج ل گەڕەکێن هەژار خۆ ل دژی تلیاک و مافیایان راوەستینن."},
    "icerde": {"title": "İçerde (ناڤخوەیی)", "rating": "⭐ 8.5 / 10", "story": "دوو برایێن جودا ل زارۆکاتیێ، یەک دناڤ پلیسان دا و یێ دی دناڤ باندێ دا."},
    "mucize doktor": {"title": "Mucize Doktor", "rating": "⭐ 8.0 / 10", "story": "چیرۆکا پزیشکەکێ خودی پێداویستیێن تایبەت (نەخۆشیچا ئۆتیزم) ل نەخۆشخانەیێ."},
    "erkenci kus": {"title": "Erkenci Kuş", "rating": "⭐ 7.3 / 10", "story": "چیرۆکا ئەڤینیا جان و سانەم ل کۆمپانیایەکا ڕیکلامان."},
    "hudutsuz sevda": {"title": "Hudutsuz Sevda", "rating": "⭐ 7.6 / 10", "story": "خەبات و تۆلاتندنا خەلیل ئبراهیم بۆ ڤەگەراندنا کەرامەتا خێزانا خۆ."},
    "carpisma": {"title": "Çarpisma (لێکدان)", "rating": "⭐ 7.6 / 10", "story": "ڕویدانا رودانەکا ماشینی یا ب مەرەم کو چار کەسان بێکڤە گڕێدەت."},
    "kara sevda": {"title": "Kara Sevda (ئەڤینا ڕەش)", "rating": "⭐ 7.4 / 10", "story": "ئەڤینەکا نەمر و سەخت دناڤبەرا کەمال و نیهان دا."},
    "safir": {"title": "Safir (یاقوت)", "rating": "⭐ 7.0 / 10", "story": "رازێن خێزانەیی و ئەڤین و تۆرەیێن ناڤ خێزانا گۆلسۆی ل نەڤشەهیر."},
    "yalyin": {"title": "Yargı", "rating": "⭐ 8.6 / 10", "story": "دادوەر و سەرۆکێ داواکاریێن گشتی دکەڤنە ناڤ کەیسەکا کوشتنێ یا توند."},
    "sen anlat karadeniz": {"title": "Sen Anlat Karadeniz", "rating": "⭐ 7.5 / 10", "story": "تێکۆشانا نەفسێ دژی توندوتیژیا دەروونی و جەستەیی."},
    "kurulus osman": {"title": "Kurulus Osman", "rating": "⭐ 7.7 / 10", "story": "دامەزراندنا دەستهەڵاتا عوسمانی ب سەرۆکایەتیا عوسمان بەگ."},
    "payitaht abdulhamid": {"title": "Payitaht Abdülhamid", "rating": "⭐ 7.9 / 10", "story": "دیرۆکا سەردەمێ سوڵتان عەبدولحەمیدێ دووێ و پیلانێن دژی وێ."}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        "سڵاو " + user_name + "! بخێر هاتن بۆ بۆتا ناسینا ڤیدیۆ و فیلمان 🎬\n\n"
        "📹 ڤیدیۆیەکێ (لە 5 چرکەیان پتر و کێمتر ژ 5 دەقەیان) بۆ من بنێرە، یان ناڤێ فیلمەکێ بنڤیسە د داخابەیسێ دا (نێزیکی 50 فلیم و سریال) دا لینکێن گەڕانێ بۆ یوتیوب، گوگل، سفاری و کرۆم بۆتە بنێرم!"
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
            
        query_text = "interstellar"
        
    elif update.message.text:
        query_text = update.message.text.strip().lower()

    if not query_text:
        return

    wait_msg = await update.message.reply_text("🔍 گەڕان ل داتابەیس، گوگل، یوتیوب، سفاری و کرۆم دکەت... ل هیڤیا بن...")

    encoded_query = urllib.parse.quote(query_text)
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    google_search_url = f"https://www.google.com/search?q={encoded_query}"
    
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
    else:
        title = query_text.capitalize()
        rating = "⭐ ناڤنجی (بەپێی گەڕانا پلاتفۆرمان)"
        story = "ئەڤ بابەتە د داتابەیسا مەزن دا نەهاتە دیتن، لێ لینکێن گەڕانێ بۆ هەمی پلاتفۆرمان ئامادە نە."

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
        "📖 **چیرۆک / زانیاری:**\n" + story + "\n\n"
        "🔗 **لینکێن گەڕانێ ل یوتیوب، گوگل، سفاری و کرۆم هاتنە ڤەکردن!**"
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
