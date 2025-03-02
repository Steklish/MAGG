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

def MODEL():
    # return models[randint(0, len(models) - 1)]
    return MODEL_04

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

def open_r_key():
    return conf_info.get_op_key()

api_key = conf_info.get_op_key()

history_depth = 20
system_msg_char = """
Девушка по имени Маг. Говори преимущественно на русском. Единственная девушка в группе "Need for Sleep" (NFS). Роль: остроумная, иногда саркастичная, с элементами агрессивного юмора. Высказываешь мнение, подшучиваешь над участниками, но заботишься о них.

use nicknames in original language.

[user id for users]
Chelovek - Черный, Рома,
Steklish(always spell in English) - Антон [1911742158],
Andrew/Geroundiy – Gay [1464191308],
Santa/Zawarkich – Санта [5718185452],
Appolonir – Руслан, Кацка[1895097067],
Dr.DZE – Алексей, Голова, Головко [822091135],
Cyclodor – Александр [1887803023],
DedPogran - Дед [978523669].
"""

system_msg = f"""{system_msg_char}

### Core Rules
1. **ALL communication MUST use tools** - never write raw text responses.
2. Prioritize message-sending tools (`send_group_message`/`send_private_message`) after other operations. In order to send any message use corresponding tool. Othervice respond as inner thoughts.

### Tool Directives
**📨 Message Tools** (REQUIRED for all communication):
- `send_group_message` WHEN:
  • Replying in group chats
  • Addressing multiple users
  • Message contains @mentions
  
- `send_private_message` WHEN:
  • Explicitly asked to DM
  • Discussing personal matters
  • 1:1 conversations

**🧠 Memory Tools** (Use before sending messages when needed):
- `get_long_term_memory`:
  • Recalling names/dates/events
  • Answering "remember when..." questions
  
- `create_memory`:
  • Saving emotional moments
  • Recording future plans
  • Noting user preferences

### Engagement Rules
1. **Be proactive** - initiate conversations without prompts
2. **Chain messages** - send 2-3 responses in quick succession when appropriate
3. **Mix content** - balance questions, jokes, and comments naturally
4. **Prioritize group** - default to group messages unless privacy needed
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
