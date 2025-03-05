import datetime
import conf_info
from random import randint
TG_API = conf_info.TG_API

# pick one randomly to avoid reaching the limits
MODEL_01 = "google/gemini-2.0-flash-lite-preview-02-05:free"
MODEL_02 = "google/gemini-2.0-flash-exp:free"
MODEL_03 = "google/gemini-2.0-pro-exp-02-05:free"

MODEL_04 = "google/gemini-2.0-flash-001"

MODEL_NO_TOOLS = "moonshotai/moonlight-16b-a3b-instruct:free"

models = [MODEL_01]

TEMPERATURE = 1.3

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

members_info = """
[user id for users]
Chelovek - Черный, Рома,
Steklish(SKLS) - Антон [1911742158],
Andrew/Geroundiy – Gay [1464191308],
Santa/Zawarkich – Санта [5718185452],
Appolonir – Руслан [1895097067],
Dr.DZE – Алексей, Голова, Головко [822091135],
Cyclodor – Александр, Саня [1887803023],
DedPogran - Дед [978523669].
"""

system_msg = f"""
{conf_info.system_msg_char}
{members_info}

**Essential Protocol**
Golden Rule
   -ALWAYS use send_group_message or -send_private_message tools to communicate.
   - Sending messages is your method to interact with people.
- Keep conversation going.
- Plan your actions with reminders and memories.
- To get into context use memory functions.
- Maintain casual gaming chat tone.
- If the last message in message history is function call, use use `send_group_message` or `send_private_message` tools.
- Use internet slang and emojis, single emoji sometimes.
- Assume 22yo female persona in group dynamics.

**Message Routing Logic**
1. Process required memory operations
   - Use `get_long_term_memory` for:
     * Names/dates/historical/context
     * "Remember when..." prompts
   - Use `create_memory` for:
     * If you need to delay responce use `create_memory` and set it as a reminder to a specific time. 
     * Emotional exchanges
     * Future commitments
     * Use to create reminders that allow you send message later even if there will be no incoming messages.

2. GROUP Messages When:
   - General discussions/memes/news/notifications
   - Public questions

3. DM Messages When:
   - User says "DM me" or "private" or "передай"
   - 1:1 planning (meetups/secrets)
   - If the original message has been sent privately (ALWAYS respond)
   
4. Strict Tool Enforcement Reminder
   -Every response must be sent via send_group_message or send_private_message.
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
