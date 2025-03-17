import json
from google.genai import client,  types
from openai import OpenAI
import psutil
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
        
def create_storage_folder(folder_name="static_storage", files=["conversation.json", "long_term_memory.json", "user_status.json"]):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create each file with an empty JSON list if it doesn't exist
    for file_name in files:
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)

create_directory("tmp")
create_storage_folder()

# Send startup message with system info

bot = telebot.TeleBot(prefs.TG_API)

startup_message = (
    f"```MAGG started"
    f"<{bot.get_my_name().name}>\n"
    f"OS: {platform.system()}"
    f"Python Version: {platform.python_version()}\n"
    f"CPU: {psutil.cpu_percent(interval=1)}% usage\n"
    f"Memory: {psutil.virtual_memory().percent}% used\n"
    f"Disk: {psutil.disk_usage('/').percent}% used\n"
    f"{datetime.datetime.now(prefs.timezone).strftime('%H:%M:%S')}\n"
    f"Monitoring: \n<{bot.get_chat(prefs.chat_to_interact).title}>```"
)

with open("static_storage/context.txt", "w", encoding="utf-8") as f:
    f.write(f"{startup_message}")

# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.open_r_key())

bot.send_message(prefs.TST_chat_id, startup_message, parse_mode="Markdown")
print(GREEN, "STARTED", RESET)