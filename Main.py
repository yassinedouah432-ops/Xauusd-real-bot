import os, time, requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=15)
        return float(r.json()['price'])
    except:
        return None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

def analyse(price):
    if price is None:
        return None
    if price % 10 < 3:
        sig = "🟢 *BUY - شراء* (السعر طالع)"
        tp = price + 6
        sl = price - 4
    elif price % 10 > 7:
        sig = "🔴 *SELL - بيع* (السعر نازل)"
        tp = price - 6
        sl = price + 4
    else:
        sig = "🟡 *انتظار - السوق عرضي*"
        tp = price + 5
        sl = price - 5
    
    return f"""✨ *XAUUSD REAL-TIME* ✨
    
💰 السعر الحي: *{price:.2f}$* (بحال Exness)

📊 التحليل:
{sig}

🎯 TP: `{tp:.2f}`
🛑 SL: `{sl:.2f}`

⏰ الوقت: {time.strftime('%H:%M:%S')} - Rissani
🤖 البوت خدام LIVE"""

print("Bot started...")
send_telegram("✅ *البوت REAL-TIME خدام دابا!* غادي نبدا نصيفط اشارات كل 30 دقيقة")

while True:
    price = get_gold_price()
    if price:
        msg = analyse(price)
        if msg:
            send_telegram(msg)
            print(f"Sent: {price}")
    time.sleep(1800)
