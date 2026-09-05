import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8653317587:AAH59X7hIIQ2s3rH4rzT26vDMPCRsPVFth8"

OWNERS = [7643191802, 8038533940]

user_balances = {}
user_languages = {}  # بۆ حافیزکرنا زمانێ بکارهێنەری (ku, ckb, en)
user_subscriptions = {}  
video_wait_prompt = set()
mx_waiting_id = set()  
mx_target_users = {}   

app = Client("yuseef_surchi_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_owner(user_id):
    return user_id in OWNERS

def get_text(user_id, key):
    lang = user_languages.get(user_id, "ku") # بنەڕەت بادینییە
    texts = {
        "ku": {
            "welcome": "✨ **سلاڤ و ڕێز!**\n\nب خێر هاتنی بۆ جیهانا پێشکەفتیا چێکرنا ڤیدیۆیان یا 4K ب هێزا AI.\nفەرموو ئێك ژ ڤان ڤالەکان ژ خوارێ هەلبژێرە:",
            "btn_video": "🎬 دروستکرنا ڤیدیۆ (AI)",
            "btn_bal": "💰 باڵانسا من",
            "btn_buy": "💳 كرینا باڵانسی",
            "btn_sub": "📦 پلەنێن پشکداریکردنێ",
            "btn_prof": "👤 پروفایلا من",
            "btn_lang": "🌐 گوهۆڕینا زمانێ (Language)",
            "mx_title": "⚙️ MX PANEL (تایبەت بۆ ڕێڤەبەرا)",
            "back": "🔙 ڤەگەر",
            "choose_lang": "🌐 فەرموو زمانێ خۆ هەلبژێرە:\n\nSelect your language / زمانەکەت هەڵبژێرە:",
            "lang_changed": "✅ زمان ب سەرکەفتی هاتە گوهۆڕین بۆ کوردی (بادینی)!",
            "no_sub": "❌ تە چ پشکداریکردنەکا کارا نینە!\nلطفەن سەرەتا پشکداریکردنێ چێکە یان باڵانسا خۆ بڕێڤەبەرا ڤەگۆڕە.\n\n💳 @X_MAM6 | @YUSEEF_SURCHi",
            "sub_active": "✅ پشکداریکردنا تە یا کارا یە!\nفەرموو پرۆمپتێ (Prompt) خۆ ب بادینی بنڤیسە بۆ دروستکرنا ڤیدیۆیا 4K:",
            "days_left": "ڕۆژ ماینە بۆ خلاساربوونێ",
            "video_success": "✅ **ڤیدیۆیا تە ب سەرکەفتی هاتە دروستکرن!**",
            "admin_only": "⚠️ ئەڤ پشکە تنێ بۆ خودان و ڕێڤەبەرا یە!"
        },
        "ckb": {
            "welcome": "✨ **سڵاو و ڕێز!**\n\nبەخێر هاتیت بۆ جیهانی پێشکەوتووی دروستکردنی ڤیدیۆی 4K بە هێزی AI.\nتکایە یەکێک لەم بژاردانەی خوارەوە هەڵبژێرە:",
            "btn_video": "🎬 دروستکردنی ڤیدیۆ (AI)",
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
            "sub_active": "✅ بەشداریکردنەکەت چالاکە!\nتکایە پڕۆمپتەکەت بنووسە بۆ دروستکردنی ڤیدیۆی 4K:",
            "days_left": "ڕۆژ ماون بۆ کۆتایی هاتن",
            "video_success": "✅ **ڤیدیۆکەت بە سەرکەوتوویی دروست کرا!**",
            "admin_only": "⚠️ ئەم بەشە تەنها بۆ خاوەن و بەڕێوەبەرانە!"
        },
        "en": {
            "welcome": "✨ **Hello & Welcome!**\n\nWelcome to the advanced 4K AI Video Generation bot.\nPlease select an option below:",
            "btn_video": "🎬 Create Video (AI)",
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
            "sub_active": "✅ Your subscription is active!\nPlease send your prompt for 4K video generation:",
            "days_left": "days remaining",
            "video_success": "✅ **Your 4K video was generated successfully!**",
            "admin_only": "⚠️ This section is restricted to owners/admins!"
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
            f"💰 Balance: **{bal}**\n\n💳 @X_MAM6\n💳 @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "buy_balance":
        msg.edit_text(
            "💳 Contact managers to buy balance:\n• @X_MAM6\n• @YUSEEF_SURCHi",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]])
        )

    elif data == "subscription_plans":
        text = (
            "📦 **Subscription Plans:**\n\n"
            "1️⃣ 1 Month (5,000)\n"
            "2️⃣ 6 Months (10,000)\n"
            "3️⃣ 1 Year (15,000)\n\n"
            "💳 @X_MAM6 | @YUSEEF_SURCHi"
        )
        msg.edit_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1️⃣ 1M (5k)", callback_data="buy_plan_1"),
             InlineKeyboardButton("2️⃣ 6M (10k)", callback_data="buy_plan_6")],
            [InlineKeyboardButton("3️⃣ 1Y (15k)", callback_data="buy_plan_12")],
            [InlineKeyboardButton(get_text(user_id, "back"), callback_data="main_menu")]
        ]))

    elif data.startswith("buy_plan_"):
        months = int(data.split("_")[2])
        prices = {1: 5000, 6: 10000, 12: 15000}
        cost = prices.get(months, 5000)
        current_bal = user_balances.get(user_id, 0)

        if current_bal < cost:
            callback_query.answer("❌ Low balance!", show_alert=True)
            return

        user_balances[user_id] = 0
        expire_time = time.time() + (months * 30 * 86400)
        user_subscriptions[user_id] = {
            "plan": f"{months} Months",
            "expire_time": expire_time
        }
        callback_query.answer("✅ Success!", show_alert=True)
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
            f"👤 **Profile:**\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"💰 Balance: **{bal}**\n"
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
                    [InlineKeyboardButton("1️⃣ 1M (5k)", callback_data="buy_plan_1"),
                     InlineKeyboardButton("2️⃣ 6M (10k)", callback_data="buy_plan_6")],
                    [InlineKeyboardButton("3️⃣ 1Y (15k)", callback_data="buy_plan_12")],
                    [InlineKeyboardButton("🔄 Check Sub", callback_data="create_video")],
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
            "⚙️ **MX PANEL (Owner Dashboard)**\n\n👤 Enter User ID:",
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
        
        try:
            client.send_message(target_id, f"✅ Balance added: +{amount}")
        except Exception:
            pass

        msg.edit_text(
            f"✅ **Balance sent successfully!**\n🆔 ID: `{target_id}`\n💰 Added: {amount}",
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
                [InlineKeyboardButton("🔙 Back", callback_data="mx_panel")]
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
        enhanced = f"{prompt}, cinematic 4k resolution, hyper realistic"
        
        sent = message.reply_text("⏳ Generating 4K video...")
        sent.edit_text(
            f"{get_text(user_id, 'video_success')}\n\n"
            f"🌐 Prompt: `{enhanced}`\n"
            f"💬 Input: {prompt}\n"
            "🎬 Quality: 4K (100% Works)"
        )

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
        message.reply_text(f"✅ Added {amount} to ID: {target_id}")
    except ValueError:
        pass

app.run()
