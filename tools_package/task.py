from .imports_for_tools import *


setup_task_tool = {
    "type": "function",
    "function": {
        "name": "setup_task",
        "description": (
            "PROACTIVE TASK CREATION: form tasks to preform in specific time to have an ability to alert user or preform a specific action"
            "Examples: - User asks to remind them about ones bithday the day before."
            "Be proactive! If it wold be fun or important to remind user something in the future,  make a task."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": "Detailed description of the task including any instructions."
                },
                "time_to_exec": {
                    "type": "string",
                    "description": "Exact time for the task to be executed in `DD-MM-YYYY-hh-mm` format."
                }
            },
            "required": ["memory", "time_to_exec"]
        }
    }
}

def setup_task(memory: str, time_to_exec:str):
    print("TASK ACCEPTED")
    memory = str(memory)
    new_memory = {
        'is_task' : True,
        'date created': datetime.datetime.now(prefs.timezone).strftime('%H:%M:%S'),
        'content': memory + " " + time_to_exec
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
                "```TASK_ACCEPTED \n" + str(new_memory) + "```", parse_mode="Markdown"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
       



