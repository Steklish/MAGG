import random
import ai_handler
import telebot
from stuff import *
import prefs
import json
from media_handler import *
import datetime
import time
import tools_package.tools as tools
# Telegram creds
from bot_instance import bot 
def start_loop():
    try:    
        bot.polling(non_stop=True)
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "```TELEGRAM_ERROR \n" + str(e) + "```", parse_mode="Markdown"
        )
        time.sleep(5)
        start_loop()
    
@bot.message_handler(commands=["ok"])
def is_alive(message):
    bot.send_message(
        prefs.TST_chat_id,
        "```STATUS_CHECK```", parse_mode="Markdown"
    )    

@bot.message_handler(commands=['nfs'])
def send_file(message:telebot.types.Message):
    if prefs.chat_to_interact == prefs.NFS_chat_id:
        bot.send_message(
            message.chat.id,
            "`CURRENTLY IS SET TO NFS`", parse_mode="Markdown"
        )
    else:
        prefs.chat_to_interact = prefs.NFS_chat_id
        
        bot.send_message(
            message.chat.id,
            "`REDIRECTING TO NFS`", parse_mode="Markdown"
        )


@bot.message_handler(commands=['chat'])
def send_file(message:telebot.types.Message):
    bot.send_message(
            message.chat.id,
            f"`{bot.get_chat(prefs.chat_to_interact).title}`", parse_mode="Markdown"
        )

@bot.message_handler(commands=['tst'])
def send_file(message:telebot.types.Message):
    if prefs.chat_to_interact == prefs.TST_chat_id:
        bot.send_message(
            message.chat.id,
            "`CURRENTLY IS SET TO TST`", parse_mode="Markdown"
        )
    else:
        prefs.chat_to_interact = prefs.TST_chat_id
        
        bot.send_message(
            message.chat.id,
            "`REDIRECTING TO TST`", parse_mode="Markdown"
        )


@bot.message_handler(commands=['bio'])
def send_file(message:telebot.types.Message):
    bot.send_document(message.chat.id, open("static_storage/conversation.json", 'rb'))
    bot.send_document(message.chat.id, open("static_storage/long_term_memory.json", 'rb'))
        


# ! general message
@bot.message_handler(func=lambda message: str(message.chat.id) == prefs.chat_to_interact or 
                     bot.get_chat(message.chat.id).type == "private")
def process_any_msg(message:telebot.types.Message):
    
    
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())        
        
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    msg = {
        'role' : 'user',
        'content' : json.dumps({
            "sender" : {
                'name' : message.from_user.full_name,
                'username' : message.from_user.username,
                "user_id" : message.from_user.id,
                },
            "date" : datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            'message' : message.text,
            "from" : origin,
        }, indent=4, ensure_ascii=False)
    }
    msgs.append(msg)
    if len(msgs)  > prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
    
    
    ai_handler.smart_response()
    
@bot.message_handler(content_types=['document', 'photo', 'video', 'audio', 'voice'],
                     func=lambda message: str(message.chat.id) == prefs.chat_to_interact or 
                     bot.get_chat(message.chat.id).type == "private")
def handle_files(message:telebot.types.Message):
    file_url = None
    try:
        if message.document:
            try:
                file_info = bot.get_file(message.document.file_id)
                file_path = file_info.file_path
                file_url = f"https://api.telegram.org/file/bot{prefs.TG_API}/{file_path}"
                print("DOCUMENT")
                extract_doc(file_url, message, file_path)
            except Exception as e:
                bot.send_message(
                    prefs.TST_chat_id,
                    "```DOCUMENT_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
        elif message.photo:
            try:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_path = file_info.file_path
                file_url = f"https://api.telegram.org/file/bot{prefs.TG_API}/{file_path}"
                print("PHOTO")
                extract_img(file_url, message, file_path)
            except Exception as e:
                bot.send_message(
                    prefs.TST_chat_id,
                    "```PHOTO_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
        # elif message.video:
        #     try:
        #         file_info = bot.get_file(message.video.file_id)
        #         print("VIDEO")
        #     except Exception as e:
        #         bot.send_message(
        #             prefs.TST_chat_id,
        #             "```VIDEO_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
        #         )
        # elif message.audio:
        #     try:
        #         file_info = bot.get_file(message.audio.file_id)
        #         print("AUDIO")
        #     except Exception as e:
        #         bot.send_message(
        #             prefs.TST_chat_id,
        #             "```AUDIO_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
        #         )
        elif message.voice:
            try:
                file_info = bot.get_file(message.voice.file_id)
                file_path = file_info.file_path
                file_url = f"https://api.telegram.org/file/bot{prefs.TG_API}/{file_path}"
                print("VOICE", file_url)
                extract_voice(file_url, message, file_path)
            except Exception as e:
                bot.send_message(
                    prefs.TST_chat_id,
                    "```VOICE_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "```GENERAL_Error: General_error_in_handle_files " + str(e) + "```", parse_mode="Markdown"
        )
    ai_handler.smart_response()
    if random.randint(1, 3) == 3:    
        tools.non_stop()
start_loop()
# bot.polling()
    
