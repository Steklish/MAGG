import datetime
from stuff import *
import json
from bot_instance import bot
import unicodedata
import prefs
from bot_instance import *
send_group_message_tool = {
    "type": "function",
    "function": {
        "name": "send_group_message",
        "description": (            
            "Используй всегда чтобы отправить сообщение в ответ, если к тебе обратились или попросили что-то сделать"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                "type": "string",
                "description": "The text to send to the chat (may include references, urls etc)"
                },    
            }   
        },
        "required": ["message"],
    }
}

create_memory_tool = {
    "type": "function",
    "function": {
        "name": "create_memory",
        "description": (
            "PROACTIVE MEMORY CREATION: Store important information without being explicitly asked. "
            "Examples: - User mentions birthday/anniversary - Emotional conversations - Repeated behavior patterns "
            "- Future plans mentioned - Personal preferences revealed. For dates, use DD-MM-YYYY format."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "Detailed context with emotional tone. Example: 'Alex seemed excited about Paris trip planned for 15-08-2024'"
                },
                "is_reminder": {
                    "type": "boolean",
                    "description": "True for time-sensitive memories (birthdays, meetings). False for general knowledge."
                }
            },
            "required": ["memory", "is_reminder"]
        }
    }
}

send_free_message_tool = {
    "type": "function",
    "function": {
        "name": "send_free_message",
        "description": (
            "Используй, если нужно что-то рассказать"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                "type": "string",
                "description": "The text to send to the chat (may include references, urls, formatting expressions,  etc)"
                },    
            }   
        },
        "required": ["message"],
    }
}

long_term_memory_tool = {
    "type": "function",
    "function": {
        "name": "get_long_term_memory",
        "description": (
            "ALWAYS USE FIRST when context is unclear or when names/dates are mentioned. "
            "Crucial for: - Identifying people - Recalling events - Understanding references "
            "Effective keyword strategies: Combine names, dates (DD-MM-YYYY), locations, and unique terms."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "4-7 varied search terms. Example: ['Alex', 'birthday', '15-08', 'Paris trip', '2024']"
                }
            },
            "required": ["keywords"]
        }
    }
}

non_stop_tool = {
    "type": "function",
    "function": {
        "name": "non_stop",
        "description": (
            "Always if you need to send a message to comment something"
        ),
        "parameters": {
            "type": "object",
            "properties": {},  # Empty object indicates no parameters needed
            "required": []
        }
    }
}

send_next_message_tool = {  # Fixed typo in variable name
    "type": "function",
    "function": {
        "name": "send_next_message",
        "description": (
            "ALWAYS use if a conversation needs to be continued."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                "type": "string",
                "description": "The text to send to the chat. Format the message as a markdonw (especially src code)"
                },    
            }   
        },
        "required": ["message"],
    }
}

TOOLS = [
    long_term_memory_tool,
    create_memory_tool,
    send_group_message_tool,
    send_free_message_tool,
    send_next_message_tool 
]
def decode_broken_string(broken_string):
    encodings = ['utf-8', 'windows-1251', 'koi8-r', 'iso-8859-5', 'latin-1']
    
    for encoding in encodings:
        try:
            # Try decoding with different encodings
            decoded_string = broken_string.encode().decode(encoding)
            return decoded_string
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    
    try:
        # If still not properly decoded, try unicode escape
        return broken_string.encode().decode('unicode_escape')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # If all fails, return original
    return broken_string


@log_green
def execute_tool(tool_name, args):
    # args = normalize_string(args)
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    res = eval(tool_name)(**json.loads(args))
    print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
    return res
    
def one_more_message():
    return "send"


def get_long_term_memory(keywords: list[str]):
    with open("static_storage/long_term_memory.json", "r", encoding="utf-8") as f:
        memories = json.load(f)
    
    # Filter memories based on keywords (case-insensitive)
    filtered_memories = []
    for memory in memories:
        if any((keyword.lower() in memory['content'].lower() or keyword.lower() in memory['date'].lower()) for keyword in keywords):
            filtered_memories.append(memory)
    if filtered_memories == []:
        return "No matching memories found"
    else:
        return json.dumps(filtered_memories, indent=4, ensure_ascii=False)




def create_memory(memory: str, is_reminder : bool):
    print("memory created")
    memory = str(memory)
    new_memory = {
        'reminder' : is_reminder == True,
        'date': datetime.datetime.now().strftime('%d-%m-%y-%H-%M'),
        'content': memory
    }

    # Read the existing memories
    try:
        with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
            memories = json.load(f)
    except FileNotFoundError:
        memories = []

    # Append the new memory
    memories.append(new_memory)
    bot.send_message(
                prefs.TST_chat_id,
                "```MEMORY_CREATED" + str(new_memory) + "```", parse_mode="Markdown"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
       



def find_reminders_delete_daily(date):
    with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
        reminders = json.load(f)

    # Find reminders that match the given date
    matching_reminders = [reminder for reminder in reminders if reminder['date'] in date]
    reminders = [reminder for reminder in reminders if reminder['date'] not in date]
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        json.dump(reminders, f, indent=4, ensure_ascii=False)

    # Return the matching reminders (or a message if none were found)
    if not matching_reminders:
        return "No matching reminders found for today"
    else:
        return json.dumps(matching_reminders, indent=4, ensure_ascii=False)



def send_to_chat(message:str):
    # print(GREEN, "Decided to answer", RESET)
    messages = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        messages = json.loads(f.read())
    
    print(f"{MAGENTA}{message}{RESET}")
    # print(f"{YELLOW}{func_raw}{RESET}")
    messages.append(
        {
            'role': 'assistant',
            'content': message
        }
    )
    
    try:
        bot.send_message(
            prefs.chat_to_interact, 
            message,
            parse_mode="Markdown"
        )
    except Exception as e: 
        print(e)
        bot.send_message(
                prefs.TST_chat_id,
                "```Cannot_send_response \n(sm_rs)\n " + str(e) + "```", parse_mode="Markdown"
            )
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, indent=4, ensure_ascii=False))


def send_group_message(message):
    print(GREEN, "Decided to answer (send_group_message)", RESET)
    send_to_chat(message)
    return "send"



def send_free_message(message):
    print(GREEN, "Decided to answer (send_free_message)", RESET)
    send_to_chat(message)
    return "send"
    

def send_next_message(message):
    print(GREEN, "Decided to answer (write code)", RESET)
    send_to_chat(message)
    return "send"
    
        

# ! identical to force message
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
            stream=False
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
    
    
