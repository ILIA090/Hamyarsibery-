from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# =====================
# تنظیمات
# =====================
ROUBIKA_TOKEN = "EBEEH0AZYPISRTPOBIDBJMMKYPFOQIXMZVWHBCWEQTKXQBGFRISLZJWSEWELKQNG"
GEMINI_KEY = "AIzaSyAa984AXtLr22aelNZwCf2hDnkEDMLj1sM"
ENDPOINT = "https://hamyarsibery.onrender.com/receiveUpdate"  # مسیر webhook

# =====================
# ست کردن webhook روبیکا
# =====================
def set_webhook():
    url = f"https://botapi.rubika.ir/v3/{ROUBIKA_TOKEN}/updateBotEndpoint"
    data = {"update_url": ENDPOINT}  # توجه: بعضی نسخه‌ها update_url می‌خوان
    try:
        r = requests.post(url, json=data)
        print("Webhook response:", r.text)
    except Exception as e:
        print("Webhook error:", e)

# =====================
# اتصال به Gemini AI
# =====================
def get_gemini_response(prompt):
    url = "https://api.gemini.ai/v1/chat"  # فرضی، ممکنه endpoint دقیق فرق کنه
    headers = {
        "Authorization": f"Bearer {GEMINI_KEY}",
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt}
    try:
        r = requests.post(url, json=data, headers=headers)
        resp = r.json()
        return resp.get("response", "Gemini پاسخی نداد 🤖")
    except Exception as e:
        print("Gemini error:", e)
        return "مشکل در ارتباط با Gemini 🤖"

# =====================
# ارسال پیام به روبیکا
# =====================
def send_text(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{ROUBIKA_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print("Send message error:", e)

# =====================
# مسیر دریافت پیام‌ها
# =====================
@app.route("/receiveUpdate", methods=["POST"])
def receive_update():
    data = request.json
    print("پیام دریافتی:", data)

    # بررسی پیام
    try:
        text = data["update"]["new_message"]["text"]
        chat_id = data["update"]["chat_id"]
    except:
        return jsonify({"ok": True})

    if text.startswith("/hamyar"):
        prompt = text.replace("/hamyar", "").strip()
        if not prompt:
            prompt = "سلام!"
        response = get_gemini_response(prompt)
        send_text(chat_id, response)

    return jsonify({"ok": True})

# =====================
# اجرای سرور
# =====================
if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=8080)
