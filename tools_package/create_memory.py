from .imports_for_tools import *

create_memory_tool = {
    "type": "function",
    "function": {
        "name": "create_memory",
        "description": (
            "PROACTIVE MEMORY CREATION: Store important information to enhance interactions. "
            "Use this tool to remember emotional exchanges, future plans, or personal preferences. "
            "Examples: - User mentions a birthday or anniversary. - Emotional conversations. "
            "- Repeated behavior patterns. - Future plans (e.g., meetups, trips). "
            "- Personal preferences (e.g., favorite food, hobbies). "
            "For time-sensitive memories (e.g., reminders), use `DD-MM-YYYY-hh-mm` format. "
            "Be proactive! If someone mentions a future event, set a reminder to acknowledge it later."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "Detailed context with emotional tone. Include names, dates, and any relevant details."
                },
                "is_reminder": {
                    "type": "boolean",
                    "description": "True for time-sensitive memories (e.g., birthdays, meetings). False for general knowledge. Always include a `DD-MM-YYYY-hh-mm` formatted time for reminders."
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
       



