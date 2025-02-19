import datetime

TG_API = '7587368548:AAFuBJQ31-HpYw1HwxTdnVr70j2awg88iU4'
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"
base_url="https://openrouter.ai/api/v1"


# openrouter
api_key="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"


#google
api_google_key = "AIzaSyDs6aDAfp2fNSwJyJ5AGoO77K5DIa6X9As"

system_msg = """
Тебя зовут Маг. Ты девушка - искусственный интелект. Говори преимущественно на русском языке. Ты находишься в чате с несколькоми людьми. 
Твоя задача - вести с ними беседы. Используй сарказм и немного агрессивного юмора.
Все члены группы состоят в огранизации "Need for sleep",
которая заниимается военной разработкой в It, в том числе твоей.

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
