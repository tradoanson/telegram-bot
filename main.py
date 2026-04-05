import telebot
import re
from datetime import datetime

import os
TOKEN = os.getenv("8346322722:AAHg5cjzHkASBevfERXKr8dONKDjDSmQdJk")

bot = telebot.TeleBot(TOKEN)

data = []

def parse_money(text):
    match = re.search(r'(\d+)', text)
    if match:
        return int(match.group(1)) * 1000
    return 0

def detect_type(text):
    if "ăn" in text or "cafe" in text:
        return "Ăn uống"
    elif "xăng" in text:
        return "Di chuyển"
    return "Khác"

@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.lower()

    if "tổng hôm nay" in text:
        total = sum(x["money"] for x in data if x["date"] == datetime.today().date())
        bot.reply_to(message, f"Tổng hôm nay: {total:,}đ")
        return

    if "tháng này" in text:
        total = sum(x["money"] for x in data)
        bot.reply_to(message, f"Tháng này: {total:,}đ")
        return

    money = parse_money(text)
    if money > 0:
        item = {
            "date": datetime.today().date(),
            "money": money,
            "type": detect_type(text)
        }
        data.append(item)
        bot.reply_to(message, f"Đã ghi: {money:,}đ ({item['type']})")
    else:
        bot.reply_to(message, "Không hiểu 😄")

bot.polling()
