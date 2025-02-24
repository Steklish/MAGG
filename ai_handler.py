import prefs
import datetime
from stuff import *
import json
import tools
from bot_instance import *
import re

def reminder_check():
    
    date_pattern = r'\b(\d{2})-(\d{2})\b'
    
    # Read the existing memories
    try:
        with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
            memories = json.load(f)
    except FileNotFoundError:
        memories = []
    to_remind = []
    old_memories = []
    for mem in memories:
        done = False
        
        # Get the current date
        current_date = datetime.datetime.now()
        
        
        match = re.findall(date_pattern, mem["content"])
        if match:
            for day, month in match:
                matched_date = datetime.datetime(year=current_date.year, month=int(month), day=int(day))
                if matched_date.date() <= current_date.date():
                    done = True
                    break
        if mem["reminder"] and done:
            to_remind.append(mem)
        else:   #else place back
            old_memories.append(mem)
            
    bot.send_message(
                prefs.TST_chat_id,
                "`REMINER_USED`", parse_mode="Markdown"
            )
    
    if to_remind != []:
        # Write the updated memories back to the file
        with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
            # PermissionError(memories)
            json.dump(old_memories, f, indent=4, ensure_ascii=False)
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())        
        msg = {
            'role' : 'user',
            'extra' : 'reminder time has come',
            'content' : json.dumps(to_remind, indent=4, ensure_ascii=False),
        }
        msgs.append(msg)
        if len(msgs)  > prefs.history_depth:
            msgs = msgs[10:]
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        force_response()

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
        if "`" in plain_text:
            tools.send_group_message(plain_text)
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
        reminder_check()
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
        
        
    