import telebot
import pytesseract
from PIL import Image
import io
import re
import os
from flask import Flask

# Para hindi mag-shutdown ang Render (Keep-alive)
app = Flask(__name__)
@app.route('/')
def index(): return "Bot is Running"

TOKEN = "8363241560:AAGM3sxjyuYihR-HSfwtSePCYZixAO9R-OM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image = Image.open(io.BytesIO(downloaded_file))
        text = pytesseract.image_to_string(image)
        numbers = re.findall(r'\d+', text)
        balance_candidates = [n for n in numbers if len(n) >= 5]
        
        if balance_candidates:
            bot.reply_to(message, f"💎 **Diamond Current Balance:**\n`{balance_candidates[0]}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "Hindi mahanap ang balance. Siguraduhing malinaw ang photo.")
    except:
        bot.reply_to(message, "Error processing image.")

if __name__ == "__main__":
    # Patakbuhin ang bot sa background
    import threading
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    # Patakbuhin ang web server para sa Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
