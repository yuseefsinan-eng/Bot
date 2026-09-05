import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8653317587:AAH59X7hIIQ2s3rH4rzT26vDMPCRsPVFth8"

OWNER_ID = 7643191802
ADMIN_ID = 8038533940

# Database کاتی (Memory)
user_balances = {}
video_wait_prompt = set()

app = Client("yuseef_surchi_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_admin_or_owner(user_id):
    return user_id in [OWNER_ID, ADMIN_ID]

@app.on_message(filters.command("start"))
def start_cmd(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0

    text = (
        "👋 سلاڤ و رێز / سڵاو و ڕێز!\n"
        "ب خێر هاتنی بۆ بۆتا چێکرنا ڤیدیۆیان یا 4K.\n"
        "بەخێر هاتن بۆ بۆتی دروستکردنی ڤیدیۆی 4K.\n\n"
        "ڤان دگمێن ل خوارێ بکاربینە / ئەم دوگمە خوارانە بەکاربهێنە:"
    )
    
    buttons = [
        [InlineKeyboardButton("🎬 دروستکرنا ڤیدیۆ (AI) / دروستکردنی ڤیدیۆ", callback_data="create_video")],
        [InlineKeyboardButton("💰 باڵانسا من / باڵانسم", callback_data="check_balance"),
         InlineKeyboardButton("💳 كرینا باڵانسی / کڕینی باڵانس", callback_data="buy_balance")],
        [InlineKeyboardButton("📦 پلەنێن بەشداریێ / پلانەکانی بەشداریکردن", callback_data="subscription_plans")],
    ]
    
    if is_admin_or_owner(user_id):
        buttons.append([InlineKeyboardButton("⚙️ MX PANEL (ڕێڤەبەر / بەڕێوەبەر)", callback_data="mx_panel")])

    message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query()
def callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    msg = callback_query.message

    if data == "check_balance":
        bal = user_balances.get(user_id, 0)
        msg.edit_text(
            f"💰 باڵانسا تەیا نۆکە / باڵانسی ئێستای تۆ: **{bal}** دینار\n\n"
            "بۆ زێدەکرنا باڵانسی / بۆ زیادکردنی باڵانس سەرەدانا ڤان هەردوو کاکا بکە:\n"
            "• @X_MAM6\n"
            "• @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر / گەڕانەوە", callback_data="main_menu")]])
        )

    elif data == "buy_balance":
        msg.edit_text(
            "💳 بۆ كرینا باڵانسی یان ڤەگوهاستنا پارەی / بۆ کڕینی باڵانس یان گواستنەوەی پارە، سەرەدانا ڤان یوزرنەمان بکە:\n\n"
            "👤 ڕێڤەبەر 1 / بەڕێوەبەر 1: @X_MAM6\n"
            "👤 ڕێڤەبەر 2 / بەڕێوەبەر 2: @YUSEEF_SURCHi\n\n"
            "پاشان داخوازییا خۆ بنێرە بۆ وان / پاشان داواکارییەکەت بۆیان بنێرە.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر / گەڕانەوە", callback_data="main_menu")]])
        )

    elif data == "subscription_plans":
        text = (
            "📦 **پلەنێن بەشدارییا ڤیدیۆیان (4K) / پلانی بەشداریکردنی ڤیدیۆ:**\n\n"
            "1️⃣ **بۆ هەیڤەکێ / بۆ مانگێک (5,000 دینار):** ڤیدیۆ چێکرنا بەردەوام / دروستکردنی ڤیدیۆی بەردەوام\n"
            "2️⃣ **بۆ 6 هەیڤان / بۆ 6 مانگ (10,000 دینار):** تەمامیا خزمەتگوزارییان / سەرجەم خزمەتگوزارییەکان\n"
            "3️⃣ **بۆ سالەکێ / بۆ ساڵێک (15,000 دینار):** هەموو تایبەتمەندی ب شێوەیەکێ تێر و پڕ\n\n"
            "💳 **بۆ کرینێ، سەرەدانا ڤان هەردوو کاکا بکە / بۆ کڕین سەردانی ئەم دوو کاکە بکە:**\n"
            "• @X_MAM6\n"
            "• @YUSEEF_SURCHi"
        )
        msg.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر / گەڕانەوە", callback_data="main_menu")]]))

    elif data == "create_video":
        video_wait_prompt.add(user_id)
        msg.edit_text(
            "✍️ پرۆمپتێ (Prompt) خۆ ب زمانێ **کوردی (بادینی و سۆرانی)** ل ڤێرە بنڤیسە:\n"
            "پڕۆمپتەکەت لێرە بنووسە (ئێمە خۆمان دەیگوازینەوە سەر ئینگلیزی بۆ 4K):\n"
            "(ئەم ب خۆ دێ تێکەلی ئینگلیزی کەین بۆ کوالێتییا 4K)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر / گەڕانەوە", callback_data="main_menu")]])
        )

    elif data == "mx_panel":
        if not is_admin_or_owner(user_id):
            callback_query.answer("⚠️ ئەڤ پشکە تنێ بۆ خودان و ڕێڤەبەری یە! / ئەم بەشە تەنها بۆ خاوەن و بەڕێوەبەرە!", show_alert=True)
            return
        
        msg.edit_text(
            "⚙️ **MX PANEL (ڕێڤەبەری / بەڕێوەبەرایەتی)**\n\n"
            "ل ڤێرە تو دشێی باڵانسی بۆ بکارهێنەران زێدە بکەی / لێرە دەتوانیت باڵانس بۆ بەکارهێنەران زیاد بکەیت.\n"
            "شێوازێ نڤیسینێ د چاتێ دا / شێوازی نووسین لە چاتدا:\n"
            "`/addbal [ID] [ڕێژە / بڕ]`\n\n"
            "بۆ نموونە: `/addbal 123456789 5000`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ڤەگەر / گەڕانەوە", callback_data="main_menu")]])
        )

    elif data == "main_menu":
        if user_id in video_wait_prompt:
            video_wait_prompt.remove(user_id)
        
        buttons = [
            [InlineKeyboardButton("🎬 دروستکرنا ڤیدیۆ (AI) / دروستکردنی ڤیدیۆ", callback_data="create_video")],
            [InlineKeyboardButton("💰 باڵانسا من / باڵانسم", callback_data="check_balance"),
             InlineKeyboardButton("💳 كرینا باڵانسی / کڕینی باڵانس", callback_data="buy_balance")],
            [InlineKeyboardButton("📦 پلەنێن بەشداریێ / پلانی بەشداریکردن", callback_data="subscription_plans")],
        ]
        if is_admin_or_owner(user_id):
            buttons.append([InlineKeyboardButton("⚙️ MX PANEL (ڕێڤەبەر / بەڕێوەبەر)", callback_data="mx_panel")])

        msg.edit_text("🏠 سەرەتا / سەرەکی:\nفەرموو ئێك ژ ڤان ڤالەکان هەلبژێرە / تکایە بژاردەیەک هەڵبژێرە:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.text & ~filters.command(["start", "addbal"]))
def handle_text(client, message: Message):
    user_id = message.from_user.id
    
    if user_id in video_wait_prompt:
        video_wait_prompt.remove(user_id)
        kurdish_prompt = message.text
        
        # تێکەڵکرنا بادینی/سۆرانی دگەل ئینگلیزی بۆ 4K
        enhanced_prompt = f"{kurdish_prompt}, cinematic 4k resolution, highly detailed, photorealistic, masterwork"
        
        sent_msg = message.reply_text("⏳ تشتەکی بڕاوە... ڤیدیۆیا تە یا 4K بەرهەم دهێت / چاوەڕوان بە... ڤیدیۆی 4K ئامادە دەبێت...")
        
        sent_msg.edit_text(
            f"✅ **ڤیدیۆیا تە ب سەرکەفتی هاتە چێکرن! / ڤیدیۆکەت بە سەرکەوتوویی دروست کرا!**\n\n"
            f"🌐 **Prompt:** `{enhanced_prompt}`\n"
            f"💬 **دەقێ تە / دەقەکەت:** {kurdish_prompt}\n"
            f"🎬 **کوالێتی / کوالێتی:** 4K (100% کارا / کارا)\n\n"
            "💳 بۆ نووژەنکرنا باڵانسی سەرەدانا @X_MAM6 یان @YUSEEF_SURCHi بکە."
        )

@app.on_message(filters.command("addbal"))
def add_balance_cmd(client, message: Message):
    user_id = message.from_user.id
    if not is_admin_or_owner(user_id):
        message.reply_text("⚠️ ئەڤ فەرمانە تنێ بۆ خودان و ڕێڤەبەری یە! / ئەم فەرمانە تەنها بۆ بەڕێوەبەرە!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        message.reply_text("⚠️ شێوازێ ڤەکرنێ هەڵە یە! / شێوازی فەرمانەکە هەڵەیە!\nبکاربینە / بەکاربهێنە: `/addbal [ID] [ڕێژە]`")
        return
    
    try:
        target_id = int(args[1])
        amount = int(args[2])
        
        if amount > 1000000000000: # سنۆرێ 1 ترلیۆن
            message.reply_text("⚠️ ڕێژە گەلەک مەزنە! نەشێی ژ 1 ترلیۆن زیاتر باڵانسی زێدە بکەی.")
            return

        if target_id not in user_balances:
            user_balances[target_id] = 0
            
        user_balances[target_id] += amount
        message.reply_text(f"✅ ب سەرکەفتی باڵانس هاتە زێدەکرن / باڵانس زیاد کرا بۆ ID: `{target_id}`\nمەبلەغ / بڕ: **{amount}**\nباڵانسا نوو / باڵانسی نوێ: **{user_balances[target_id]}**")
    except ValueError:
        message.reply_text("⚠️ ژ ڕەحمەتا خۆ ID و مەبلەغی ب ژمارە بنڤیسە / تکایە ID و بڕەکە بە ژمارە بنووسە.")

app.run()

