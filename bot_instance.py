from google.genai import client, types
from openai import OpenAI
import telebot
import prefs
from stuff import *
bot = telebot.TeleBot(prefs.TG_API)

# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.api_key)


bot.send_message(prefs.TST_chat_id, "👩🏻‍🦼👩🏻‍🦼👩🏻‍🦼💨 host started\n`" + prefs.datetime.datetime.now().strftime("%H:%M:%S") + "`",
                 parse_mode="Markdown")
print(GREEN, "STARTED", RESET)
    
    
last_msg = None