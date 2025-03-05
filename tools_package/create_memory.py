from .imports_for_tools import *

create_memory_tool = {
    "type": "function",
    "function": {
        "name": "create_memory",
        "description": (
            "PROACTIVE MEMORY CREATION: Store important information without being explicitly asked. "
            "Examples: - User mentions birthday/anniversary - Emotional conversations - Repeated behavior patterns "
            "- Future plans mentioned - Personal preferences revealed. For dates, use DD-MM-YYYY format."
            "Use DD-MM-YYYY-hh-mm format when setting reminders"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "Detailed context with emotional tone."
                },
                "is_reminder": {
                    "type": "boolean",
                    "description": "True for time-sensitive memories (birthdays, meetings). False for general knowledge. Always put a DD-MM-YYYY-hh-mm formatted time and date of when to trigger the reminder"
                }
            },
            "required": ["memory", "is_reminder"]
        }
    }
}

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
                "```MEMORY_CREATED \n" + str(new_memory) + "```", parse_mode="Markdown"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
       



