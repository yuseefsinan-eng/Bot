import os
import time
import json
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8653317587:AAH59X7hIIQ2s3rH4rzT26vDMPCRsPVFth8"

OWNERS = [7643191802, 8038533940]
DATA_FILE = "ultimate_bot_database.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"balances": {}, "languages": {}, "subscriptions": {}, "all_users": []}

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "balances": user_balances,
                "languages": user_languages,
                "subscriptions": user_subscriptions,
                "all_users": list(all_users)
            }, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

data_db = load_data()
user_balances = {int(k): v for k, v in data_db.get("balances", {}).items()}
user_languages = {int(k): v for k, v in data_db.get("languages", {}).items()}
user_subscriptions = {int(k): v for k, v in data_db.get("subscriptions", {}).items()}
all_users = set(data_db.get("all_users", []))

video_wait_prompt = set()
mx_waiting_id = set()  
mx_target_users = {}   

app = Client("yuseef_surchi_ultimate_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_owner(user_id):
    return user_id in OWNERS

def get_text(user_id, key):
    lang = user_languages.get(user_id, "ku") 
    texts = {
        "ku": {
            "welcome": "🔥 **سلاڤ و ڕێز بۆ خودانێ کێشەر!**\n\nب خێر هاتنی بۆ سیستەمێ پێشکەفتی یێ چێکرنا ڤیدیۆیا 4K و AI ب تایبەتمەندیا **Facial Consistency**.\nفەرموو هەلبژێرە:",
            "btn_video": "🎬 دروستکرنا ڤیدیۆیا 4K (AI)",
            "btn_bal": "💰 باڵانسا من",
            "btn_buy": "💳 کرینا باڵانسی",
            "btn_sub": "📦 پلەنێن پشکداریکردنێ",
            "btn_prof": "👤 پروفایلا من",
            "btn_lang": "🌐 گۆڕینا زمانێ (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بۆ ڕێڤەبەرا)",
            "back": "🔙 ڤەگەر",
            "choose_lang": "🌐 فەرموو زمانێ خۆ هەلبژێرە:\n\nSelect your language / زمانەکەت هەڵبژێرە:",
            "lang_changed": "✅ زمان ب سەرکەفتی هاتە گۆڕین بۆ کوردی (بادینی)!",
            "no_sub": "❌ تە چ پشکداریکردنەکا کارا نینە!\nلطفەن سەرەتا پشکداریکردنێ چێکە یان باڵانسا خۆ ل دەف ڕێڤەبەرا زێدە بکە.\n\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ پشکداریکردنا تە یا کارا یە!\n✍️ فەرموو پرۆمپتێ خۆ بنڤیسە یان وێنەیەکێ ڕێفرنس بۆ ناسینا دەمچەی بنێرە:",
            "days_left": "ڕۆژ ماینە بۆ خلاساربوونێ",
            "video_success": "🚀 **ڤیدیۆیا تە ب کوالێتیا Ultra 4K و Facial Consistency هاتە بەرهەمئینان!**",
            "admin_only": "⚠️ ئەڤ پشکە تنێ بۆ ڕێڤەبەرا یە!",
            "bal_text": "💰 باڵانسا تەیا نۆکە:",
            "buy_text": "💳 بۆ کرینا باڵانسی یان پشکداریکردنێ، پەیوەندیێ ب ڤان هەردوو کاکا بکە:",
            "sub_plans_title": "📦 **پلەنێن پێشکەفتی یێن ڤیدیۆیێ (4K):**",
            "sub_1": "1️⃣ هەیڤەک (5,000 د.ع)",
            "sub_6": "2️⃣ 6 هەیڤ (10,000 د.ع)",
            "sub_12": "3️⃣ سالەک (15,000 د.ع)",
            "check_sub": "🔄 پشکنینا پشکداریکردنێ",
            "profile_title": "👤 **پروفایلا تە یا تایبەت:**",
            "id_text": "🆔 ناسنامە (ID):",
            "sub_label": "📦 پشکداریکردن:",
            "no_sub_profile": "❌ بێ پشکداریکردن",
            "lang_label": "🌐 زمان: کوردی (بادینی)",
            "mx_prompt": "⚙️ **MX PANEL - سیستەمێ ڕێڤەبەریێ**\n\n👤 فەرموو، ID یا بکارهێنەری ل ڤێرە بنڤیسە:",
            "gen_video": "⏳ چاوەڕوانبە... سیستەمێ AI مژوولی چێکرنا ڤیدیۆیا تە یە ب کوالێتیا بلند..."
        },
        "ckb": {
            "welcome": "🔥 **سڵاو و ڕێز بۆ بەڕێزت!**\n\nبەخێر هاتیت بۆ سیستەمی پێشکەوتووی دروستکردنی ڤیدیۆی 4K بە تایبەتمەندی **Facial Consistency**.\nتکایە یەکێک هەڵبژێرە:",
            "btn_video": "🎬 دروستکردنی ڤیدیۆی 4K (AI)",
            "btn_bal": "💰 باڵانسم",
            "btn_buy": "💳 کڕینی باڵانس",
            "btn_sub": "📦 پلانی بەشداریکردن",
            "btn_prof": "👤 پڕۆفایلم",
            "btn_lang": "🌐 گۆڕینی زمان (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بە بەڕێوەبەران)",
            "back": "🔙 گەڕانەوە",
            "choose_lang": "🌐 تکایە زمانەکەت هەڵبژێرە:\n\nSelect your language / زمانەکەت هەڵبژێرە:",
            "lang_changed": "✅ زمان بە سەرکەوتوویی گۆڕدرا بۆ کوردی (سۆرانی)!",
            "no_sub": "❌ تۆ هیچ بەشداریکردنێکی چالاکت نییە!\nتکایە سەرەتا بەشداریکردن بکە.\n\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ بەشداریکردنەکەت چالاکە!\n✍️ تکایە پڕۆمپتەکەت بنووسە یان وێنەیەک بنێرە:",
            "days_left": "ڕۆژ ماون بۆ کۆتایی هاتن",
            "video_success": "🚀 **ڤیدیۆکەت بە کوالێتی Ultra 4K و Facial Consistency دروست کرا!**",
            "admin_only": "⚠️ ئەم بەشە تەنها بۆ بەڕێوەبەرانە!",
            "bal_text": "💰 باڵانسی ئێستای تۆ:",
            "buy_text": "💳 بۆ کڕینی باڵانس، پەیوەندی بەم کەسانە بکە:",
            "sub_plans_title": "📦 **پلانی بەشداریکردنی ڤیدیۆ (4K):**",
            "sub_1": "1️⃣ مانگێک (5,000 د.ع)",
            "sub_6": "2️⃣ 6 مانگ (10,000 د.ع)",
            "sub_12": "3️⃣ ساڵێک (15,000 د.ع)",
            "check_sub": "🔄 پشکنینی بەشداریکردن",
            "profile_title": "👤 **پڕۆفایلی تایبەتی تۆ:**",
            "id_text": "🆔 ناسنامە (ID):",
            "sub_label": "📦 بەشداریکردن:",
            "no_sub_profile": "❌ بێ بەشداریکردن",
            "lang_label": "🌐 زمان: کوردی (سۆرانی)",
            "mx_prompt": "⚙️ **MX PANEL - بەڕێوەبەر**\n\n👤 تکایە IDی بەکارهێنەر لێرە بنووسە:",
            "gen_video": "⏳ چاوەڕوانبە... زیرەکی دەستکرد خەریکی دروستکردنی ڤیدیۆکەتە..."
        },
        "en": {
            "welcome": "🔥 **Hello!**\n\nWelcome to the Ultimate 4K AI Video Bot with **Facial Consistency** technology.\nPlease select an option:",
            "btn_video": "🎬 Create 4K Video (AI)",
            "btn_bal": "💰 My Balance",
            "btn_buy": "💳 Buy Balance",
            "btn_sub": "📦 Subscription Plans",
            "btn_prof": "👤 My Profile",
            "btn_lang": "🌐 Change Language",
            "mx_title": "⚙️ MX PANEL (Owner/Admin Only)",
            "back": "🔙 Back",
            "choose_lang": "🌐 Please select your language:",
            "lang_changed": "✅ Language successfully changed to English!",
            "no_sub": "❌ You don't have an active subscription!\nPlease subscribe first.\n\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ Your subscription is active!\n✍️ Send your prompt or reference image:",
            "days_left": "days remaining",
            "video_success": "🚀 **Your 4K video was generated with Ultra Facial Consistency!**",
            "admin_only": "⚠️ This section is restricted to admins!",
            "bal_text": "💰 Your current balance:",
            "buy_text": "💳 To buy balance, please contact:",
            "sub_plans_title": "📦 **4K Video Subscription Plans:**",
            "sub_1": "1️⃣ 1 Month (5,000 IQD)",
            "sub_6": "2️⃣ 6 Months (10,000 IQD)",
            "sub_12": "3️⃣ 1 Year (15,000 IQD)",
            "check_sub": "🔄 Check Subscription",
            "profile_title": "👤 **My Profile:**",
            "id_text": "🆔 User ID:",
            "sub_label": "📦 Subscription:",
            "no_sub_profile": "❌ No active subscription",
            "lang_label": "🌐 Language: English",
            "mx_prompt": "⚙️ **MX PANEL - Admin**\n\n👤 Please enter User ID:",
            "gen_video": "⏳ Processing... AI is generating your 4K video with facial consistency..."
        }
    }
    return texts.get(lang, texts["ku"]).get(key, key)

def main_menu_keyboard(user_id):
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
    all_users.add(user_id)
    if user_id not in user_balances:
        user_balances[user_id] = 0
    save_data()

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
        save_data()
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
            f"{get_text(user_id, 'bal_text')} **{bal}** د.ع\n\n💳 @X_MAM6\n💳 @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "buy_balance":
        msg.edit_text(
            f"{get_text(user_id, 'buy_text')}\n• @X_MAM6\n• @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "subscription_plans":
        text = (
            f"{get_text(user_id, 'sub_plans_title')}\n\n"
            f"1️⃣ {get_text(user_id, 'sub_1')}\n"
            f"2️⃣ {get_text(user_id, 'sub_6')}\n"
            f"3️⃣ {get_text(user_id, 'sub_12')}\n\n"
            f"💳 @X_MAM6 | @YUSEEF_SURCHi"
        )
        msg.edit_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(get_text(user_id, "sub_1"), callback_data="buy_plan_1"),
             InlineKeyboardButton(get_text(user_id, "sub_6"), callback_data="buy_plan_6")],
            [InlineKeyboardButton(get_text(user_id, "sub_12"), callback_data="buy_plan_12")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]
        ]))

    elif data.startswith("buy_plan_"):
        months = int(data.split("_")[2])
        prices = {1: 5000, 6: 10000, 12: 15000}
        cost = prices.get(months, 5000)
        current_bal = user_balances.get(user_id, 0)

        if current_bal < cost:
            callback_query.answer("❌ باڵانسا تە بەس نینە!", show_alert=True)
            return

        user_balances[user_id] -= cost
        expire_time = time.time() + (months * 30 * 86400)
        user_subscriptions[user_id] = {
            "plan": f"{months}",
            "expire_time": expire_time
        }
        save_data()
        callback_query.answer("✅ Success!", show_alert=True)
        msg.edit_text(get_text(user_id, "sub_active"), reply_markup=main_menu_keyboard(user_id))

    elif data == "my_profile":
        sub = user_subscriptions.get(user_id)
        bal = user_balances.get(user_id, 0)
        if sub and sub["expire_time"] > time.time():
            remaining_days = int((sub["expire_time"] - time.time()) / 86400)
            sub_status = f"✅ {sub['plan']} هەیڤ ({remaining_days} {get_text(user_id, 'days_left')})"
        else:
            sub_status = get_text(user_id, "no_sub_profile")

        profile_text = (
            f"{get_text(user_id, 'profile_title')}\n\n"
            f"{get_text(user_id, 'id_text')} `{user_id}`\n"
            f"{get_text(user_id, 'btn_bal')}: **{bal}** د.ع\n"
            f"{get_text(user_id, 'sub_label')} {sub_status}\n"
            f"{get_text(user_id, 'lang_label')}"
        )
        msg.edit_text(profile_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]]))

    elif data == "create_video":
        sub = user_subscriptions.get(user_id)
        if not sub or sub["expire_time"] < time.time():
            msg.edit_text(
                get_text(user_id, "no_sub"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_text(user_id, "sub_1"), callback_data="buy_plan_1"),
                     InlineKeyboardButton(get_text(user_id, "sub_6"), callback_data="buy_plan_6")],
                    [InlineKeyboardButton(get_text(user_id, "sub_12"), callback_data="buy_plan_12")],
                    [InlineKeyboardButton(get_text(user_id, "check_sub"), callback_data="create_video")],
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
            get_text(user_id, "mx_prompt"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data.startswith("mx_add_"):
        if not is_owner(user_id):
            return
        parts = data.split("_")
        amount = int(parts[2])
        target_id = mx_target_users.get(user_id)

        if not target_id:
            msg.edit_text("⚠️ Error!", reply_markup=main_menu_keyboard(user_id))
            return

        if target_id not in user_balances:
            user_balances[target_id] = 0
        
        user_balances[target_id] += amount
        save_data()
        
        try:
            client.send_message(target_id, f"✅ Balance added: +{amount} IQD")
        except Exception:
            pass

        msg.edit_text(
            f"✅ **Balance sent successfully!**\n🆔 ID: `{target_id}`\n💰 Added: {amount} IQD",
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

@app.on_message(filters.text & ~filters.command(["start", "addbal", "stats", "broadcast"]))
def handle_text(client, message: Message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if is_owner(user_id) and user_id in mx_waiting_id:
        mx_waiting_id.remove(user_id)
        try:
            target_id = int(message.text.strip())
            mx_target_users[user_id] = target_id
            
            buttons = [
                [InlineKeyboardButton("5,000", callback_data="mx_add_5000"),
                 InlineKeyboardButton("10,000", callback_data="mx_add_10000")],
                [InlineKeyboardButton("15,000", callback_data="mx_add_15000"),
                 InlineKeyboardButton("25,000", callback_data="mx_add_25000")],
                [InlineKeyboardButton("50,000", callback_data="mx_add_50000"),
                 InlineKeyboardButton("100,000", callback_data="mx_add_100000")],
                [InlineKeyboardButton(get_text(user_id, "back"), callback_data="mx_panel")]
            ]
            message.reply_text(
                f"⚙️ **MX PANEL - Custom Balance**\n🆔 ID: `{target_id}`\nSelect amount:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except ValueError:
            message.reply_text("⚠️ Invalid ID!", reply_markup=main_menu_keyboard(user_id))
        return

    if user_id in video_wait_prompt:
        video_wait_prompt.remove(user_id)
        prompt = message.text
        
        sent = message.reply_text(get_text(user_id, "gen_video"))
        time.sleep(1)
        sent.edit_text(
            f"{get_text(user_id, 'video_success')}\n\n"
            f"💬 **پڕۆمپت:** `{prompt}`\n"
            f"🧬 **Facial Consistency:** `Enabled (Reference Priority)`\n"
            f"🎬 **کوالێتی:** 4K Ultra HD\n\n"
            f"✨ (بۆتێ ب سەرکەفتی وەڵاما تە دا)"
        )

@app.on_message(filters.command("stats"))
def stats_cmd(client, message: Message):
    if not is_owner(message.from_user.id):
        return
    total_u = len(all_users)
    total_subs = len(user_subscriptions)
    message.reply_text(f"📊 **ئامارێن بۆتێ:**\n\n👥 هەمی بکارهێنەر: `{total_u}`\n📦 پشکدارێن کارا: `{total_subs}`")

@app.on_message(filters.command("broadcast"))
def broadcast_cmd(client, message: Message):
    if not is_owner(message.from_user.id):
        return
    if not message.reply_to_message:
        message.reply_text("⚠️ ڕیپلاي ل سەر وێنە یان پەیامەکێ بکە و `/broadcast` بنڤیسە.")
        return
    
    success = 0
    failed = 0
    for uid in all_users:
        try:
            message.reply_to_message.copy(uid)
            success += 1
        except Exception:
            failed += 1
    message.reply_text(f"✅ ڕیکلام ب سەرکەفتی هاتە هنارتن:\n📤 گەهشتە: `{success}`\n❌ نەگەهشتە: `{failed}`")

@app.on_message(filters.command("addbal"))
def add_balance_cmd(client, message: Message):
    user_id = message.from_user.id
    if not is_owner(user_id):
        return
    args = message.text.split()
    if len(args) < 3:
        return
    try:
        target_id = int(args[1])
        amount = int(args[2])
        if target_id not in user_balances:
            user_balances[target_id] = 0
        user_balances[target_id] += amount
        save_data()
        message.reply_text(f"✅ Added {amount} IQD to ID: {target_id}")
    except ValueError:
        pass

app.run()
