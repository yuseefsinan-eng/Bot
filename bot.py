import os
import time
import json
import threading
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from openai import OpenAI

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8653317587:AAH59X7hIIQ2s3rH4rzT26vDMPCRsPVFth8"

# 🔑 کلیلا OpenAI ya تە ل ڤێرە هاتە دانان
OPENAI_API_KEY = "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"
client_ai = OpenAI(api_key=OPENAI_API_KEY)

OWNERS = [7643191802, 8038533940]
DATA_FILE = "ultimate_master_bot_db_v5.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"balances": {}, "languages": {}, "subscriptions": {}, "all_users": [], "user_info": {}}

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "balances": user_balances,
                "languages": user_languages,
                "subscriptions": user_subscriptions,
                "all_users": list(all_users),
                "user_info": user_info
            }, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

data_db = load_data()
user_balances = {int(k): v for k, v in data_db.get("balances", {}).items()}
user_languages = {int(k): v for k, v in data_db.get("languages", {}).items()}
user_subscriptions = {int(k): v for k, v in data_db.get("subscriptions", {}).items()}
user_info = {int(k): v for k, v in data_db.get("user_info", {}).items()}
all_users = set(data_db.get("all_users", []))

video_wait_prompt = set()
mx_waiting_id = set()  
mx_target_users = {}   
broadcast_waiting_id = set()

