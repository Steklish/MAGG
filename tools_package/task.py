from .imports_for_tools import *


google_instruct_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="instruct",
            description=(
                "Proactively create tasks to be performed in the future to execute a defined action. "
                "Use this tool in combination with other functions, to ensure efficient task management."
                "Provide instructions relevant to the time the task needs to be completed."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "memory": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "You need to provide instructions for future self. Describe in details what exactly you will have to do. May also include instructions on setting following tasks."
                        ),
                    ),
                    "time_to_exec": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "The time for the task to be executed, in DD-MM-YYYY-hh-mm format."
                        ),
                    ),
                },
                required=["memory", "time_to_exec"],
            ),
        ),
    ]
)


def instruct(memory: str, time_to_exec:str):
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
       



