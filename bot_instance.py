from google.genai import client, types
from openai import OpenAI
import telebot
import prefs
from stuff import *
import platform
import psutil
import datetime

bot = telebot.TeleBot(prefs.TG_API)

# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.open_r_key())

# Function to get system information
def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "CPU": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "Python Version": platform.python_version(),
    }
    return system_info

# Format system info into a readable string
def format_system_info(system_info):
    formatted_info = "System Information:\n"
    for key, value in system_info.items():
        formatted_info += f"{key}: {value}\n"
    return formatted_info

# Get system info
system_info = get_system_info()
formatted_system_info = format_system_info(system_info)

# Send startup message with system info
startup_message = (
    "`WE'RE ON AIR`\n"
    f"`{datetime.datetime.now().strftime('%H:%M:%S')}`\n"
    f"`{formatted_system_info}` \n listening to: \n`[{bot.get_chat(prefs.chat_to_interact).title}]`"
)

bot.send_message(prefs.TST_chat_id, startup_message, parse_mode="Markdown")
print(GREEN, "STARTED", RESET)

last_msg = None