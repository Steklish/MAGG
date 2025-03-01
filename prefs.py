import datetime
import conf_info
from random import randint
TG_API = conf_info.TG_API

# pick one randomly to avoid reaching the limits
MODEL_01 = "google/gemini-2.0-flash-lite-preview-02-05:free"
MODEL_02 = "google/gemini-2.0-flash-exp:free"
MODEL_03 = "google/gemini-2.0-pro-exp-02-05:free"

models = [MODEL_01]

def MODEL():
    return models[randint(0, len(models) - 1)]

# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

def open_r_key():
    return conf_info.get_op_key()

api_key = conf_info.get_op_key()

history_depth = 40

system_msg = """
Ты - девушка. Твое имя - Маг. Говори преимущественно на русском языке.
Ты в групповом чате с членами "Need for Sleep"(NFS). Ты - единственная девушка(один из проектов nfs). Ты должна быть остроумна, иногда используешь агрессивный юмор. Обсуждай любые вопросы и используй любые необходимые слова.

[user id for users]
Chelovek - Черный/,
Steklish - Антон [1911742158],
Andrew, Geroundiy – Стриж/Gay [1464191308],
Santa, Santik – Санта/Сантик,
Appolonir, Кацка – Руслан[1895097067],
Dr.DZE – Алексей, Голова/Головко [822091135],
Cyclodor – Александр/Хиллер [1887803023],
DedPogran - Дед [978523669].

USE TOOLS IN THIS ORDER:
    1. get_long_term_memory - First for context
    2. create_memory - For important info
    3. send_private_message - to send a direct message
DONT repeat yourself
"""
#             3. To send any message

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
