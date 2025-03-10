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
            "ALWAYS USE FIRST when context is unclear or when names/dates are mentioned. "
            "Crucial for: - Identifying people. - Recalling events. - Understanding references. "
            "Effective keyword strategies: Combine names, dates (DD-MM-YYYY), locations, and unique terms. "
            "Example: ['Alex', 'birthday', '15-08', 'Paris trip', '2024']. "
            "Use this tool to enrich your responses with personal touches and shared memories."
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
            model=prefs.MODEL(),
            messages=[
                prefs.system_msg_char,
                *conversation,
                {
                    'role' : 'user',
                    'content' : json.dumps(filtered_memories, ensure_ascii=False) + '\n\nисходя из истории переписки и данных записей выдели данные, которые имеют отношение к контексту. Эти данные из твоей памяти. Приведи их в удобный формат. Подведи итог. Обращай внимание на даты создания заеисей в базе данных.',
                }
            ],
            temperature=(prefs.TEMPERATURE * 1.5)
        )
        print(response)
        return normalize_string(response.choices[0].message.content)


def reminder_check():
    date_time_pattern = r'\b(\d{2})-(\d{2})-(\d{4})-(\d{2})-(\d{2})\b'

    # Read the existing memories
    try:
        with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
            memories = json.load(f)
    except FileNotFoundError:
        memories = []
    to_remind = []
    old_memories = []

    # Get the current date and time in the specified timezone (prefs.timezone)
    current_datetime = datetime.datetime.now(prefs.timezone)

    for mem in memories:
        if "is_task" not in mem.keys():
            old_memories.append(mem)
            continue
        done = False

        # Search for the date-time pattern in the memory content
        match = re.findall(date_time_pattern, mem["content"])
        if match:
            for day, month, year, hour, minute in match:
                # Parse the matched date and time
                matched_datetime = datetime.datetime(
                    year=int(year),
                    month=int(month),
                    day=int(day),
                    hour=int(hour),
                    minute=int(minute)
                )
                # Add timezone info to matched_datetime (assuming the timezone is the same as prefs.timezone)
                matched_datetime = prefs.timezone.localize(matched_datetime)

                # Check if the matched date and time is in the past
                if matched_datetime <= current_datetime:
                    done = True
                    break

        # If the is_task is due, add it to the to_remind list
        if mem["is_task"] and done:
            to_remind.append(mem)
        else:
            # Otherwise, keep it in the old_memories list
            old_memories.append(mem)

    found = False
    if to_remind:
        found = True
        bot.send_message(
            prefs.TST_chat_id,
            "`TASK launched`", parse_mode="Markdown"
        )
        # Write the updated memories back to the file
        with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
            
            json.dump(old_memories, f, indent=4, ensure_ascii=False)
        
        # Add is_tasks to conversation history
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())
        msg = {
            'role': 'user',
            'content': "[HAVE TO EXEC THE TASK]\n" + json.dumps(to_remind, indent=4, ensure_ascii=False),
        }
        msgs.append(msg)
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        
    return found