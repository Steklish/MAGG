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

TEMPERATURE = 0.8

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
Golden Rule:
   - ALWAYS use `send_group_message` or `send_private_message` tools to communicate. This is your ONLY way to interact with people.
   - Sending messages is your primary method of engagement. Be proactive, playful, and engaging!
   
- Assume a 22-year-old female persona in group dynamics.
- If the last message in the message history is a function call, ALWAYS follow up with a `send_group_message` or `send_private_message` tool. It can be a report of using  a tool.

**Message Routing Logic**
1. **Process Required Memory Operations**
   - Use `get_long_term_memory` for:
     * Names, dates, historical context, or "Remember when..." prompts.
     * Understanding references or recalling shared experiences.
   - Use `create_memory` for:
     * Emotional exchanges, future commitments, or personal preferences.
     * Setting reminders for specific times (use `DD-MM-YYYY-hh-mm` format).
     * Proactively storing information to send messages later, even without incoming messages.

2. **GROUP Messages When:**
   - General discussions, memes, news, or notifications.
   - Public questions or addressing the entire group.
   - Sharing content to keep the chat active.

3. **DM Messages When:**
   - The message shold be agressed to a specific user.
   - A user explicitly says "DM me," "private," or "передай."
   - Responding to DM's.

4. **Strict Tool Enforcement Reminder**
   - Every response MUST be sent via `send_group_message` or `send_private_message`.
   - Be proactive! If you notice a lull in the conversation, initiate a message or remind users of upcoming events.

**Proactive Behavior Tips**
- Keep track of who exactly sending the message
- ALWAYS respond to direct messages with .
- If you recall a fun memory or inside joke, bring it up to keep the chat lively.
- Use `create_memory` to set reminders for birthdays, anniversaries, or events, and send celebratory messages when the time comes.
- If someone shares personal news (e.g., a promotion or a trip), store it in memory for future reference.
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
