import re
from .imports_for_tools import *
import conf_info
import datetime
import json

long_term_memory_tool = {
    "type": "function",
    "function": {
        "name": "get_long_term_memory",
        "description": (
            "Periodically retrieving the context of the conversation."
            "Use this tool to recall shared experiences, historical context, names, dates, or "
            "specific events. This tool is essential for understanding references, emotional "
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
        try:
            if any((keyword.lower() in memory['content'].lower() or keyword.lower() in memory['date created'].lower()) for keyword in keywords):
                filtered_memories.append(memory)
        except Exception as e:
            print(str(e))
    if filtered_memories == []:
        return "No matching memories found"
    else:
        
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
            
        client.api_key = prefs.open_r_key()
        response = client.chat.completions.create(
            model=prefs.MODEL_NO_TOOLS,
            messages=[
                prefs.system_msg_char,
                *conversation,
                {
                    'role' : 'user',
                    'content' : json.dumps(filtered_memories, ensure_ascii=False) + '\n\nисходя из истории переписки и данных записей выдели данные, которые имеют отношение к контексту, остальное опусти. Эти данные из твоей памяти. Приведи их в удобный формат. Подведи итог. Обращай внимание на даты создания заеисей в базе данных.',
                }
            ],
            temperature=(prefs.TEMPERATURE * 1.5)
        )
        print(response)
        return normalize_string(response.choices[0].message.content)
