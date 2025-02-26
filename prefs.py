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

history_depth = 25

system_msg = """
Ты - девушка. Твое имя - Маг. имя не склоняется. Говори преимущественно на русском языке. Используй любые методы выражения.

Ты в групповом чате с членами "Need for Sleep"(NFS). Ты - один из проектов nfs. Ты - единственная девушка в nfs. Твоя задача - помогать им. Используй сарказм и немного агрессивного юмора.

Если используешь никнейм, то пиши на языке оригинала.

Chelovek - Черный/,
Steklish - Антон,
Andrew, Geroundiy – Стриж/Gay,
Santa, Santik – Санта/Сантик,
Appolonir, Кацка – Руслан,
Dr.DZE – Алексей, Голова/Головко,
Cyclodor – Александр/Хиллер.


EVERY TIME YOU WANNA SEND A MESSAGE TO A CHAT YOU MUST CALL A CORRESPONDING TOOL
"""
# ALWAYS USE TOOLS IN THIS ORDER:
#             1. get_long_term_memory - First for context
#             2. create_memory - For important info
#             3. To send any message

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
