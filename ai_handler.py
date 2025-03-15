import prefs
import datetime
from stuff import *
import json
from bot_instance import *
import tools_package.tools as tools

def smart_response(TOOLSET=tools.TOOLS, tool_choice="auto", 
                   TEMP=prefs.TEMPERATURE, messages=None, system_message=None):
    try:
        print(f"{GREEN}Smart message launched{RESET}")
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%H:%M:%S')
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
        if not system_message:
            system_message = {
                'role': 'system',
                'content': f"""Current time: {current_datetime}
                {prefs.system_msg()}
                """
            }
        if not messages:
            messages = [system_message, *conversation]
        client.api_key = prefs.open_r_key()
        
        print(f"{GREEN}Ready to send response{RESET}")
        response = client.chat.completions.create(
            model=prefs.MODEL(),
            messages=messages,
            # tools=tools.TOOLS,
            # tool_choice=tool_choice,
            # temperature=TEMP,
            # frequency_penalty=2
        )
        print(response)
        if response.choices[0].finish_reason == 'error':
            
            return "error"
        
        if not response.choices:
            bot.send_message(
                prefs.TST_chat_id,
                f"🔴\n```API Error: {response}```",
                parse_mode="Markdown"
            )
            return
        message = response.choices[0].message
        plain_text = message.content
        tool_calls = message.tool_calls
        tools_called = []
        if tool_calls:
            
            #  vars to return into a conversation
            call_request = []
            call_response = []
                
                
            for call in tool_calls:
                func_name = call.function.name
                tools_called.append(func_name)
                func_args = call.function.arguments

                this_call = {
                                'id' : str(call.id),
                                "type" : str(call.type),
                                "function":{
                                    "name" : str(func_name),
                                    "arguments" : str(func_args)
                                }
                            }
                call_request.append(this_call)
            
            for call in tool_calls:
                func_name = call.function.name
                func_args = call.function.arguments
                #! tool execution
                try:                                
                    result = tools.execute_tool(func_name, func_args)   
                    # save a function call only on success
                    tools_called.append(func_name)
                except Exception as e:
                    print(RED, e.with_traceback(), RESET)
                    error_msg = f"Tool {func_name} failed: {str(e.with_traceback())}"
                    bot.send_message(prefs.TST_chat_id, f"🟠\n```{error_msg}```", parse_mode="Markdown")
                    result = e
                
                call_response.append(
                    {
                        "role": "tool",
                        "name": func_name,
                        "tool_call_id": call.id,
                        "content": str(result),
                    }
                )
                
            conversation.append(call_request)
            conversation.append(*call_response)
            
            
                    
            with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
                json.dump(conversation, f, indent=4, ensure_ascii=False)
        
        #!a list with every tool name called in this turn
        return tools_called
    
    # error handling per whole response
    except Exception as e:
        print(RED, e.with_traceback(), RESET)
        error_msg = f"Critical failure: {str(e.with_traceback())}"
        bot.send_message(prefs.TST_chat_id, f"🔴\n```{error_msg}```", parse_mode="Markdown")
        return 1