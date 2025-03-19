from .imports_for_tools import *


google_setup_task_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="setup_task",
            description=(
                "Proactively create tasks to be performed at a specific time, enabling the system to alert the user or execute a defined action. "
                "Use this tool frequently, in combination with other functions, to ensure efficient task management. "
                "Provide instructions relevant to the time the task needs to be completed."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "memory": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "A detailed description of the task, including any relevant instructions for its execution."
                        ),
                    ),
                    "time_to_exec": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "The exact time when the task should be executed, in `DD-MM-YYYY-hh-mm` format."
                        ),
                    ),
                },
                required=["memory", "time_to_exec"],
            ),
        ),
    ]
)


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
       



