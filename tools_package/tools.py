#gene.ral import
from .imports_for_tools import *

# each tool import
from .create_memory import *
from .get_long_term_memory import *
from .send_group_messgae import *
from .send_private_message import *

TOOLS = [
    long_term_memory_tool,
    create_memory_tool,
    send_group_message_tool,
    send_private_message_tool
]



def execute_tool(tool_name, args):
    # args = normalize_string(args)
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    res = eval(tool_name)(**json.loads(args))
    print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
    return res

# ! force messagging
def non_stop():
    try:
        print("Non-stop message")
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
        client.api_key = prefs.open_r_key()
        resp = client.chat.completions.create(
            model=prefs.MODEL(),
            messages = [sys_m, *msgs],
            tool_choice='auto',
            tools=TOOLS,
            parallel_tool_calls=True,
            stream=False,
        )
        print(resp)
        plain_text = ''
        
        plain_text = resp.choices[0].message.content
        func_raw = resp.choices[0].message.tool_calls
        
        print(f"{MAGENTA}{plain_text}{RESET}")
        # print(f"{YELLOW}{func_raw}{RESET}")
        
        if plain_text is not None and plain_text != "" and plain_text != "\n":
            try:
                bot.send_message(
                    prefs.chat_to_interact, 
                    plain_text,  # Fix payload encoding issue
                    parse_mode="Markdown"
                )
                msgs.append(
                    {
                        'role': 'assistant',
                        'content': plain_text
                    }
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

                        res = execute_tool(func_name, func_params)
                        if res is None: res = 'no return'
                        
                    
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
    