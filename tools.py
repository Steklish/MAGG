from datetime import datetime
from stuff import *
import json

import unicodedata

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

one_more_message_tool = {
    "type": "function",
    "function": {
        "name": "one_more_message",
        "description": "Call this every time you want to sent another message afer what you just said",
    }
}

@log_yellow
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

long_term_memory_tool = {
    "type": "function",
    "function": {
        "name": "get_long_term_memory",
        "description": "This is MEMORY. Always use it when you cannot get into unclear context or you need addidional information on a subject. Filtered based on provided keywords. Use this function if the user is asking to recall something related to the past, or if the context of the conversation is not clear. You can also include date formatted like this DD-MM",
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of keywords to search for in the long-term memory. These keywords help identify and filter the relevant memories to be retrieved. Pass from 4 to 7 keywords for best results"
                }
            },
            "required": ["keywords"]
        },
        "return_value": {
            "type": "string",
            "description": "A JSON-formatted string containing the relevant memories filtered based on the provided keywords."
        }
    }
}



@log_green
def create_memory(memory: str, is_reminder : bool):
    
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

    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)

create_memory_tool = {
    "type": "function",
    "function": {
        "name": "create_memory",
        "description": (
            "Always use it if you find conversation excieting or funny or important. Always memorize emotional moments." 
            "If you use it to create a reminder always insert date in DD-MM format in memory field." 
            "This function logs the current date and the memory content in a structured format."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": (
                        "The content of the memory to be stored. Provide a detailed description of the memory (also can mention the emotional flavour if possible)"
                    )
                },
                "is_reminder": {
                    "type": "boolean",
                    "description": (
                        "If true this message will rise at specified date in memory"
                    )
                }
            },
            "required": ["memory", "is_reminder"]
        },
        "return_value": {
            "type": "None",
            "description": (
                "This function does not return a value. It writes the new memory to the 'long_term_memory.json' file."
            )
        }
    }
}


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


TOOLS = [
    long_term_memory_tool,
    create_memory_tool
]
