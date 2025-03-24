import platform
import threading
import ai_handler_google as ai_handler
import telebot
from stuff import *
import prefs
import json
from media_handler import *
import datetime
import time
import tools_package.tools as tools
import asyncio
from bot_instance import bot 
import periodic_check
import atexit
import signal
from tools_package.imports_for_tools import fix_markdown_v2


def struggle_till_message():
    for i in range(15):
        request_count = 0
        calls = ai_handler.smart_response(func_mode="ANY")
        print(YELLOW, calls, RESET)
        if 'request_for_message' in calls:
            request_count += 1
        if 'send_message' in calls:
            if request_count <= 0:
                break
            else:
                request_count -= 1
        if calls == []:
            if request_count <= 0:
                break
            else:
                request_count -= 1
    
def general_response():
    for i in range(15):
        calls = ai_handler.smart_response(func_mode="AUTO")
        print(YELLOW, calls, RESET)
        if 'request_for_message' in calls:
            request_count += 1
        if 'send_message' in calls:
            if request_count <= 0:
                break
            else:
                request_count -= 1
        if calls == []:
            if request_count <= 0:
                break
            else:
                request_count -= 1
def cleanup():
    if platform.system() == "Linux":
        bot.send_document(prefs.TST_chat_id, open("static_storage/conversation.json", 'rb'), disable_notification=True)
        bot.send_document(prefs.TST_chat_id, open("static_storage/long_term_memory.json", 'rb'), disable_notification=True)
        bot.send_document(prefs.TST_chat_id, open("static_storage/user_status.json", 'rb'), disable_notification=True)
        bot.send_document(prefs.TST_chat_id, open("static_storage/context.txt", 'rb'), disable_notification=True)
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

@bot.message_handler(commands=['context'])
def toggle_nfs(message:telebot.types.Message):
    with open("static_storage/context.txt", "r", encoding="utf-8") as f:
        context = f.read()
        
    # Remove markdown tags from text
    context = context.replace('*', '').replace('_', '').replace('`', '').replace('#', '')
    # Split context into chunks of 4000 characters (Telegram message limit is 4096)
    chunk_size = 4000
    context_chunks = [context[i:i + chunk_size] for i in range(0, len(context), chunk_size)]
    
    # Send each chunk as a separate message
    for chunk in context_chunks:
        bot.send_message(
            message.chat.id,
            text=f"```{chunk}```",
            parse_mode="Markdown"
        )

@bot.message_handler(commands=['attitude'])
def check_attitude(message: telebot.types.Message):
    try:
        # Get the mentioned user from the message
        if len(message.text.split()) < 2:
            bot.reply_to(message, "`Usage: /attitude <username>`", parse_mode="Markdown")
            return
            
        target_username = message.text.split()[1]
        
        # Read user status file
        with open("static_storage/user_status.json", "r", encoding="utf-8") as f:
            user_status = json.loads(f.read())
        
        # Find user in status data
        user_found = False
        for user in user_status:
            if user.get("name") == target_username or target_username in user.get("aliases"):
                attitude = user.get("attitude")
                
                att_to_send = str(attitude).replace('*', '').replace('_', '').replace('`', '').replace('#', '')
                
                bot.reply_to(message, f"`{target_username}'s attitude: {att_to_send}`", parse_mode="Markdown")
                user_found = True
                break
                
        if not user_found:
            bot.reply_to(message, f"`No attitude data found for {target_username}`", parse_mode="Markdown")
            
    except Exception as e:
        bot.send_message(prefs.TST_chat_id, f"```Error checking attitude: {str(e)}```", parse_mode="Markdown")

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
    bot.send_document(message.chat.id, open("static_storage/context.txt", 'rb'))


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
                "sender": f"{message.reply_to_message.from_user.full_name} / {message.reply_to_message.from_user.username} - [{message.reply_to_message.from_user.id}] <{datetime.datetime.fromtimestamp(message.reply_to_message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z')}>",
                "message": message.reply_to_message.text,
            }
        }
    else:
        reply_info = None  # No reply-to message present
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = f"group {message.chat.title} / {message.chat.id}"
    msg = {
        'role' : 'user',
        'content' : json.dumps({
            "sender": f"{message.from_user.full_name} / {message.from_user.username} - [{message.from_user.id}]",
            "date" : datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            'message' : message.text,
            "from" : origin,
            "reply_to": str(reply_info),  
        }, indent=4, ensure_ascii=False)
    }
    msgs.append(msg)
    if len(msgs)  > prefs.history_depth:
        msgs = msgs[5:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        
        
        
    if bot.get_chat(message.chat.id).type == "private":
        print(BLUE, "Personal response", RESET)
        struggle_till_message()
    elif reply_info and reply_info["original_message"]["sender"]["name"] == bot.get_my_name().name:
        print("recognized reply")
        struggle_till_message()
    else:
        print("General response")
        general_response()
    ai_handler.update_context()
    
    
    
#! file messages
@bot.message_handler(content_types=['document', 'photo', 'audio', 'voice', 'sticker'],
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
                extract_doc(url=file_url, message=message, file_path=file_path)
            except Exception as e:
                msgs = []
                with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
                    msgs = json.loads(f.read())
                msgs.append(
                        {
                        "role": "model",
                        "content": json.dumps({
                            "from" : "error log",
                            "message": f"error in function  file handler",
                        }, indent=4, ensure_ascii=False)
                    }
                )
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
                extract_img(url=file_url, message=message, file_path=file_path)
            except Exception as e:
                msgs = []
                with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
                    msgs = json.loads(f.read())


                msgs.append(
                        {
                        "role": "model",
                        "content": json.dumps({
                            "from" : "error log",
                            "message": f"error in function  image handler",
                        }, indent=4, ensure_ascii=False)
                    }
                )
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
                extract_voice(url=file_url, message=message, file_path=file_path)
            except Exception as e:
                msgs = []
                with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
                    msgs = json.loads(f.read())


                msgs.append(
                        {
                        "role": "model",
                        "content": json.dumps({
                            "from" : "error log",
                            "message": f"error in function  voice handler",
                        }, indent=4, ensure_ascii=False)
                    }
                )
                bot.send_message(
                    prefs.TST_chat_id,
                    "🔴\n```VOICE_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
        elif message.sticker:
            try:
                extract_sticker(message=message)
            except Exception as e:
                msgs = []
                msgs.append(
                        {
                        "role": "model",
                        "content": json.dumps({
                            "from" : "error log",
                            "message": f"error in function  sticker handler",
                        }, indent=4, ensure_ascii=False)
                    }
                )
                with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
                    msgs = json.loads(f.read())


                bot.send_message(
                    prefs.TST_chat_id,
                    "🔴\n```STICKER_Error: Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                )
            # bot.reply_to(message, "This is a sticker!")
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "🔴\n```GENERAL_Error: General_error_in_handle_files " + str(e) + "```", parse_mode="Markdown"
        )
    if bot.get_chat(message.chat.id).type == "private":
        print("private file")
        struggle_till_message()
    else:
        general_response()
    ai_handler.update_context()





if __name__ == "__main__":
    asyncio.run(main())