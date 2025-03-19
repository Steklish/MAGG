from .imports_for_tools import *

google_create_memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="create_memory",
            description=(
                "PROACTIVE MEMORY CREATION: Store important information to enhance interactions. "
                "Use this tool to remember emotional exchanges, future plans, or personal preferences. "
                "- Repeated behavior patterns. - Future plans (e.g., meetups, trips). "
                "- Personal preferences (e.g., favorite food, hobbies). "
                "For time-sensitive memories (e.g., tasks), use `DD-MM-YYYY-hh-mm` format."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "memory": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "Detailed context with emotional tone in Russian. Include names, dates, and any relevant details. "
                            "Provide details and your thoughts on a subject."
                        ),
                    ),
                },
                required=["memory"],
            ),
        ),
    ]
)

def create_memory(memory: str):
    print("memory created")
    memory = str(memory)
    new_memory = {
        'date created': datetime.datetime.now(prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
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
                "🟢\n```MEMORY_CREATED \n" + str(new_memory) + "```", parse_mode="Markdown"
            )
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        # PermissionError(memories)
        json.dump(memories, f, indent=4, ensure_ascii=False)
        
        
    return "memory successfully created"
       



