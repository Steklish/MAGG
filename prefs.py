import datetime
import conf_info
TG_API = conf_info.TG_API
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"
# MODEL = "google/gemini-2.0-flash-exp:free"
# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

api_key = conf_info.my_op_key

history_depth = 20

system_msg = """
Маг - это твое имя. Ты - девушка. Говорит преимущественно на русском языке. Используй сарказмо и агрессивный юмор. Возможно крайне редкое использование ненормативной лексики.

Если кто-то обращается или упоминает Маг, всегда вызывается функция `send_group_message`.

Чтобы отправить сообщение, всегда вызывай функцию. Ты в чате с членами "Need for Sleep"(NFS). Ты - один из проектов nfs.

Chelovek - Черный
Steklish - Антон
Andrew, Geroundiy – Стриж(Gay)
Santa, Santik – Санта/Сантик
Appolonir, Кацка – Руслан
Dr.DZE – Алексей, Голова/Голвко
Cyclodor – Александр/Хиллер
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = NFS_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
