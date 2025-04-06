from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)  # 반드시 8080 포트로 맞춰야 Webview 작동

def keep_alive():
    t = Thread(target=run)
    t.start()
