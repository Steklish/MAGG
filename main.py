import platform
import random
import threading
import ai_handler
import telebot
from stuff import *
import prefs
import json
from media_handler import *
import datetime
import time
import tools_package.tools as tools
import asyncio
# Telegram creds
from bot_instance import bot 
import periodic_check
import atexit
import signal
import sys


def struggle_till_message():
    while 1: 
            calls = ai_handler.smart_response(TOOLSET=tools.TOOLS, tool_choice="required")
            if 'send_private_message' in calls or 'send_group_message' in calls:
                break
    

def cleanup():
    if platform.system() == "Linux":
        bot.send_document(prefs.TST_chat_id, open("static_storage/conversation.json", 'rb'), disable_notification=True)
        bot.send_document(prefs.TST_chat_id, open("static_storage/long_term_memory.json", 'rb'), disable_notification=True)
        bot.send_document(prefs.TST_chat_id, open("static_storage/user_status.json", 'rb'), disable_notification=True)
        bot.send_message(
                prefs.TST_chat_id,
                "`STOPPED the remote server`", parse_mode="Markdown"
                , disable_notification=True
            )

def handle_signal(signum, frame):
    cleanup()

atexit.register(cleanup)
# signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def start_loop():
    try:    
        bot.polling(non_stop=True)
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "🔴\n```TELEGRAM_ERROR \n" + str(e) + "```", parse_mode="Markdown"
        )
        time.sleep(5)
        start_loop()
    
async def main():
    # Create and launch the periodic check task
    tick = asyncio.create_task(periodic_check.check_state())
    
    # Start the non-async loop in a separate thread
    loop_thread = threading.Thread(target=start_loop)
    loop_thread.daemon = True
    loop_thread.start()

    # Keep the async task running
    await tick

@bot.message_handler(commands=["amnesia"])
def is_alive(message):
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write("[]")      
    bot.send_message(
        message.chat.id,
        "```HISTORY_CLEARED```", parse_mode="Markdown"
    )    

@bot.message_handler(commands=["ok"])
def is_alive(message):
    bot.send_message(
        message.chat.id,
        "```STATUS_CHECK```", parse_mode="Markdown"
    )    

@bot.message_handler(commands=['nfs'])
def toggle_nfs(message:telebot.types.Message):
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
def check_chat(message:telebot.types.Message):
    bot.send_message(
            message.chat.id,
            f"`{bot.get_chat(prefs.chat_to_interact).title}`", parse_mode="Markdown"
        )

@bot.message_handler(commands=['tst'])
def toggle_tst(message:telebot.types.Message):
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
def bio(message:telebot.types.Message):
    bot.send_document(message.chat.id, open("static_storage/conversation.json", 'rb'))
    bot.send_document(message.chat.id, open("static_storage/long_term_memory.json", 'rb'))
    bot.send_document(message.chat.id, open("static_storage/user_status.json", 'rb'))
        


# ! general message
@bot.message_handler(func=lambda message: str(message.chat.id) == prefs.chat_to_interact or 
                     bot.get_chat(message.chat.id).type == "private")
def process_any_msg(message:telebot.types.Message):
    
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())        
        
    if message.reply_to_message:  # Check if the message is a reply
        reply_info = {
            "original_message": {
                "sender": {
                    "name": message.reply_to_message.from_user.full_name,
                    "username": message.reply_to_message.from_user.username,
                    "user_id": message.reply_to_message.from_user.id,
                },
                "date": datetime.datetime.fromtimestamp(
                    message.reply_to_message.date, prefs.timezone
                ).strftime('%d-%m-%Y %H:%M:%S %Z'),
                "message": message.reply_to_message.text,
            }
        }
    else:
        reply_info = None  # No reply-to message present
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = f"group{message.chat.title} / {message.chat.id}"
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
            "reply_to": reply_info,  # Include reply info if present
        }, indent=4, ensure_ascii=False)
    }
    msgs.append(msg)
    if len(msgs)  > prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        
        
        
    if bot.get_chat(message.chat.id).type == "private":
        print("Personal response")
        struggle_till_message()
    elif reply_info and reply_info["original_message"]["sender"]["name"] == bot.get_my_name().name:
        print("recognized reply")
        struggle_till_message()
    else:
        print("General response")
        calls = ai_handler.smart_response(TOOLSET=tools.TOOLS, tool_choice="auto")
    ai_handler.update_context()
    
    
    
#! file messages
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
                    "🔴\n```DOCUMENT_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
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
                    "🔴\n```PHOTO_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
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
                    "🔴\n```VOICE_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "🔴\n```GENERAL_Error: General_error_in_handle_files " + str(e) + "```", parse_mode="Markdown"
        )
    if bot.get_chat(message.chat.id).type == "private":
        print("private file")
        struggle_till_message()
    else:
        ai_handler.smart_response(TOOLSET=tools.TOOLS, tool_choice="auto")
    ai_handler.update_context()
if __name__ == "__main__":
    asyncio.run(main())