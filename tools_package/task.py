from .imports_for_tools import *


google_instruct_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="instruct",
            description=(
                "Use this tool to launch an interaction cycle in a certain time. Instruct yourself with this tool."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "memory": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "Information of what you wanna do. May also include instructions on setting following instructions. May include conditions rather than plain commands. Describe also what information you will need to execute the instruction. Include some options of performing the task. Provide date that will be useful for execution in future. format this as inner thoughts or plans."
                        ),
                    ),
                    "time_to_exec": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "The time for the instruction to be executed, in DD-MM-YYYY-hh-mm format."
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
    # Check if memory exists in the current tasks
    try:
        with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
            existing_memories = json.load(f)
            for existing_memory in existing_memories:
                if existing_memory.get('is_task') and existing_memory.get('content') == memory + " " + time_to_exec:
                    print(RED,"TASK ALREADY EXISTS", RESET)
                    return "[error]TASK ALREADY EXISTS"
    except FileNotFoundError:
        existing_memories = []

    new_memory = {
        'is_task': True,
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
                # "🔵\n```TASK_ACCEPTED \n" + str(new_memory['content']) + "```", parse_mode="Markdown"
                "🔵"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
       



