from ai_handler import client as OR_client
from ai_handler import client_google as client
import telebot
from stuff import *
import prefs
import json
from media_handler import *
import tools
import datetime


# Telegram creds
from bot_instance import bot 
bot.send_message(prefs.chat_to_interact, "👩🏻‍🦼👩🏻‍🦼👩🏻‍🦼💨 host started 👩🏻‍🦼👩🏻‍🦼👩🏻‍🦼💨")

def smart_response():
    try:
        print(GREEN)
        print("Smart message launched", RESET)
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sys_m = {
                'role': 'system',
                'content': f"""настоящие время и дата {current_datetime}
                {prefs.system_msg}
                """
            }
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())
        # print(json.dumps([sys_m, *msgs], indent=4, ensure_ascii=False))
        # print(YELLOW, json.dumps([sys_m, *msgs], ensure_ascii=False), RESET)
        
        resp = OR_client.chat.completions.create(
            model=prefs.MODEL,
            messages = [sys_m, *msgs],
            tool_choice='auto',
            tools=tools.TOOLS,
            parallel_tool_calls=True,
            stream=False
        )
        print(resp)
        
        # if resp.id is None:
        #     bot.send_message(
        #                 prefs.TST_chat_id,
        #                 "```Error_from_AI_client```", parse_mode="Markdown"
        #             )
        #     return
        
        plain_text = ''
        
        plain_text = resp.choices[0].message.content
        func_raw = resp.choices[0].message.tool_calls
        
        # print(f"{RED}{plain_text}{RESET}")
        
        if func_raw is not None:
            for call in func_raw:
                func_name = call.function.name
                func_params = call.function.arguments
                call_id = call.id
                call_type = call.type
                call_index = call.index
                res = None
                msgs.append(
                                {
                                    "role": "assistant",
                                    "function_call": {
                                        'tool_call_id' : str(call_id),
                                        "name" : str(func_name),
                                        # "type" : str(call_type),
                                        # "index" : str(call_index),
                                        # "arguments" : str(func_params)
                                    }
                                }
                            )
                
        
        
        
                # !FUNCTION EXECUTION
        
                try:
                    res = tools.execute_tool(func_name, func_params)
                    if func_raw[0].function.name == "send_group_message":
                        continue
                    if res is None: res = 'no return'
                    shoul_call_once_more = True
                    #success log    
                    
                
                    msgs.append(
                                    {
                                        'role': 'function',
                                        "name" : str(func_name),
                                        'output': str(res),
                                        # "type" : str(call_type),
                                        # "index" : str(call_index),
                                        'tool_call_id' : str(call_id)
                                    }
                                )
                    
                    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
                        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
                    force_response()
                    smart_response()
                except Exception as e: 
                    print(e)
                    bot.send_message(
                            prefs.TST_chat_id,
                            "```Cannot_execute_tool " + str(e) + "```", parse_mode="Markdown"
                        )
        else:
            print(YELLOW, "deciced to stay silent...", RESET)
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "```Cannot_send_response_very_BAD  (smart response)" + str(e) + "```", parse_mode="Markdown"
        )    

def force_response():
    try:
        print("Forced message")
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sys_m = {
                'role': 'system',
                'content': f"""настоящие время и дата {current_datetime}
                {prefs.system_msg}
                """
            }
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())
        # print(json.dumps([sys_m, *msgs], indent=4, ensure_ascii=False))
        # print(YELLOW, json.dumps([sys_m, *msgs], ensure_ascii=False), RESET)
        
        resp = OR_client.chat.completions.create(
            model=prefs.MODEL,
            messages = [sys_m, *msgs],
            tool_choice='auto',
            tools=tools.TOOLS,
            parallel_tool_calls=True,
            stream=False
        )
        print(resp)
        
        # if resp.id is None:
        #     bot.send_message(
        #                 prefs.TST_chat_id,
        #                 "```Error_from_AI_client```", parse_mode="Markdown"
        #             )
        #     return
        
        plain_text = ''
        
        plain_text = resp.choices[0].message.content
        func_raw = resp.choices[0].message.tool_calls
        
        print(f"{MAGENTA}{plain_text}{RESET}")
        # print(f"{YELLOW}{func_raw}{RESET}")
        
        if plain_text is not None and plain_text != "" and plain_text != "\n":
            msgs.append(
                {
                    'role': 'assistant',
                    'content': plain_text
                }
            )
            
            try:
                bot.send_message(
                    prefs.chat_to_interact, 
                    plain_text,  # Fix payload encoding issue
                    parse_mode="Markdown"
                )
            except Exception as e: 
                print(e)
                bot.send_message(
                        prefs.TST_chat_id,
                        "```Cannot_send_response " + str(e) + "```", parse_mode="Markdown"
                    )
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        
        
        
        if func_raw is not None:
            for call in func_raw:
                func_name = call.function.name
                func_params = call.function.arguments
                call_id = call.id
                call_type = call.type
                call_index = call.index
                res = None
                msgs.append(
                                {
                                    "role": "assistant",
                                    "function_call": {
                                        'tool_call_id' : str(call_id),
                                        "name" : str(func_name),
                                        # "type" : str(call_type),
                                        # "index" : str(call_index),
                                        # "arguments" : str(func_params)
                                    }
                                }
                            )
                
        
        
        
                # !FUNCTION EXECUTION
        
                try:

                    res = tools.execute_tool(func_name, func_params)
                    if res is None: res = 'no return'
                    shoul_call_once_more = True
                    #success log    
                    
                
                    msgs.append(
                                    {
                                        'role': 'function',
                                        "name" : str(func_name),
                                        'output': str(res),
                                        # "type" : str(call_type),
                                        # "index" : str(call_index),
                                        'tool_call_id' : str(call_id)
                                    }
                                )
                    
                    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
                        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
                    force_response()
                except Exception as e: 
                    print(e)
                    bot.send_message(
                            prefs.TST_chat_id,
                            "```Cannot_execute_tool " + str(e) + "```", parse_mode="Markdown"
                        )
    except Exception as e:
        bot.send_message(
            prefs.TST_chat_id,
            "```Cannot_send_response_very_BAD (force response) " + str(e) + "```", parse_mode="Markdown"
        )
        
        
    
    
@bot.message_handler(func=lambda message: str(message.chat.id) == prefs.chat_to_interact)
def process_any_msg(message:telebot.types.Message):
    
    
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())        
    msg = {
        'role' : 'user',
        'content' : json.dumps({
            "sender" : {
                'name' : message.from_user.full_name,
                'username' : message.from_user.username
                },
            "date" : datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            'message' : message.text
        }, indent=4, ensure_ascii=False)
    }
    msgs.append(msg)
    if len(msgs)  > prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
    smart_response()  
    # force_response()
  
@bot.message_handler(content_types=['document', 'photo', 'video', 'audio', 'voice'], func=lambda message: str(message.chat.id) == prefs.chat_to_interact)
def handle_files(message):
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
        
    force_response()
try:    
    bot.polling()
except Exception as e:
    bot.send_message(
        prefs.TST_chat_id,
        "```TELEGRAM ERROR```", parse_mode="Markdown"
    )
@bot.message_handler(commands=["alive"])
def is_alive(message):
    bot.send_message(
        prefs.TST_chat_id,
        "```STATUS CHECK```", parse_mode="Markdown"
    )