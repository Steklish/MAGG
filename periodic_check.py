
import portalocker
from bot_instance import bot
import datetime
import json
import re
import ai_handler_google as ai_handler
import asyncio
from stuff import *
import tools_package.tools as tools
import prefs
from random import randint
from main import struggle_till_message, general_response
from daily_memory import check_for_date
import os
import time

def is_user_last_change(file_path):
    if os.path.exists(file_path):
        # Get the current time
        with open(file_path, 'r', encoding="utf-8") as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            actions = json.load(f)
            portalocker.unlock(f) 
        if len(actions) == 0:
            return False
        return (actions[-1]["role"] == "model" and (not "send_message" in actions[-1]["content"])) or actions[-1]["role"] == "user"
    else:
        print(f"File {file_path} does not exist.")
        return None
    

def minutes_since_last_change(file_path):
    """
    Calculates the number of minutes that have passed since the file was last modified.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        float: The number of minutes since the file was last modified.
               Returns None if the file doesn't exist.
    """
    if os.path.exists(file_path):
        # Get the current time
        current_time = time.time()
        # Get the last modification time
        mod_time = os.path.getmtime(file_path)
        # Calculate the difference in minutes
        return (current_time - mod_time) / 60
    else:
        print(f"File {file_path} does not exist.")
        return None

async def check_state():
    print(GREEN, "started check state", RESET)
    last_step_time = time.time()
    delay_time = 10
    while True:
        print(YELLOW, ".", RESET, end='', sep='')
        
        await asyncio.sleep(0.2)
        # reminder_check()
        check_for_date()
        # repeat every 5 minutes
        
        
        
        if time.time() - last_step_time > delay_time:
            last_step_time = time.time()
            calls = ai_handler.smart_response(func_mode="AUTO")
            if calls != []:
                ai_handler.update_context()
            
                
        time_passed = minutes_since_last_change("static_storage/conversation.json")
        
        if time_passed < 2 and is_user_last_change("static_storage/conversation.json"):
            calls = ai_handler.smart_response(func_mode="ANY")
            if "send_message" in calls:
                # struggle_till_message()
                ai_handler.update_context()
        
        if time_passed < 0.1:
            delay_time = 1
        elif time_passed < 2:
            delay_time = 30
        else:
            delay_time = 5 * 60
        
        

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
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())        
            
        msgs.append(
            {
                "role": "model",
                "content": f"Below is the detailed instruction, formulated on {task['date created']}: [instruction] {task['content']}"
            }
        )
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))    
        struggle_till_message()
        bot.send_message(
            prefs.TST_chat_id,
            "`TASK complete`", parse_mode="Markdown"
        )   
    return found


