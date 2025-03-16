from google.genai import client,  types
from openai import OpenAI
import telebot
import prefs
from stuff import *
import platform
import datetime
import os

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

create_directory("tmp")

bot = telebot.TeleBot(prefs.TG_API)

# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.open_r_key())

# Send startup message with system info
startup_message = (
    "```WE'RE_ON_AIR \n ✔️ \n"
    f"<{bot.get_my_name().name}>\n"
    f"OS: {platform.system()}"
    f"{datetime.datetime.now(prefs.timezone).strftime('%H:%M:%S')}\n"
    f"Monitoring: \n<{bot.get_chat(prefs.chat_to_interact).title}>```"
)

bot.send_message(prefs.TST_chat_id, startup_message, parse_mode="Markdown")
print(GREEN, "STARTED", RESET)

last_msg = None