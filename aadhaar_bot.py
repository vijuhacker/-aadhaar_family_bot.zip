#!/usr/bin/env python3
import os
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE = os.getenv("API_BASE", "https://addartofamily.vercel.app/fetch")
API_KEY = os.getenv("API_KEY", "fxt")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to *Aadhaar Family Finder Bot*\n"
        "Send me any valid 12-digit Aadhaar number.\n"
        "I’ll fetch the public family details linked with that Aadhaar.\n\n"
        "_Note: Only for Indian users._ 🇮🇳",
        parse_mode=ParseMode.MARKDOWN,
    )

def format_family_response(data: dict) -> str:
    msg = f"🏠 *Family Details (Aadhaar-linked)*\n"
    msg += f"District: {data.get('homeDistName', 'N/A')}\n"
    msg += f"State: {data.get('homeStateName', 'N/A')}\n"
    msg += f"FPS ID: {data.get('fpsId', 'N/A')}\n"
    msg += f"Scheme: {data.get('schemeName', 'N/A')}\n\n"

    members = data.get("memberDetailsList", [])
    if not members:
        msg += "_No member details found._"
        return msg

    msg += "👨‍👩‍👧 *Family Members:*\n"
    for m in members:
        name = m.get('memberName', 'Unknown').strip()
        rel = m.get('releationship_name', m.get('relationship', 'N/A'))
        uid = m.get('uid', 'No')
        member_id = m.get('memberId', '-')
        msg += (
            f"• *{name}*\n"
            f"   Relationship: {rel}\n"
            f"   Member ID: `{member_id}`\n"
            f"   UID Linked: {uid}\n\n"
        )
    return msg

def handle_aadhaar(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return
    aadhaar = update.message.text.strip()

    # Aadhaar validation (basic)
    if not aadhaar.isdigit() or len(aadhaar) != 12:
        update.message.reply_text("❌ Please send a valid 12-digit Aadhaar number.")
        return

    url = f"{API_BASE}?aadhaar={aadhaar}&key={API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        update.message.reply_text(f"⚠️ API Error: {e}")
        return

    # Check if response contains members
    if not data or not data.get("memberDetailsList"):
        update.message.reply_text("❌ No details found for this Aadhaar. Try another one.")
        return

    msg = format_family_response(data)
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_TOKEN is not set in environment.")
        return
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_aadhaar))

    print("🤖 Aadhaar Family Bot is running... (Press Ctrl+C to stop)")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
