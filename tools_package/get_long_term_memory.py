from .imports_for_tools import *


long_term_memory_tool = {
    "type": "function",
    "function": {
        "name": "get_long_term_memory",
        "description": (
            "ALWAYS USE FIRST when context is unclear or when names/dates are mentioned. "
            "Crucial for: - Identifying people - Recalling events - Understanding references "
            "Effective keyword strategies: Combine names, dates (DD-MM-YYYY), locations, and unique terms. Use this along with any tool to send a message."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "4-7 varied search terms. Example: ['Alex', 'birthday', '15-08', 'Paris trip', '2024']"
                }
            },
            "required": ["keywords"]
        }
    }
}

def get_long_term_memory(keywords: list[str]):
    with open("static_storage/long_term_memory.json", "r", encoding="utf-8") as f:
        memories = json.load(f)
    
    # Filter memories based on keywords (case-insensitive)
    filtered_memories = []
    for memory in memories:
        if any((keyword.lower() in memory['content'].lower() or keyword.lower() in memory['date'].lower()) for keyword in keywords):
            filtered_memories.append(memory)
    if filtered_memories == []:
        return "No matching memories found"
    else:
        
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
            
        client.api_key = prefs.open_r_key()
        response = client.chat.completions.create(
            model=prefs.MODEL(),
            messages=[
                prefs.system_msg_char,
                *conversation,
                {
                    'role' : 'user',
                    'extra' : 'reminder time has come',
                    'content' : json.dumps(filtered_memories, ensure_ascii=False) + 'give a summary, capture important detailes to the current context. format the output as your own memories.',
                }
            ],
            # tools=tools.TOOLS,
            # tool_choice="auto",
            temperature=1.2
            # top_p=0.9
        )
        print(response)
        return normalize_string(response.choices[0].message.content)


