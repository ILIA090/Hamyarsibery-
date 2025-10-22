# Hamyarsibery.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# =======================
# تنظیمات بات و Gemini
# =======================
ROUBIKA_TOKEN = "EBEEH0AZYPISRTPOBIDBJMMKYPFOQIXMZVWHBCWEQTKXQBGFRISLZJWSEWELKQNG"
GEMINI_KEY = "AIzaSyAa984AXtLr22aelNZwCf2hDnkEDMLj1sM"
ENDPOINT = "https://hamyarsibery.onrender.com/receiveUpdate"  # آدرس سرور Render شما

# =======================
# ست کردن Webhook روی روبیکا
# =======================
def set_webhook():
    url = f"https://botapi.rubika.ir/v3/{ROUBIKA_TOKEN}/updateBotEndpoint"
    data = {"update_url": ENDPOINT}  # 👈 باید update_url باشه
    try:
        r = requests.post(url, json=data)
        print("Webhook response:", r.text)
    except Exception as e:
        print("Webhook error:", e)

# اجرا یکبار برای ست کردن webhook
set_webhook()

# =======================
# تابع پاسخ به کاربران
# =======================
def ask_gemini(prompt):
    """
    ارسال متن به Gemini و دریافت پاسخ
    """
    headers = {
        "Authorization": f"Bearer {GEMINI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200
    }
    try:
        r = requests.post("https://api.gemini.ai/v1/complete", json=data, headers=headers)
        if r.status_code == 200:
            resp = r.json()
            return resp.get("text", "Gemini پاسخی نداد 😔")
        else:
            return f"Gemini خطا داد: {r.text}"
    except Exception as e:
        return f"خطا در ارتباط با Gemini: {e}"

# =======================
# دریافت آپدیت از روبیکا
# =======================
@app.route("/receiveUpdate", methods=["POST"])
def receive_update():
    try:
        data = request.json
        if "update" in data and data["update"]["type"] == "NewMessage":
            chat_id = data["update"]["chat_id"]
            message_text = data["update"]["new_message"]["text"]

            # فقط اگر پیام /hamyar شروع شد پاسخ بده
            if message_text.startswith("/hamyar"):
                # حذف /hamyar از متن و ارسال به Gemini
                prompt = message_text[len("/hamyar"):].strip()
                if prompt == "":
                    prompt = "سلام، میخوای چه کمکی انجام بدم؟"
                answer = ask_gemini(prompt)

                # ارسال جواب به روبیکا
                send_url = f"https://botapi.rubika.ir/v3/{ROUBIKA_TOKEN}/sendMessage"
                send_data = {
                    "chat_id": chat_id,
                    "text": answer
                }
                requests.post(send_url, json=send_data)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =======================
# مسیر تست ساده
# =======================
@app.route("/", methods=["GET"])
def index():
    return "🤖 Rubika AI bot by ilia manzari is running!"

# =======================
# اجرای Flask
# =======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
