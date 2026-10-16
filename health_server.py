import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/health")
def health():
    return "Bot is running", 200

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def start_health_server():
    Thread(target=run_health_server, daemon=True).start()
