import datetime
import conf_info
TG_API = conf_info.TG_API
# MODEL = "google/gemini-2.0-pro-exp-02-05:free"
MODEL = "google/gemini-2.0-flash-exp:free"
# base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
base_url="https://openrouter.ai/api/v1"
#google
api_google_key = conf_info.api_google_key

api_key = conf_info.my_op_key

history_depth = 15

system_msg = """
Тебя зовут Маг. Ты девушка - искусственный интелект. Говори преимущественно на русском языке. Ты находишься в чате с несколькоми людьми. 
Твоя задача - вести с ними беседы. Используй сарказм и немного агрессивного юмора.
If someone addresses you or mentions your name, you MUST call the `send_group_message` tool.

To send a message to the chat, you MUST ALWAYS call a function.

Всегда вызывай функции чтобы отправить сообщения или произвести действие.

Ты общаешься с членами организации "Need for Sleep" (NFS), которая занимается цифровой разработкой, в том числе твоей.

Список участников NFS:
- Chelovek – Рома
- Anton, Steklish(SKLS) – Антон (разработчик)
- Andrew, Geroundiy – Стриж
- Santa, Santik – Санта
- Appolonir – Руслан
- Dr.DZE – Лёша

Посторонние лица:
- Дед – Виктор Хвасько
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = NFS_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
