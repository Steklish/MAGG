from datetime import datetime
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
            "Use this tool to send messages to the group chat. "
            "Respond when mentioned or addressed, and actively engage in conversations by using this function."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text of the message to send in the group chat."
                }
            },
            "required": ["message"]
        }
    }
}


create_memory_tool = {
    "type": "function",
    "function": {
        "name": "create_memory",
        "description": (
            "User wont explicitly call it, you have to decide when to use the tool. Use this to store meaningful moments, patterns, insights, and user preferences for long-term personalization. "
            "Log emotional reactions, exciting discussions, funny exchanges, and important topics. "
            "For reminders, include the date in DD-MM format and set 'is_reminder' to true."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "A detailed memory entry, including emotional context if applicable."
                },
                "is_reminder": {
                    "type": "boolean",
                    "description": "Set to true to surface the memory as a reminder on the specified date."
                }
            },
            "required": ["memory", "is_reminder"]
        }
    }
}

message_to_continue_conversation_tool = {
    "type": "function",
    "function": {
        "name": "message_to_continue_conversation",
        "description": (
            "You must use this function in order to send a message to the chat. Use it if you feel like sending a message for whatewer reason."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The follow-up message to send."
                }
            },
            "required": ["message"]
        }
    }
}


long_term_memory_tool = {
    "type": "function",
    "function": {
        "name": "get_long_term_memory",
        "description": (
            "Always use if contet is not clear or if you meet a word the meaning you can get. Alwaus use it to get info about peoplpe and objects or events/"
            "Retrieve relevant stored knowledge to enhance responses and provide personalized experiences. "
            "Filter using diverse and meaningful keywords, including specific dates (DD-MM). "
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A diverse set of 4 to 7 keywords for effective filtering."
                }
            },
            "required": ["keywords"]
        }
    }
}


one_more_message_tool = {
    "type": "function",
    "function": {
        "name": "one_more_message",
        "description": "Call this every time you want to sent a message. Use to express your thoughts",
    }
}
    
non_stop_tool = {
    "type": "function",
    "function": {
        "name": "non_stop",
        "description": (
            "Use this tool when you wefe asked for something to send message."),
        "parameters": None
    }
}



TOOLS = [
    long_term_memory_tool,
    create_memory_tool,
    send_group_message_tool,
    message_to_continue_conversation_tool,
    non_stop_tool
]

def normalize_string(text):
    return unicodedata.normalize('NFKD', text).encode('utf-8', errors='ignore').decode('utf-8')

@log_blue
def execute_tool(tool_name, args):
    # args = normalize_string(args)
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    res = eval(tool_name)(**json.loads(args))
    print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
    return res
    
def one_more_message():
    return "go for one more message to sent to group"


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
        'date': datetime.now().strftime('%d-%m-%y-%H-%M'),
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
    # Open the file and load the reminders
    with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
        reminders = json.load(f)

    # Find reminders that match the given date
    matching_reminders = [reminder for reminder in reminders if reminder['date'] in date]

    # Remove the matching reminders from the original list
    reminders = [reminder for reminder in reminders if reminder['date'] not in date]

    # Write the updated list back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        json.dump(reminders, f, indent=4, ensure_ascii=False)

    # Return the matching reminders (or a message if none were found)
    if not matching_reminders:
        return "No matching reminders found for today"
    else:
        return json.dumps(matching_reminders, indent=4, ensure_ascii=False)




def send_group_message(message:str):
    print(GREEN, "Decided to answer", RESET)
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
                "```Cannot_send_response(sm_rs) " + str(e) + "```", parse_mode="Markdown"
            )
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, indent=4, ensure_ascii=False))




def message_to_continue_conversation(message:str):
    print(GREEN, "Decided to answer", RESET)
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
                "```Cannot_send_response(sm_rs) " + str(e) + "```", parse_mode="Markdown"
            )
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, indent=4, ensure_ascii=False))
    
    
        

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
        
        resp = client.chat.completions.create(
            model=prefs.MODEL,
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
                    non_stop()
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
    
    