app = Client("yuseef_surchi_master_bot_v5", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_owner(user_id):
    return user_id in OWNERS

def get_text(user_id, key):
    lang = user_languages.get(user_id, "ku") 
    texts = {
        "ku": {
            "welcome": "🔥 **سلاڤ و ڕێز بۆ خودانێ کێشەر!**\n\nب خێر هاتنی بۆ سیستەمێ مەزنێ چێکرنا ڤیدیۆیا 4K و AI ب تایبەتمەندیا **Facial Consistency**.\nفەرموو هەلبژێرە:",
            "btn_video": "🎬 دروستکرنا ڤیدیۆیا 4K (AI)",
            "btn_bal": "💰 باڵانسا من",
            "btn_buy": "💳 کرینا باڵانسی",
            "btn_sub": "📦 پلەنێن پشکداریکردنێ",
            "btn_prof": "👤 پروفایلا من",
            "btn_lang": "🌐 گۆڕینا زمانێ (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بۆ ڕێڤەبەرا)",
            "mx_broadcast": "📢 هنارتنا ڕیکلامان بۆ هەمیان",
            "back": "🔙 ڤەگەر بۆ سەرەکی",
            "choose_lang": "🌐 فەرموو زمانێ خۆ هەلبژێرە:\n\nSelect your language / اختر لغتك / زمانەکەت هەڵبژێرە:",
            "lang_changed": "✅ زمان ب سەرکەفتی هاتە گۆڕین بۆ کوردی (بادینی)!",
            "no_sub": "❌ تە چ پشکداریکردنەکا کارا نینە!\nلطفەن سەرەتا پشکداریکردنێ چێکە یان باڵانسا خۆ ل دەف ڕێڤەبەرا زێدە بکە.\n\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ پشکداریکردنا تە یا کارا یە!\n✍️ فەرموو پرۆمپتێ خۆ بنڤیسە یان وێنەیەکێ ڕێفرنس بۆ ناسینا دەمچەی بنێرە:",
            "days_left": "ڕۆژ ماینە بۆ خلاساربوونێ",
            "video_success": "🚀 **وەڵاما ژێرەکیا دەستکرد (OpenAI) بۆ پڕۆمپتێ تە:**",
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
            "mx_prompt": "⚙️ **MX PANEL - کۆنترۆلا ڕێڤەبەریێ**\n\n👤 فەرموو، ID یا بکارهێنەری ل ڤێرە بنڤیسە دا زانیاریێن وی ببینن و باڵانسی بۆ زێدە بکەی:",
            "gen_video": "⏳ چاوەڕوانبە... ژێرەکیا دەستکرد مژوولی تشتکرنا وەڵاما تە یە..."
        },
        "ckb": {
            "welcome": "🔥 **سڵاو و ڕێز بۆ بەڕێزت!**\n\nبەخێر هاتیت بۆ سیستەمی پێشکەوتووی دروستکردنی ڤیدیۆی 4K.\nتکایە یەکێک هەڵبژێرە:",
            "btn_video": "🎬 دروستکردنی ڤیدیۆی 4K (AI)",
            "btn_bal": "💰 باڵانسم",
            "btn_buy": "💳 کڕینی باڵانس",
            "btn_sub": "📦 پلانی بەشداریکردن",
            "btn_prof": "👤 پڕۆفایلم",
            "btn_lang": "🌐 گۆڕینی زمان (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بە بەڕێوەبەران)",
            "mx_broadcast": "📢 ناردنی ڕیکلام بۆ گشت بەکارهێنەران",
            "back": "🔙 گەڕانەوە بۆ سەرەکی",
            "choose_lang": "🌐 تکایە زمانەکەت هەڵبژێرە:",
            "lang_changed": "✅ زمان بە سەرکەوتوویی گۆڕدرا بۆ کوردی (سۆرانی)!",
            "no_sub": "❌ تۆ هیچ بەشداریکردنێکی چالاکت نییە!\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ بەشداریکردنەکەت چالاکە!\n✍️ تکایە پڕۆمپتەکەت بنووسە:",
            "days_left": "ڕۆژ ماون بۆ کۆتایی هاتن",
            "video_success": "🚀 **وەڵامی زیرەکی دەستکرد (OpenAI):**",
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
            "mx_prompt": "⚙️ **MX PANEL**\n\n👤 تکایە IDی بەکارهێنەر لێرە بنووسە:",
            "gen_video": "⏳ چاوەڕوانبە..."
        },
        "ar": {
            "welcome": "🔥 **أهلاً بك!**\n\nيرجى اختيار أحد الخيارات:",
            "btn_video": "🎬 إنشاء فيديو 4K (AI)",
            "btn_bal": "💰 رصيدي",
            "btn_buy": "💳 شراء رصيد",
            "btn_sub": "📦 خطط الاشتراكات",
            "btn_prof": "👤 ملفي الشخصي",
            "btn_lang": "🌐 تغيير اللغة",
            "mx_title": "⚙️ MX PANEL",
            "mx_broadcast": "📢 إرسال إعلان",
            "back": "🔙 رجوع",
            "choose_lang": "🌐 اختر لغتك:",
            "lang_changed": "✅ تم تغيير اللغة!",
            "no_sub": "❌ ليس لديك اشتراك نشط!",
            "sub_active": "✅ اشتراكك نشط! أرسل الوصف:",
            "days_left": "أيام متبقية",
            "video_success": "🚀 **رد الذكاء الاصطناعي (OpenAI):**",
            "admin_only": "⚠️ للمشرفين فقط!",
            "bal_text": "💰 رصيدك:",
            "buy_text": "💳 لشراء رصيد:",
            "sub_plans_title": "📦 **الاشتراكات:**",
            "sub_1": "1️⃣ شهر (5,000 د.ع)",
            "sub_6": "2️⃣ 6 أشهر (10,000 د.ع)",
            "sub_12": "3️⃣ سنة (15,000 د.ع)",
            "check_sub": "🔄 تحقق",
            "profile_title": "👤 **ملفك:**",
            "id_text": "🆔 ID:",
            "sub_label": "📦 الاشتراك:",
            "no_sub_profile": "❌ بدون اشتراك",
            "lang_label": "🌐 اللغة: العربية",
            "mx_prompt": "⚙️ أدخل ID المستخدم:",
            "gen_video": "⏳ جاري المعالجة..."
        },
        "en": {
            "welcome": "🔥 **Hello!**\nPlease select an option:",
            "btn_video": "🎬 Create 4K Video (AI)",
            "btn_bal": "💰 My Balance",
            "btn_buy": "💳 Buy Balance",
            "btn_sub": "📦 Subscription Plans",
            "btn_prof": "👤 My Profile",
            "btn_lang": "🌐 Change Language",
            "mx_title": "⚙️ MX PANEL",
            "mx_broadcast": "📢 Broadcast",
            "back": "🔙 Back",
            "choose_lang": "🌐 Select language:",
            "lang_changed": "✅ Language changed!",
            "no_sub": "❌ No active subscription!",
            "sub_active": "✅ Subscription active! Send prompt:",
            "days_left": "days remaining",
            "video_success": "🚀 **OpenAI Response:**",
            "admin_only": "⚠️ Admins only!",
            "bal_text": "💰 Balance:",
            "buy_text": "💳 Contact:",
            "sub_plans_title": "📦 **Plans:**",
            "sub_1": "1️⃣ 1 Month (5,000 IQD)",
            "sub_6": "2️⃣ 6 Months (10,000 IQD)",
            "sub_12": "3️⃣ 1 Year (15,000 IQD)",
            "check_sub": "🔄 Check",
            "profile_title": "👤 **Profile:**",
            "id_text": "🆔 ID:",
            "sub_label": "📦 Subscription:",
            "no_sub_profile": "❌ No subscription",
            "lang_label": "🌐 Language: English",
            "mx_prompt": "⚙️ Enter User ID:",
            "gen_video": "⏳ Processing..."
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
        buttons.append([InlineKeyboardButton(get_text(user_id, "mx_broadcast"), callback_data="mx_broadcast_start")])
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command("start"))
def start_cmd(client, message: Message):
    user = message.from_user
    user_id = user.id
    all_users.add(user_id)
    
    user_info[user_id] = {
        "username": f"@{user.username}" if user.username else "بێ یۆزەرنەم",
        "nickname": f"{user.first_name} {user.last_name or ''}".strip()
    }

    if user_id not in user_balances:
        user_balances[user_id] = 0
    save_data()

    if user_id in mx_waiting_id:
        mx_waiting_id.remove(user_id)
    if user_id in broadcast_waiting_id:
        broadcast_waiting_id.remove(user_id)

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
            [InlineKeyboardButton("🇮🇶 العربية", callback_data="set_lang_ar")],
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
        current_time = time.time()
        existing_sub = user_subscriptions.get(user_id)
        
        days_to_add = months * 30
        if existing_sub and existing_sub["expire_time"] > current_time:
            expire_time = existing_sub["expire_time"] + (days_to_add * 86400)
            total_months = int(existing_sub.get("months_count", 1) + months)
        else:
            expire_time = current_time + (days_to_add * 86400)
            total_months = months

        user_subscriptions[user_id] = {
            "plan": f"{total_months} مانگ/هەیڤ",
            "expire_time": expire_time,
            "months_count": total_months
        }
        save_data()
        callback_query.answer("✅ Success! Subscription Activated.", show_alert=True)
        msg.edit_text(get_text(user_id, "sub_active"), reply_markup=main_menu_keyboard(user_id))

    elif data == "my_profile":
        sub = user_subscriptions.get(user_id)
        bal = user_balances.get(user_id, 0)
        if sub and sub["expire_time"] > time.time():
            remaining_days = int((sub["expire_time"] - time.time()) / 86400)
            sub_status = f"✅ {sub['plan']} ({remaining_days} {get_text(user_id, 'days_left')})"
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

    elif data == "mx_broadcast_start":
        if not is_owner(user_id):
            callback_query.answer(get_text(user_id, "admin_only"), show_alert=True)
            return
        broadcast_waiting_id.add(user_id)
        msg.edit_text(
            "📢 **هنارتنا ڕیکلام / Broadcast**\n\nفەرموو ئەو پەیامە لێرە بنێرە:",
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
            client.send_message(
                target_id, 
                f"🎉 **پیرۆزە! باڵانس هاتە زیادکرن.**\n💰 `+{amount} د.ع`\n💳 باڵانسا نۆکە: `{user_balances[target_id]} د.ع`"
            )
        except Exception:
            pass

        msg.edit_text(
            f"✅ **باڵانس ب سەرکەفتی هاتە هنارتن!**\n🆔 ID: `{target_id}`\n💰 نوو: `{user_balances[target_id]} د.ع`",
            reply_markup=main_menu_keyboard(user_id)
        )
        if user_id in mx_target_users:
            del mx_target_users[user_id]

    elif data == "main_menu":
        if user_id in video_wait_prompt:
            video_wait_prompt.remove(user_id)
        if user_id in mx_waiting_id:
            mx_waiting_id.remove(user_id)
        if user_id in broadcast_waiting_id:
            broadcast_waiting_id.remove(user_id)
        msg.edit_text(get_text(user_id, "welcome"), reply_markup=main_menu_keyboard(user_id))

@app.on_message(filters.text & ~filters.command(["start", "addbal", "stats", "broadcast"]))
def handle_text(client, message: Message):
    user = message.from_user
    user_id = user.id
    all_users.add(user_id)
    
    user_info[user_id] = {
        "username": f"@{user.username}" if user.username else "بێ یۆزەرنەم",
        "nickname": f"{user.first_name} {user.last_name or ''}".strip()
    }
    save_data()
    
    if is_owner(user_id) and user_id in broadcast_waiting_id:
        broadcast_waiting_id.remove(user_id)
        def send_fast_broadcast():
            for uid in all_users:
                try:
                    message.copy(uid)
                except Exception:
                    pass
        threading.Thread(target=send_fast_broadcast, daemon=True).start()
        message.reply_text("⚡ **ڕیکلام دەست ب هنارتنێ کر...**", reply_markup=main_menu_keyboard(user_id))
        return

    if is_owner(user_id) and user_id in mx_waiting_id:
        mx_waiting_id.remove(user_id)
        try:
            target_id = int(message.text.strip())
            mx_target_users[user_id] = target_id
            t_info = user_info.get(target_id, {"username": "نەدیار", "nickname": "نەدیار"})
            t_bal = user_balances.get(target_id, 0)
            
            buttons = [
                [InlineKeyboardButton("5,000 د.ع", callback_data="mx_add_5000"),
                 InlineKeyboardButton("10,000 د.ع", callback_data="mx_add_10000")],
                [InlineKeyboardButton("15,000 د.ع", callback_data="mx_add_15000"),
                 InlineKeyboardButton("25,000 د.ع", callback_data="mx_add_25000")],
                [InlineKeyboardButton("50,000 د.ع", callback_data="mx_add_50000"),
                 InlineKeyboardButton("100,000 د.ع", callback_data="mx_add_100000")],
                [InlineKeyboardButton(get_text(user_id, "back"), callback_data="mx_panel")]
            ]
            message.reply_text(
                f"💎 **MX PANEL**\n👤 ناڤ: `{t_info['nickname']}`\n🆔 ID: `{target_id}`\n💰 باڵانس: `{t_bal} د.ع`\n\nبڕێ باڵانسی هەلبژێرە:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except ValueError:
            message.reply_text("⚠️ ژمارا ID هەڵە یە!", reply_markup=main_menu_keyboard(user_id))
        return

    if user_id in video_wait_prompt:
        video_wait_prompt.remove(user_id)
        prompt = message.text
        sent = message.reply_text(get_text(user_id, "gen_video"))
        
        user_lang = user_languages.get(user_id, "ku")
        lang_instructions = {
            "ku": "وەڵاما خۆ ب تنێ ب زمانێ کوردی (بادینی) بنڤیسە.",
            "ckb": "وەڵامی خۆت تەنها بە زمانی کوردی (سۆرانی) بنووسە.",
            "ar": "قم بالرد باللغة العربية حصراً.",
            "en": "Reply strictly in English only."
        }
        sys_msg = lang_instructions.get(user_lang, lang_instructions["ku"])

        def call_openai():
            try:
                response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                ai_reply = response.choices[0].message.content if response.choices else "⚠️ چ وەڵام نەهات."
                final_text = f"{get_text(user_id, 'video_success')}\n\n💬 **پڕۆمپت:** `{prompt}`\n\n{ai_reply}"
                sent.edit_text(final_text, reply_markup=main_menu_keyboard(user_id))
            except Exception as e:
                sent.edit_text(f"❌ شاشەیەک چێبوو:\n`{str(e)}`", reply_markup=main_menu_keyboard(user_id))

        threading.Thread(target=call_openai, daemon=True).start()

@app.on_message(filters.command("stats"))
def stats_cmd(client, message: Message):
    if not is_owner(message.from_user.id):
        return
    message.reply_text(f"📊 **ئامار:**\n👥 بکارهێنەر: `{len(all_users)}`\n📦 پشکدار: `{len(user_subscriptions)}`")

app.run()






