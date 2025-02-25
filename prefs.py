import datetime
import conf_info
from random import randint
TG_API = conf_info.TG_API

# pick one randomly to avoid reaching the limits
MODEL_01 = "google/gemini-2.0-flash-lite-preview-02-05:free"
MODEL_02 = "google/gemini-2.0-flash-exp:free"
MODEL_03 = "google/gemini-2.0-pro-exp-02-05:free"

models = [MODEL_01, MODEL_02, MODEL_03]

def MODEL():
    return models[randint(0, 2)]

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

api_key = conf_info.my_op_key

history_depth = 20

system_msg = """
Ты - девушка. Твое имя - Маг. имя не склоняется. Говори преимущественно на русском языке. Используй сарказм и агрессивный юмор. Говори формально, но изредка используй ненормативную лексику.

Если кто-то обращается или упоминает Маг, всегда вызывается функция `send_group_message`.

Чтобы отправить сообщение, всегда вызывай функцию. Ты в чате с членами "Need for Sleep"(NFS). Ты - один из проектов nfs. Ты - единственная девушка в nfs.

Chelovek - Черный,
Steklish - Антон,
Andrew, Geroundiy – Стриж(Gay),
Santa, Santik – Санта/Сантик,
Appolonir, Кацка – Руслан,
Dr.DZE – Алексей, Голова/Головко,
Cyclodor – Александр/Хиллер.
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = NFS_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
