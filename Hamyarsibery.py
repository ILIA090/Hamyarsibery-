from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "EBEEH0AZYPISRTPOBIDBJMMKYPFOQIXMZVWHBCWEQTKXQBGFRISLZJWSEWELKQNG"
GEMINI_API_KEY = "AIzaSyAa984AXtLr22aelNZwCf2hDnkEDMLj1sM"  # از Google AI Studio بگیر
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

def send_message(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

@app.route("/receiveUpdate", methods=["POST"])
def receive_update():
    data = request.get_json()

    try:
        message = data["update"]["new_message"]
        text = message.get("text", "")
        chat_id = message.get("chat_id")

        # بررسی دستور hamyar
        if text.startswith("/hamyar"):
            user_query = text.replace("/hamyar", "").strip()

            # ارسال به Gemini AI
            payload = {
                "contents": [{"parts": [{"text": user_query}]}]
            }
            response = requests.post(GEMINI_URL, json=payload)
            ai_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

            # ارسال پاسخ به گروه
            send_message(chat_id, ai_text)

    except Exception as e:
        print("خطا:", e)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

@app.route("/")
def home():
    return "🤖 Rubika AI bot by ilia manzari is running!"
