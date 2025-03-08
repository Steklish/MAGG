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
    # print(f"{YELLOW}{func_raw}{RESET}")
    
    try:
        bot.send_message(
            prefs.chat_to_interact, 
            normalize_string(message),
            parse_mode="Markdown"
        )
        # print("sent to the chat successfully")
        messages.append(
            {
                'role': 'assistant',
                'content': normalize_string(message)
            }
        )
        # print(messages)
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(messages, indent=4, ensure_ascii=False))
        return 0
    except Exception as e: 
        print(e)
        bot.send_message(
                prefs.TST_chat_id,
                "```Cannot_send_response \n(sm_rs)\n " + str(e) + "```", parse_mode="Markdown"
            )
        return 1
