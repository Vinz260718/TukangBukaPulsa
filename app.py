from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import requests
from datetime import datetime
import pytz

# ================= CONFIG =================
BOT_TOKEN = "8297410519:AAFC5V7CKuGVc5GsEpAznTP1fw6TqwzYFzs"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxlq9xEcH9TmB9BZAstKFcpdEucE-XV-7giWO78IKLj6Glt_YqCGZ_iCq2_bszZ9Mo1BA/exec"

# ================= HELPER (WIB FIX) =================
def get_sheet_name():
    tz = pytz.timezone("Asia/Jakarta")
    today = datetime.now(tz).day
    return f"{today + 1} DES"

# Mapping TSEL -> Nama + Cell
TSEL_MAP = {
    "TSEL_1": {"name": "TSEL 1", "cell": "F3"},
    "TSEL_2": {"name": "TSEL 2", "cell": "F4"},
    "TSEL_3": {"name": "TSEL 3", "cell": "F5"},
    "TSEL_4": {"name": "TSEL 4", "cell": "F6"},
    "TSEL_5": {"name": "TSEL 5", "cell": "F7"},
    "TSEL_6": {"name": "TSEL 6", "cell": "F8"},
    "TSEL_7": {"name": "TSEL 7", "cell": "F9"},
    "TSEL_8": {"name": "TSEL 8", "cell": "F10"},
    "TSEL_9": {"name": "TSEL 9", "cell": "F11"},
    "TSEL_10": {"name": "TSEL 10", "cell": "F12"},
    "TSEL_11": {"name": "TSEL 11", "cell": "F13"},
    "TSEL_12": {"name": "TSEL 12", "cell": "F14"},
    "TSEL_13": {"name": "TSEL 13", "cell": "F15"},
    "TSEL_14": {"name": "TSEL 14", "cell": "F16"},
}

# ================= START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("TSEL 1", callback_data="TSEL_1"),
         InlineKeyboardButton("TSEL 2", callback_data="TSEL_2")],
        [InlineKeyboardButton("TSEL 3", callback_data="TSEL_3"),
         InlineKeyboardButton("TSEL 4", callback_data="TSEL_4")],
        [InlineKeyboardButton("TSEL 5", callback_data="TSEL_5"),
         InlineKeyboardButton("TSEL 6", callback_data="TSEL_6")],
        [InlineKeyboardButton("TSEL 7", callback_data="TSEL_7"),
         InlineKeyboardButton("TSEL 8", callback_data="TSEL_8")],
        [InlineKeyboardButton("TSEL 9", callback_data="TSEL_9"),
         InlineKeyboardButton("TSEL 10", callback_data="TSEL_10")],
        [InlineKeyboardButton("TSEL 11", callback_data="TSEL_11"),
         InlineKeyboardButton("TSEL 12", callback_data="TSEL_12")],
        [InlineKeyboardButton("TSEL 13", callback_data="TSEL_13"),
         InlineKeyboardButton("TSEL 14", callback_data="TSEL_14")],
    ]

    sheet_name = get_sheet_name()

    await update.message.reply_text(
        f"Pilih TSEL yang mau dibuka pulsanya 👇\n📍 Target Sheet: {sheet_name}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= BUTTON HANDLER =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tsel_data = TSEL_MAP.get(query.data)
    tsel_name = tsel_data["name"]
    cell = tsel_data["cell"]
    sheet_name = get_sheet_name()

    try:
        response = requests.post(
            WEB_APP_URL,
            json={
                "sheet": sheet_name,
                "cell": cell
            },
            timeout=10
        )
        result = response.json()

        if result.get("status") == "success":
            msg = (
                "✅ RESET BERHASIL\n\n"
                f"📍 Sheet : {sheet_name}\n"
                f"📡 Target: {tsel_name}\n"
                "🧾 Status: Udah Gue Bantu Buka Pulsa Mu Asep Gondrong 😎"
            )
        else:
            msg = (
                "❌ RESET GAGAL\n\n"
                f"📍 Sheet : {sheet_name}\n"
                f"📡 Target: {tsel_name}\n"
                "🧾 Status: Gondrong Ini Ada Masalah Cak Perbaiki Dulu 😈"
            )

    except Exception as e:
        msg = (
            "⚠️ SYSTEM ERROR\n\n"
            f"📍 Sheet : {sheet_name}\n"
            f"📡 Target: {tsel_name}\n"
            "🧾 Status: Gondrong Ini Ada Masalah Cak Perbaiki Dulu 😈"
        )

    await query.edit_message_text(msg)

# ================= MAIN =================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 Bot nyala, sheet otomatis ngikut tanggal WIB...")
    app.run_polling()

print("DEBUG SHEET =>", repr(get_sheet_name()))