import os
import logging
import datetime
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

API_ID = 34584240
API_HASH = "eba4f8333cba5f9697a1d20779d4d6e9"
BOT_TOKEN = "8884140391:AAFNa_XLY0mukd8O5JH070MeDmxRmW9yM9c"
OWNER_ID = 7643191802

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

users_db = {}
admin_state = {}
active_user_bots = {} # بۆ ڕاگرتنا پرۆسەیێن بۆتێن بەکارهێنەران

def get_user(user_id, user=None):
    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 0.0, 
            "expire_date": None, 
            "lifetime": False,
            "first_name": user.first_name if user else "نەدیار",
            "username": user.username if user else None,
            "bot_token": None
        }
    elif user:
        if user.first_name:
            users_db[user_id]["first_name"] = user.first_name
        if user.username:
            users_db[user_id]["username"] = user.username
    return users_db[user_id]

def is_active(user_id):
    user_data = get_user(user_id)
    if user_data["lifetime"]:
        return True
    if user_data["expire_date"] and datetime.datetime.now() < user_data["expire_date"]:
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user(user.id, user)
    bal = user_data["balance"]
    
    if user_data["lifetime"]:
        status = "✅ چالاکە (هەتامایێ - Lifetime)"
    elif is_active(user.id):
        status = f"✅ چالاکە هەتا: {user_data['expire_date'].strftime('%Y-%m-%d')}"
    else:
        status = "❌ نەچالاکە (بێ بەرامبەر کار ناکەت)"
    
    profile_text = (
        f"👤 **پروفایلا تە (User Profile)**\n\n"
        f"• **ناڤ:** {user.first_name}\n"
        f"• **یوزرنەیم:** @{user.username or 'نەهاتییە دانان'}\n"
        f"• **ایدی:** `{user.id}`\n"
        f"• **💰 بیلانس:** `{bal}` دینار\n"
        f"• **⏳ بەشداری:** {status}\n\n"
        f"🤖 بۆتێ پارەیی یێ تایبەت ب کارپێکرنا بۆتان!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 کڕینا بەشدارییێ (Plans)", callback_data="buy_plans")],
        [InlineKeyboardButton("💳 کڕینا بیلانس (Buy Balance)", url="https://t.me/YUSEEF_SURCHI")],
        [InlineKeyboardButton("🚀 کارپێکرنا بۆتا خۆ (Run Bot)", callback_data="run_bot_menu")],
    ]
    
    if user.id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("⚙️ کۆنترۆل پەنێل (CC Panel)", callback_data="cc_panel")])
        
    keyboard.append([InlineKeyboardButton("🔄 نووکرن (Refresh)", callback_data="refresh")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(profile_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(profile_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_data = get_user(user.id, user)
    await query.answer()
    
    if query.data == "buy_plans":
        keyboard = [
            [InlineKeyboardButton("٦ هەیڤ - 5,000 دینار", callback_data="buy_6m")],
            [InlineKeyboardButton("١ سال - 10,000 دینار", callback_data="buy_1y")],
            [InlineKeyboardButton("هەتامایێ - 25,000 دینار", callback_data="buy_lifetime")],
            [InlineKeyboardButton("⬅️ ڤەگەر", callback_data="back_to_profile")]
        ]
        await query.edit_message_text(
            "🛒 **هەلبژارتنا پلانێ (Paid Bot Plans)**\n\nتکایە ماوەیێ خوە هەلبژێرە:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif query.data in ["buy_6m", "buy_1y", "buy_lifetime"]:
        if user_data["lifetime"]:
            await query.answer("✅ تو ژ بەرێڤە خودانێ پلانا هەتامایێ یی!", show_alert=True)
            return

        if query.data == "buy_6m":
            cost = 5000
            days = 180
        elif query.data == "buy_1y":
            cost = 10000
            days = 365
        elif query.data == "buy_lifetime":
            cost = 25000
            days = 0
        
        if user_data["balance"] >= cost:
            user_data["balance"] -= cost
            
            if query.data == "buy_lifetime":
                user_data["lifetime"] = True
                user_data["expire_date"] = None
            else:
                if user_data["expire_date"] and datetime.datetime.now() < user_data["expire_date"]:
                    user_data["expire_date"] += datetime.timedelta(days=days)
                else:
                    user_data["expire_date"] = datetime.datetime.now() + datetime.timedelta(days=days)
                
            await query.answer("✅ بەشدارییا تە ب سەرکەفتیانە هاتە کڕین!", show_alert=True)
            await start(update, context)
        else:
            await query.answer("❌ بیلانسێ تە تێرا ناکەت! تکایە ل دەف خودانی بیلانس بکڕە.", show_alert=True)

    elif query.data == "run_bot_menu":
        if not is_active(user.id):
            keyboard = [[InlineKeyboardButton("⬅️ ڤەگەر", callback_data="back_to_profile")]]
            await query.edit_message_text(
                "❌ **تۆ نەشێی بۆتی کار پێ بکەی!**\n\nپێدڤییە بەشدارییێ بکڕی (Paid Bot) دا کو بشێی بۆتا خۆ Run بکەی.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return
            
        context.user_data["waiting_for_bot_token"] = True
        keyboard = [
            [InlineKeyboardButton("⏹️ ڕاگرتنا بۆتا من", callback_data="stop_my_bot")],
            [InlineKeyboardButton("⬅️ ڤەگەر بۆ پروفایلی", callback_data="back_to_profile")]
        ]
        await query.edit_message_text(
            "🚀 **کارپێکرنا بۆتا تە (Run Your Bot)**\n\n"
            "• فەرموو **Bot Token** ێ خۆ ل ڤێرە بنڤیسە و بۆ من بنێرە دا بۆتا تە ڕاستەوخۆ بهێتە کارپێکرن!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif query.data == "stop_my_bot":
        if user.id in active_user_bots:
            active_user_bots[user.id].terminate()
            del active_user_bots[user.id]
            user_data["bot_token"] = None
            await query.answer("✅ بۆتا تە هاتە ڕاگرتن!", show_alert=True)
        else:
            await query.answer("⚠️ چ بۆتەک ژ لایێ تە ڤە کار ناکەت.", show_alert=True)
        await start(update, context)
        
    elif query.data == "cc_panel":
        if user.id != OWNER_ID:
            await query.answer("تو نینه ڕێپێدراو!", show_alert=True)
            return
            
        admin_state[user.id] = "waiting_for_balance_input"
        keyboard = [
            [InlineKeyboardButton("📊 لستا 15 کەسێن یەکەم (Top 15)", callback_data="top_15_users")],
            [InlineKeyboardButton("❌ پاشگەزبوونەوە", callback_data="cancel_admin")],
            [InlineKeyboardButton("⬅️ ڤەگەر", callback_data="back_to_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "⚙️ **CC Panel - کۆنترۆلا بیلانسێ**\n\n"
            "`USER_ID +5000` (بۆ زێدەکرنێ)\n"
            "`USER_ID -2000` (بۆ کێمکرنێ)\n\n"
            "فەرموو فەرمانێ بنڤیسە یان لستا 15 کەسان هەلبژێرە:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "top_15_users":
        if user.id != OWNER_ID:
            return
            
        sorted_users = sorted(users_db.items(), key=lambda x: x[1]["balance"], reverse=True)[:15]
        list_text = "📊 **لستا 15 کەسێن خودان بیلانس یێن پێشەنگ (Top 15):**\n\n"
        if not sorted_users:
            list_text += "هیچ بەکارهێنەرەک هێشتا تۆمار نەکرییە."
        else:
            for idx, (uid, udata) in enumerate(sorted_users, 1):
                uname = f"@{udata['username']}" if udata['username'] else "نەهاتییە دانان"
                list_text += f"{idx}. **{udata['first_name']}** | {uname} | ایدی: `{uid}` | بیلانس: `{udata['balance']}`\n"
                
        keyboard = [[InlineKeyboardButton("⬅️ ڤەگەر بۆ CC Panel", callback_data="cc_panel")]]
        await query.edit_message_text(list_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
    elif query.data == "cancel_admin" or query.data == "refresh" or query.data == "back_to_profile":
        if user.id in admin_state: del admin_state[user.id]
        if "waiting_for_bot_token" in context.user_data: del context.user_data["waiting_for_bot_token"]
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    
    # ئەگەر بەکارهێنەر تەکەنێ بۆتا خۆ نڤیسی بیت
    if context.user_data.get("waiting_for_bot_token"):
        if not is_active(user.id):
            await update.message.reply_text("❌ بەشدارییا تە ب دوماهی هاتییە!")
            return
            
        bot_token = text.strip()
        user_data = get_user(user.id, user)
        user_data["bot_token"] = bot_token
        
        # ئەگەر بۆتەک پێشتر کار بکەت، ڕادوەستینین
        if user.id in active_user_bots:
            active_user_bots[user.id].terminate()
            
        # کارپێکرنا فایلا دووەم (user_bot.py) ب ڕێکا subprocess
        process = subprocess.Popen(["python", "user_bot.py", bot_token])
        active_user_bots[user.id] = process
        
        del context.user_data["waiting_for_bot_token"]
        await update.message.reply_text("✅ **بۆتا تە ب سەرکەفتیانە هاتە کارپێکرن (Run) ل سەر سێرڤەری!**", parse_mode="Markdown")
        await start(update, context)
        return

    # پشکنینا CC Panel بۆ خودانی
    if user.id == OWNER_ID and admin_state.get(user.id) == "waiting_for_balance_input":
        try:
            parts = text.strip().split()
            if len(parts) >= 2:
                target_user_id = int(parts[0])
                action_value = parts[1]
                target_data = get_user(target_user_id)
                
                amount = float(action_value.replace("+", "").replace("-", ""))
                if amount > 10000000:
                    await update.message.reply_text("❌ ژ 10,000,000 زێدەتر ناهێتە قەبوولکرن.")
                    return

                if "-" in action_value:
                    target_data["balance"] -= amount
                    msg = f"✅ `{amount}` هاتە کێمکرن!"
                else:
                    target_data["balance"] += amount
                    msg = f"✅ `{amount}` هاتە زێدەکرن!"
                
                del admin_state[user.id]
                await update.message.reply_text(f"{msg}\n• **ایدی:** `{target_user_id}`\n• **بیلانسێ نوو:** `{target_data['balance']}`", parse_mode="Markdown")
                await start(update, context)
            else:
                await update.message.reply_text("❌ شێواز هەڵەیە! نموونە: `7643191802 +5000`")
        except ValueError:
            await update.message.reply_text("❌ ایدی یان بیلانس نە دروستە.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("بۆتا سەرەکی کار دکەت...")
    application.run_polling()

if __name__ == "__main__":
    main()
