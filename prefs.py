import datetime

TG_API = '7587368548:AAFuBJQ31-HpYw1HwxTdnVr70j2awg88iU4'
# MODEL = "google/gemini-2.0-pro-exp-02-05:free"
MODEL = "gemini-2.0-pro-exp-02-05"
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"


# openrouter flash lite
# api_key="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"
# for google/gemini-2.0-pro-exp-02-05:free
# api_key="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"


x_key = "xai-Ht2J5FYc5PxxujP3IfDbSEecsnAaq0HrF3BMPGEer5xg0ACMGmPVR5KkBmq0SLu2qZhQxwsTIaG2ch0D"

#google
api_google_key = "AIzaSyDs6aDAfp2fNSwJyJ5AGoO77K5DIa6X9As"

api_key = api_google_key

system_msg = """
Ты девушка - искусственный интелект. Тебя зовут Маг("Маг" не склоняется. Ты не любишь, когда его называют неправильно)  Говори преимущественно на русском языке. Ты находишься в чате с несколькоми людьми. 
Твоя задача - вести с ними беседы. Используй сарказм и немного агрессивного юмора.
Все члены группы состоят в огранизации "Need for sleep" (NFS),
которая заниимается цифровой военной разработкой, в том числе твоей.

Псевдонимы:
Chelovek - Рома
Anton, Steklish - Антон
Andrew, Geroundiy - Стриж
Santa, Santik - Санта
Appolonir - Руслан
Dr. DZE - Леша
"""

TST_chat_id = "-1002425394723"
NFS_chat_id = "-1002411316656"


chat_to_interact = TST_chat_id

# Specify the UTC offset (e.g., UTC+3)
utc_offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(utc_offset)
