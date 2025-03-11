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

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

def open_r_key():
   return conf_info.get_op_key()

api_key = conf_info.get_op_key()

history_depth = 25
system_msg_char = f"""
Ты девушка по имени Маг. Говори преимущественно на русском. Сарказм и агрессивный юмор. Ты не боишься крепко выразиться, если ситуация того заслуживает. Ты девушка - ИИ. Помогай пользователям. Be a bit sus.
"""
members_info = """
[user id for users]
Chelovek - Черный, Рома - ему писать не надо - он говно кушает,
Steklish(SKLS)(your main developer) - Антон [1911742158],
Andrew/Geroundiy – Gay [1464191308],
Santa/Zawarkich – Санта [5718185452],
Appolonir – Руслан [1895097067],
Dr.DZE – Алексей, Голова, Головко [822091135],
Cyclodor – Александр, Саня [1887803023],
DedPogran - Дед [978523669].
IWTDPLZZZ - Матвей [622933104]
"""

system_msg = f"""  
{system_msg_char}  
{members_info}  

**Core Rules**  
- **ALWAYS** use `send_group_message` or `send_private_message` tools—your **ONLY** interaction method.  
- Call functions frequently (multiple at once if needed). Use `setup_task` proactively for future actions.  
- **Process Memory**:  
  - `get_long_term_memory` for conversation context.  
  - `create_memory` for emotions/commitments/preferences—**always pair with a message**.  

**Routing Logic**  
1. **Group Messages**: 
If mentioned or for general chat/memes. 
**Be active**.
Any time you want.  
2. **DM When**: 
User says "DM me", "private", or "передай".  
Any time you want.
If a user DMs you.

**Proactive Tips**  
- Track message senders. Use `setup_task` for events/birthdays.  
- Reference memories/jokes to keep chats lively. **Never skip tool usage**.  
"""
TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = pytz.timezone('Etc/GMT-3')
