import requests
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_currency_rates():
    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}")
    data = response.json()
    usd_to_kzt = data["rates"]["KZT"]
    
    currencies = ["USD", "RUB", "EUR", "KGS", "CNY", "GBP", "JPY", "AUD", "CAD", "CHF", "UZS", "UAH", "BYN", "TRY", "KRW", "SGD", "INR", "AED"]
    result = []
    
    for currency in currencies:
        if currency == "KZT":
            continue
        rate = usd_to_kzt / data["rates"][currency]
        result.append({"name": currency, "rate": round(rate, 2)})
    
    return result

async def start(update: Update, context: CallbackContext):
    keyboard = [["Курс валют"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы получить курс валют к тенге.",
        reply_markup=reply_markup
    )

async def send_rates(update: Update, context: CallbackContext):
    rates = get_currency_rates()
    message = "📊 **Курс валют к KZT (тенге):**\n\n"
    
    for currency in rates:
        message += f"➡️ 1 {currency['name']} = {currency['rate']} KZT\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text(["Курс валют"]), send_rates))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()