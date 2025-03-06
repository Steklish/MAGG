import prefs
import datetime
from stuff import *
import json
from bot_instance import *
import tools_package.tools as tools

def smart_response(TOOLSET=tools.TOOLS, tool_choice="auto", TEMP=prefs.TEMPERATURE):
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
            tool_choice=tool_choice,
            temperature=TEMP,
            frequency_penalty=-1.0
        )
        try:
            print(response)
            if response.choices[0].finish_reason == 'error':
                smart_response(TOOLSET)
                return
            print(BRIGHT_RED, response.choices[0].message.content, RESET)
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
                        # if result != 'send':
                        #     print(YELLOW, "Silence...", RESET)
                        if "get_long_term_memory" == func_name:
                            smart_response()
                except Exception as e:
                    error_msg = f"Tool {func_name} failed: {str(e)}"
                    bot.send_message(prefs.TST_chat_id, f"```{error_msg}```", parse_mode="Markdown")


    except Exception as e:
        error_msg = f"Critical failure: {str(e)}"
        bot.send_message(prefs.TST_chat_id, f"```{error_msg}```", parse_mode="Markdown")