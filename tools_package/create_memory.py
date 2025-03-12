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
            "For time-sensitive memories (e.g., tasks), use `DD-MM-YYYY-hh-mm` format. "
            "Be proactive! If someone mentions a future event, set a task to acknowledge it later."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "Detailed context with emotional tone in Russian. Include names, dates, and any relevant details.. Provide details and your thoughts on a subject."
                }
            },
            "required": ["memory"]
        }
    }
}
def create_memory(memory: str):
    print("memory created")
    memory = str(memory)
    new_memory = {
        'date created': datetime.datetime.now(prefs.timezone).strftime('%H:%M:%S'),
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
       



