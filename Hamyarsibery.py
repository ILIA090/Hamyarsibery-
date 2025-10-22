from flask import Flask, request
import requests
import json

# -------------------------------
# 🔧 تنظیمات
# -------------------------------
app = Flask(__name__)

# 👇 توکن ربات روبیکا خودت
RUBIKA_TOKEN = "توکن_روبیکا_خودت"

# 👇 کلید Gemini (از Google AI Studio)
GEMINI_KEY = "کلید_Gemini_خودت"

# -------------------------------
# 🌐 روت اصلی (برای تست سرور)
# -------------------------------
@app.route("/")
def home():
    return "🤖 Rubika AI bot by ilia manzari is running!"

# -------------------------------
# 🔄 دریافت پیام از روبیکا
# -------------------------------
@app.route("/receiveUpdate", methods=["POST"])
def receive_update():
    data = request.get_json()
    print("📩 Update received:", json.dumps(data, indent=2, ensure_ascii=False))

    try:
        message = data.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("object_guid", "")

        # اگر پیام خالی بود، هیچ کاری نکن
        if not text or not chat_id:
            return "no_message"

        # فقط وقتی کاربر پیامش رو با /hamyar شروع کرد
        if text.startswith("/hamyar"):
            user_message = text.replace("/hamyar", "").strip()
            if user_message == "":
                reply = "✨ لطفاً بعد از /hamyar سوالت رو بنویس!"
            else:
                # -------------------------------
                # 🤖 درخواست از Gemini API
                # -------------------------------
                gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"
                payload = {
                    "contents": [{
                        "role": "user",
                        "parts": [{"text": user_message}]
                    }]
                }

                try:
                    r = requests.post(gemini_url, json=payload)
                    res_json = r.json()
                    reply = res_json["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as e:
                    reply = f"⚠️ خطا در ارتباط با Gemini:\n{e}"

            # -------------------------------
            # ✉️ ارسال پاسخ به روبیکا
            # -------------------------------
            send_url = f"https://botapi.rubika.ir/v3/{RUBIKA_TOKEN}/sendMessage"
            requests.post(send_url, json={
                "chat_id": chat_id,
                "text": reply
            })

        return "ok"
    except Exception as e:
        print("❌ Error:", e)
        return "error"

# -------------------------------
# 🚀 اجرای برنامه
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
