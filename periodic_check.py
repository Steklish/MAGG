from bot_instance import bot
import datetime
import json
import re
import ai_handler
import asyncio
from stuff import *
import tools_package.tools as tools
import prefs

async def check_state():
    while True:
        print(YELLOW, "tick", RESET)
        reminder_check()
        # repeat every 5 minutes
        await asyncio.sleep(5*60)
        
        

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
    # Write the updated memories back to the file
    with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
        json.dump(old_memories, f, indent=4, ensure_ascii=False)
    
    for task in to_remind:
        found = True
        msg = {
            'role': 'user',
            'content': f"{task['content']}",
        }
        
        while 1:
            calls = ai_handler.smart_response(tool_choice="required", messages=[prefs.system_msg(), msg])
            if 'send_private_message' in calls or 'send_group_message' in calls:
                break

            print(RED, "did not send a message (from task handler)", RESET)            
        bot.send_message(
            prefs.TST_chat_id,
            "`TASK complete`", parse_mode="Markdown"
        )   
    return found