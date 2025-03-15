import datetime
from stuff import *
import json
from bot_instance import bot
import prefs
from bot_instance import *
from stuff import *

    

def send_to_chat(message:str):
    # print(GREEN, "Decided to answer", RESET)
    messages = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        messages = json.loads(f.read())
    
    print(f"{MAGENTA}{message}{RESET}")
    
    try:
        bot.send_message(
            prefs.chat_to_interact, 
            normalize_string(message),
            parse_mode="Markdown"
        )

        return 0
    except Exception as e: 
        print(e)
        bot.send_message(
                prefs.TST_chat_id,
                "🔴\n```Cannot_send_response \n(send_to_chat)\n " + str(e) + "```", parse_mode="Markdown"
            )
        return 1
