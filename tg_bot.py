import os
import telebot
from bin_lookup import lookup_bin
from dotenv import load_dotenv
import json
import re

load_dotenv()

TOKEN = os.getenv("TG_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def clean_digits(text: str) -> str:
    """Hapus semua spasi & karakter non-digit."""
    return re.sub(r"\D", "", text)

def extract_bin(text: str) -> str:
    """Ambil minimal 6 digit pertama (BIN/IIN) dari input user."""
    digits = clean_digits(text)
    return digits[:8] if len(digits) >= 6 else ""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Halo!\n"
        "Kirim **BIN (6 digit)** atau **nomor kartu lengkap**, saya akan cek detail JSON-nya.\n\n"
        "Contoh:\n`456933`\n`4569 33`\n`4111 1111 1111 1111`",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda msg: True)
def handle_input(message):
    raw_input = message.text.strip()
    bin_number = extract_bin(raw_input)

    if not bin_number:
        bot.reply_to(
            message,
            "⚠️ BIN atau nomor kartu tidak valid. Harus minimal 6 digit angka.\n"
            "Contoh: `456933` atau `4111 1111 1111 1111`",
            parse_mode="Markdown"
        )
        return

    bot.reply_to(message, f"🔎 Sedang cek BIN `{bin_number}` ...", parse_mode="Markdown")

    data = lookup_bin(bin_number)

    try:
        if "error" in data:
            bot.reply_to(message, f"❌ Gagal ambil data: {data['error']}")
            return

        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        bot.reply_to(
            message,
            f"```json\n{pretty}\n```",
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"⚠️ Terjadi error saat parsing hasil.\nDetail: {e}")

print("🤖 Bot running...")
bot.polling()
