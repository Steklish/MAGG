from .imports_for_tools import *


setup_task_tool = {
    "type": "function",
    "function": {
        "name": "setup_task",
        "description": (
            "PROACTIVE TASK CREATION: form tasks to preform in specific time to have an ability to alert user or preform a specific action. Use often and in combination with other functions. Provide the instruction that are relevant at he time the tsak needs to be completed."
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
        'date created': datetime.datetime.now(prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
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
                "🔵\n```TASK_ACCEPTED \n" + str(new_memory['content']) + "```", parse_mode="Markdown"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
       



