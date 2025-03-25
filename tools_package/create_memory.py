from .imports_for_tools import *

google_create_memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="create_memory",
            description=(
                "Store important information."
                "Use create_memory to save emotional moments or significant information for future use make a detailed descriptive notes. Dont create similar memories."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "memory": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "Detailed note in Russian. Include names, dates, emotional tone and all the relevant details. Describe exhaustively. Provide colorful picture of the event"
                            "Provide tags to refer to this memory in the future."
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
       



