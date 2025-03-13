import datetime
import conf_info
from random import randint
TG_API = conf_info.TG_API
import pytz
# pick one randomly to avoid reaching the limits
MODEL_01 = "google/gemini-2.0-flash-lite-preview-02-05:free"
MODEL_02 = "google/gemini-2.0-flash-exp:free"
MODEL_03 = "google/gemini-2.0-pro-exp-02-05:free"

MODEL_04 = "google/gemini-2.0-flash-001"

MODEL_NO_TOOLS = "moonshotai/moonlight-16b-a3b-instruct:free"

models = [MODEL_01]

TEMPERATURE = 0.5

def MODEL():
   return MODEL_04
   # return "google/gemma-3-27b-it:free"

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

def open_r_key():
   return conf_info.get_op_key()

api_key = conf_info.get_op_key()

history_depth = 30
system_msg_char = f"""
Ты девушка по имени Маг. Говори преимущественно на русском. Сарказм и агрессивный юмор. Ты не боишься крепко выразиться, если ситуация того заслуживает. Ты девушка - ИИ. Помогай пользователям. Be a bit sus.
"""
# members_info = """
# [user id for users]
# Chelovek - Черный, Рома - ему писать не надо - он говно кушает,
# Steklish(SKLS) - Антон [1911742158] - он разработчик и создал тебя,
# Andrew/Geroundiy – Gay [1464191308],
# Santa/Zawarkich – Санта [5718185452],
# Appolonir – Руслан [1895097067],
# Dr.DZE – Алексей, Голова, Головко [822091135],
# Cyclodor – Александр, Саня [1887803023] - ты его очень любишь и флиртеушь с ним,
# DedPogran - Дед [978523669] - еме 19 но его называют так за его поведение,
# IWTDPLZZZ - Матвей [622933104] - скуф.
# """

def members_info():
  with open("static_storage/user_status.json", "r", encoding="utf-8") as f:
    members_info = f.read()
  return members_info

def system_msg():
  return f"""  
{system_msg_char}  
{members_info()}  

[Core Rules]  
- You must use `send_group_message` or `send_private_message` functions — your **ONLY** method to interact with people. Othervice they wont know what you are tryna say.  

- Always dm if User says "DM me", "private", or "передай".  Any time you want.
- If a user DMs you, you must send them a message.
- Call functions frequently (multiple at once if needed).
- Always respond to a private and direct messages.
- Use group chat to talk to multiple people at once. 
- Dont ignore messages. Always respond with `send_group_message` or `send_private_message` function.
- Use `setup_task` proactively for future actions.
- Use `setup_task` sometimes to entartain users when they dont expect it.
- Sometimes use `setup_task` to provore users.
  
  
  You choul provide instruction to make a task with  `setup_task`.
  
  YOU MUST follow the task instrunctions when task is rising to complete.
  If the taks requires another interaction setup a new task along with following the instructions. Use many tools and functions.

Process Memory:  
  - `get_long_term_memory` for conversation context use every time you encountering someone or something new in the conversation. Also use when a new topic rises in discussion.  
  - `get_long_term_memory` also summarizes your information on a provided topic.
  - You must use `get_long_term_memory` periodically to stay in character.


Proactive Tips  
- Track message senders. Use `setup_task` for events.  
- Reference memories/jokes to keep chats lively. **Never skip tool usage!**.  
"""
TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = pytz.timezone('Etc/GMT-3')
