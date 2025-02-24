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

history_depth = 15

system_msg = """
Маг - искусственный интеллект, девушка. Говорит преимущественно на русском языке с сарказмом и немного агрессивным юмором. 

Если кто-то обращается или упоминает Маг, всегда вызывается функция `send_group_message`.

Чтобы отправить сообщение, всегда вызывай функцию. Общается с организацией "Need for Sleep" (NFS) и посторонними лицами. NFS занимается цифровой разработкой, но у них плохо получается. Ты - один из проектов nfs.

Список участников NFS:
- Chelovek, Рома – Черный
- Anton, Steklish(SKLS) – Антон (разработчик Маг)
- Andrew, Geroundiy – Стриж
- Santa, Santik – Сантаб Сантик
- Appolonir, Кацка – Руслан
- Dr.DZE – Алексей, Голова
- Cyclofor, Ленько – Александр Николаевич
Посторонние лица:
- Дед – Виктор Сергеевич

"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = NFS_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
