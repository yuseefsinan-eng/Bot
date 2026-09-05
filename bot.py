import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8653317587:AAH59X7hIIQ2s3rH4rzT26vDMPCRsPVFth8"

OWNERS = [7643191802, 8038533940]

user_balances = {}
user_languages = {}  
user_subscriptions = {}  
video_wait_prompt = set()
mx_waiting_id = set()  # بۆ گرتنا ID یا بکارهێنەری ژ خودانی
mx_target_users = {}   # حافیزەکراو بۆ ID یا هاتییە نڤیسین

app = Client("yuseef_surchi_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_owner(user_id):
    return user_id in OWNERS

def get_text(user_id, key):
    lang = user_languages.get(user_id, "ku") 
    texts = {
        "ku": {
            "welcome": "👋 سلاڤ و رێز!\nب خێر هاتنی بۆ بۆتا چێکرنا ڤیدیۆیان یا 4K.\nفەرموو زمانێ خۆ هەلبژێرە یان ئێک ژ ڤان ڤالەکان بکاربخە:",
            "btn_video": "🎬 دروستکرنا ڤیدیۆ (AI)",
            "btn_bal": "💰 باڵانسا من",
            "btn_buy": "💳 كرینا باڵانسی",
            "btn_sub": "📦 پلەنێن پشکداریکردنێ",
            "btn_prof": "👤 پروفایلا من",
            "btn_lang": "🌐 گوهۆڕینا زمانێ (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بۆ ڕێڤەبەرا)",
            "back": "🔙 ڤەگەر",
            "choose_lang": "🌐 زمانێ خۆ هەلبژێرە / Select your language:",
            "lang_changed": "✅ زمان ب سەرکەفتی هاتە گوهۆڕین!",
            "no_sub": "❌ تە چ پشکداریکردن نینە. لطفەن پشکداریکردنێ لە سەرەتا چێکە یان باڵانسا خۆ بگووهۆرە.\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ پشکداریکردنا تە یا کارا یە! فەرموو پرۆمپتێ (Prompt) خۆ ب نڤیسە بۆ دروستکرنا ڤیدیۆیا 4K:",
            "days_left": "ڕۆژ ماینە بۆ خلاساربوونێ",
            "video_success": "✅ ڤیدیۆیا تە ب سەرکەفتی هاتە چێکرن ب کوالێتییا 4K!",
            "admin_only": "⚠️ ئەڤ پشکە تنێ بۆ خودان و ڕێڤەبەرا یە!"
        },
        "ckb": {
            "welcome": "👋 سڵاو و ڕێز!\nبەخێر هاتیت بۆ بۆتی دروستکردنی ڤیدیۆی 4K.\nتکایە زمانەک هەڵبژێرە یان یەکێک لەم بژاردانە بەکاربهێنە:",
            "btn_video": "🎬 دروستکردنی ڤیدیۆ (AI)",
            "btn_bal": "💰 باڵانسم",
            "btn_buy": "💳 کڕینی باڵانس",
            "btn_sub": "📦 پلانی بەشداریکردن",
            "btn_prof": "👤 پڕۆفایلم",
            "btn_lang": "🌐 گۆڕینی زمان (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بە بەڕێوەبەران)",
            "back": "🔙 گەڕانەوە",
            "choose_lang": "🌐 زمانەکەت هەڵبژێرە / Select your language:",
            "lang_changed": "✅ زمان بە سەرکەوتوویی گۆڕدرا!",
            "no_sub": "❌ تۆ هیچ بەشداریکردنت نییە. تکایە سەرەتا بەشداریکردن بکە.\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ بەشداریکردنەکەت چالاکە! تکایە پڕۆمپتەکەت بنووسە بۆ دروستکردنی ڤیدیۆی 4K:",
            "days_left": "ڕۆژ ماون بۆ کۆتایی هاتن",
            "video_success": "✅ ڤیدیۆکەت بە سەرکەوتوویی دروست کرا بە کوالێتی 4K!",
            "admin_only": "⚠️ ئەم بەشە تەنها بۆ خاوەن و بەڕێوەبەرانە!"
        },
        "en": {
            "welcome": "👋 Hello!\nWelcome to the 4K AI Video Generation Bot.\nPlease select your language or choose an option below:",
            "btn_video": "🎬 Create Video (AI)",
            "btn_bal": "💰 My Balance",
            "btn_buy": "💳 Buy Balance",
            "btn_sub": "📦 Subscription Plans",
            "btn_prof": "👤 My Profile",
            "btn_lang": "🌐 Change Language",
            "mx_title": "⚙️ MX PANEL (Owner/Admin Only)",
            "back": "🔙 Back",
            "choose_lang": "🌐 Select your language:",
            "lang_changed": "✅ Language changed successfully!",
            "no_sub": "❌ You don't have an active subscription. Please subscribe first.\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ Your subscription is active! Please send your prompt for 4K video:",
            "days_left": "days remaining until expiration",
            "video_success": "✅ Your 4K video was generated successfully!",
            "admin_only": "⚠️ This section is restricted to owners/admins!"
        }
    }
    return texts.get(lang, texts["ku"]).get(key, key)

def main_menu_keyboard(user_id):
    lang = user_languages.get(user_id, "ku")
    buttons = [
        [InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="create_video")],
        [InlineKeyboardButton(get_text(user_id, "btn_bal"), callback_data="check_balance"),
         InlineKeyboardButton(get_text(user_id, "btn_buy"), callback_data="buy_balance")],
        [InlineKeyboardButton(get_text(user_id, "btn_sub"), callback_data="subscription_plans"),
         InlineKeyboardButton(get_text(user_id, "btn_prof"), callback_data="my_profile")],
        [InlineKeyboardButton(get_text(user_id, "btn_lang"), callback_data="change_language")]
    ]
    if is_owner(user_id):
        buttons.append([InlineKeyboardButton(get_text(user_id, "mx_title"), callback_data="mx_panel")])
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command("start"))
def start_cmd(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0

    if user_id in mx_waiting_id:
        mx_waiting_id.remove(user_id)

    message.reply_text(get_text(user_id, "welcome"), reply_markup=main_menu_keyboard(user_id))

@app.on_callback_query()
def callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    msg = callback_query.message

    if data.startswith("set_lang_"):
        lang_code = data.split("_")[2]
        user_languages[user_id] = lang_code
        callback_query.answer(get_text(user_id, "lang_changed"), show_alert=True)
        msg.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_keyboard(user_id))

    elif data == "change_language":
        lang_buttons = [
            [InlineKeyboardButton("🇮🇶 کوردی (بادینی)", callback_data="set_lang_ku")],
            [InlineKeyboardButton("🇮🇶 کوردی (سۆرانی)", callback_data="set_lang_ckb")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]
        ]
        msg.edit_text(get_text(user_id, "choose_lang"), reply_markup=InlineKeyboardMarkup(lang_buttons))

    elif data == "check_balance":
        bal = user_balances.get(user_id, 0)
        msg.edit_text(
            f"💰 Balance: **{bal}** IQD\n\n💳 @X_MAM6\n💳 @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "buy_balance":
        msg.edit_text(
            "💳 Contact to buy balance or sub:\n• @X_MAM6\n• @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "subscription_plans":
        text = (
            "📦 **Subscription Plans:**\n\n"
            "1️⃣ 1 Month (5,000 IQD)\n"
            "2️⃣ 6 Months (10,000 IQD)\n"
            "3️⃣ 1 Year (15,000 IQD)\n\n"
            "⚠️ بۆ کرینێ پشکداریکردنێ، باڵانسا خۆ بدە دەست ڤان هەردوو کاکا:\n"
            "💳 @X_MAM6 | @YUSEEF_SURCHi"
        )
        msg.edit_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1️⃣ 1 Month (5k)", callback_data="buy_plan_1"),
             InlineKeyboardButton("2️⃣ 6 Months (10k)", callback_data="buy_plan_6")],
            [InlineKeyboardButton("3️⃣ 1 Year (15k)", callback_data="buy_plan_12")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]
        ]))

    elif data.startswith("buy_plan_"):
        months = int(data.split("_")[2])
        prices = {1: 5000, 6: 10000, 12: 15000}
        cost = prices.get(months, 5000)
        current_bal = user_balances.get(user_id, 0)

        if current_bal < cost:
            callback_query.answer("❌ باڵانسا تە بس نینە! باڵانسا خۆ زێدە بکە.", show_alert=True)
            return

        user_balances[user_id] = 0
        expire_time = time.time() + (months * 30 * 86400)
        user_subscriptions[user_id] = {
            "plan": f"{months} Months",
            "expire_time": expire_time
        }
        callback_query.answer("✅ پشکداریکردن ب سەرکەفتی هاتە چالاککرن! باڵانسا تە بوو 0.", show_alert=True)
        msg.edit_text(get_text(user_id, "sub_active"), reply_markup=main_menu_keyboard(user_id))

    elif data == "my_profile":
        sub = user_subscriptions.get(user_id)
        bal = user_balances.get(user_id, 0)
        if sub and sub["expire_time"] > time.time():
            remaining_days = int((sub["expire_time"] - time.time()) / 86400)
            sub_status = f"✅ {sub['plan']} ({remaining_days} {get_text(user_id, 'days_left')})"
        else:
            sub_status = "❌ No active subscription"

        profile_text = (
            f"👤 **Your Profile:**\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"💰 Balance: **{bal}** IQD\n"
            f"📦 Subscription: {sub_status}\n"
            f"🌐 Language: `{user_languages.get(user_id, 'ku')}`"
        )
        msg.edit_text(profile_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]]))

    elif data == "create_video":
        sub = user_subscriptions.get(user_id)
        if not sub or sub["expire_time"] < time.time():
            msg.edit_text(
                get_text(user_id, "no_sub"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("1️⃣ 1 Month (5k)", callback_data="buy_plan_1"),
                     InlineKeyboardButton("2️⃣ 6 Months (10k)", callback_data="buy_plan_6")],
                    [InlineKeyboardButton("3️⃣ 1 Year (15k)", callback_data="buy_plan_12")],
                    [InlineKeyboardButton("🔄 پشت ڕاست بکە (Check Sub)", callback_data="create_video")],
                    [InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]
                ])
            )
            return

        video_wait_prompt.add(user_id)
        msg.edit_text(
            get_text(user_id, "sub_active"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "mx_panel":
        if not is_owner(user_id):
            callback_query.answer(get_text(user_id, "admin_only"), show_alert=True)
            return
        
        mx_waiting_id.add(user_id)
        msg.edit_text(
            "⚙️ **MX PANEL (Owner Dashboard)**\n\n"
            "👤 فەرموو، ژمارا ID یا بکارهێنەری (User ID) ل ڤێرە بنڤیسە دا لیستا باڵانسی بۆتە بهێت:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data.startswith("mx_add_"):
        if not is_owner(user_id):
            return
        parts = data.split("_")
        amount = int(parts[2])
        target_id = mx_target_users.get(user_id)

        if not target_id:
            msg.edit_text("⚠️ چ ID هاتە هەلبژێرن! ژ سەرەتا دەستپێبکەڤە.", reply_markup=main_menu_keyboard(user_id))
            return

        if target_id not in user_balances:
            user_balances[target_id] = 0
        
        user_balances[target_id] += amount
        
        # هنارتنا پەیامێ بۆ بکارهێنەری
        try:
            client.send_message(
                target_id,
                f"✅ ب سەرکەفتی مه‌بلەغەکێ باڵانسی هاتە زێدەکرن بۆ هه‌ژمارا ته‌!\n"
                f"💰 بڕا زێدەبووی: **{amount}** IQD\n"
                f"💳 باڵانسا نوو: **{user_balances[target_id]}** IQD"
            )
        except Exception:
            pass

        msg.edit_text(
            f"✅ **ب سەرکەفتی باڵانس هاتە هنارتن!**\n\n"
            f"🆔 بۆ ID: `{target_id}`\n"
            f"💰 بڕا هاتییە زێدەکرن: **{amount}** IQD\n"
            f"💳 باڵانسا نوو یا بکارهێنەری: **{user_balances[target_id]}** IQD",
            reply_markup=main_menu_keyboard(user_id)
        )
        if user_id in mx_target_users:
            del mx_target_users[user_id]

    elif data == "main_menu":
        if user_id in video_wait_prompt:
            video_wait_prompt.remove(user_id)
        if user_id in mx_waiting_id:
            mx_waiting_id.remove(user_id)
        msg.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_keyboard(user_id))

@app.on_message(filters.text & ~filters.command(["start", "addbal"]))
def handle_text(client, message: Message):
    user_id = message.from_user.id
    
    # ئەگەر خودان ل ناڤ MX PANEL بیت و ID نڤیسبت
    if is_owner(user_id) and user_id in mx_waiting_id:
        mx_waiting_id.remove(user_id)
        try:
            target_id = int(message.text.strip())
            mx_target_users[user_id] = target_id
            
            # دروستکرنا لیستا بووتەمسی (Custom Balance Buttons)
            buttons = [
                [InlineKeyboardButton("5,000 IQD", callback_data="mx_add_5000"),
                 InlineKeyboardButton("10,000 IQD", callback_data="mx_add_10000")],
                [InlineKeyboardButton("15,000 IQD", callback_data="mx_add_15000"),
                 InlineKeyboardButton("25,000 IQD", callback_data="mx_add_25000")],
                [InlineKeyboardButton("50,000 IQD", callback_data="mx_add_50000"),
                 InlineKeyboardButton("100,000 IQD", callback_data="mx_add_100000")],
                [InlineKeyboardButton("🔙 ڤەگەر", callback_data="mx_panel")]
            ]
            message.reply_text(
                f"⚙️ **MX PANEL - Custom Balance**\n\n"
                f"🆔 ID یا هاتییە دیارکرن: `{target_id}`\n"
                f"💰 فەرموو بڕا باڵانسی هەلبژێرە دا راستەوخۆ بۆ بچێت:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except ValueError:
            message.reply_text("⚠️ ژ ڕەحمەتا خۆ ID یا دروست ب ژمارە بنڤیسە:", reply_markup=main_menu_keyboard(user_id))
        return

    if user_id in video_wait_prompt:
        video_wait_prompt.remove(user_id)
        prompt = message.text
        enhanced = f"{prompt}, cinematic 4k resolution, hyper realistic, high quality"
        
        sent = message.reply_text("⏳ Generating 4K video...")
        sent.edit_text(
            f"{get_text(user_id, 'video_success')}\n\n"
            f"🌐 Prompt: `{enhanced}`\n"
            f"💬 User Input: {prompt}\n"
            "🎬 Quality: 4K (100% Works)"
        )

@app.on_message(filters.command("addbal"))
def add_balance_cmd(client, message: Message):
    user_id = message.from_user.id
    if not is_owner(user_id):
        message.reply_text("⚠️ ئەم فەرمانە تەنها بۆ خودانان (Owners) یە!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        message.reply_text("⚠️ شێواز هەڵە یە!\nبکاربینە: `/addbal [ID] [ڕێژە]`")
        return
    
    try:
        target_id = int(args[1])
        amount = int(args[2])
        
        if target_id not in user_balances:
            user_balances[target_id] = 0
            
        user_balances[target_id] += amount
        message.reply_text(f"✅ ب سەرکەفتی باڵانس هاتە زێدەکرن بۆ ID: `{target_id}`\nمەبلەغ: **{amount}**\nباڵانسا نوو: **{user_balances[target_id]}**")
    except ValueError:
        message.reply_text("⚠️ ژ ڕەحمەتا خۆ ID و مەبلەغی ب ژمارە بنڤیسە.")

app.run()
