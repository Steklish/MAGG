import prefs
import datetime
from stuff import *
import json
from bot_instance import *
import re
import tools_package.tools as tools

def reminder_check():
    
    date_pattern = r'\b(\d{2})-(\d{2})\b'
    
    # Read the existing memories
    try:
        with open('static_storage/long_term_memory.json', 'r', encoding="utf-8") as f:
            memories = json.load(f)
    except FileNotFoundError:
        memories = []
    to_remind = []
    old_memories = []
    for mem in memories:
        done = False
        
        # Get the current datef
        current_date = datetime.datetime.now()
        
        
        match = re.findall(date_pattern, mem["content"])
        if match:
            for day, month in match:
                matched_date = datetime.datetime(year=current_date.year, month=int(month), day=int(day))
                if matched_date.date() <= current_date.date():
                    done = True
                    break
        if mem["reminder"] and done:
            to_remind.append(mem)
        else:   #else place back
            old_memories.append(mem)
             
    if to_remind != []:
        bot.send_message(
                prefs.TST_chat_id,
                "`REMINER_USED`", parse_mode="Markdown"
            )
        # Write the updated memories back to the file
        with open('static_storage/long_term_memory.json', 'w', encoding="utf-8") as f:
            # PermissionError(memories)
            json.dump(old_memories, f, indent=4, ensure_ascii=False)
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())        
        msg = {
            'role' : 'user',
            'extra' : 'reminder time has come',
            'content' : json.dumps(to_remind, indent=4, ensure_ascii=False),
        }
        msgs.append(msg)
        if len(msgs)  > prefs.history_depth:
            msgs = msgs[10:]
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        tools.non_stop()
def smart_response():
    try:
        print(f"{GREEN}Smart message launched{RESET}")
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        system_message = {
            'role': 'system',
            'content': f"""Current time: {current_datetime}
            {prefs.system_msg}
            """
        }

        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)

        client.api_key = prefs.open_r_key()
        response = client.chat.completions.create(
            model=prefs.MODEL(),
            messages=[system_message, *conversation],
            tools=tools.TOOLS,
            tool_choice="auto",
            temperature=1.1
            # top_p=0.9
        )
        try:
            print(CYAN, response.choices[0].message.content, RESET)
        except Exception as e:
            pass
        
        if not response.choices:
            bot.send_message(
                prefs.TST_chat_id,
                f"```API Error: {response}```",
                parse_mode="Markdown"
            )
            return

        message = response.choices[0].message
        plain_text = message.content
        tool_calls = message.tool_calls

        
        result = None
        # Process tool calls
        if tool_calls:
            for call in tool_calls:
                func_name = call.function.name
                func_args = call.function.arguments
                
                try:
                    
                    #! Execute tool
                    
                    result = tools.execute_tool(func_name, func_args)
                    # Store tool result
                    if not("send" in func_name):
                        conversation.append(
                            {
                                "role": "assistant",
                                "tool_calls": [{
                                    'id' : str(call.id),
                                    "type" : str(call.type),
                                    "function":{
                                        "name" : str(func_name),
                                        "arguments" : str(func_args)
                                    }
                                    # "index" : str(call_index),
                                }]
                            }
                        )
                        conversation.append(
                            {
                                "role": "tool",
                                "name": func_name,
                                "tool_call_id": call.id,
                                "content": str(result),
                            }
                        )
                        # Save conversation state
                        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
                            json.dump(conversation, f, indent=4, ensure_ascii=False)
                        if "get_long_term_memory" == func_name:
                            smart_response()
                except Exception as e:
                    error_msg = f"Tool {func_name} failed: {str(e)}"
                    bot.send_message(prefs.TST_chat_id, f"```{error_msg}```", parse_mode="Markdown")

        if result != 'send':
            print(YELLOW, "Silence...", RESET)
        # if tool_calls:   
        #     smart_response()
        reminder_check()

    except Exception as e:
        error_msg = f"Critical failure: {str(e)}"
        bot.send_message(prefs.TST_chat_id, f"```{error_msg}```", parse_mode="Markdown")