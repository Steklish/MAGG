import prefs
import datetime
from stuff import *
from google.genai import client, types
import json
from openai import OpenAI
import tools
from bot_instance import bot
# Initialize original GOOGLE client
client_google = client.Client(api_key=prefs.api_google_key)

# Initialize openrouter client
client = OpenAI(base_url=prefs.base_url, api_key=prefs.api_key)


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
        
        resp = client.chat.completions.create(
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
        
        resp = client.chat.completions.create(
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
        
        
    