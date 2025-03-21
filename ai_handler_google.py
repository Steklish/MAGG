import prefs
from bot_instance import client, bot
import datetime
from stuff import *
import json
from stuff import *
from google.genai import types
import tools_package.tools as tools


def convert_conversation():
    google_conversation = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        conversation = json.load(f)
    for turn in conversation:
        google_conversation.append(types.Content(
            role=turn["role"],
            parts=[
                types.Part.from_text(text=turn["content"]),
            ]
        ))
    return google_conversation


def convert_single(message:str):
    return types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=message),
            ]
        )


def convert_single_as_function(message:str):
    return types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=message),
            ]
        )
        

def raw_conversation():
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        conversation = json.load(f)
    return conversation



def smart_response(
    TOOLSET=tools.G_TOOLS, 
    TEMP=prefs.TEMPERATURE, 
    system_message:types.Part=None, 
    func_mode="AUTO",
    messages=None
):
    """
    Args:
        func_mode: The mode for function calling. Must be one of "ANY", "AUTO", or "NONE".
                    - "ANY": Forces the model to predict only function calls.
                    - "AUTO": Lets the model decide between function calls and text responses.
                    - "NONE": Disables function calling entirely.
                    Defaults to "AUTO".
"""
    
    try:
        print(f"{GREEN}Smart message launched{RESET}")
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%D-%M-%Y %H:%M:%S %Z')
        if not system_message:
            system_message = types.Part.from_text(text=f"Current time is {current_datetime} {prefs.system_msg()}")   
            
        print("sys message created")
        
        tool_config = types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode=func_mode,
                # allowed_function_names=["get_current_weather"],
            )
        )
        print("tool config created")
        
        generate_content_config = types.GenerateContentConfig(
            temperature=TEMP,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            tools=TOOLSET,
            response_mime_type="text/plain",
            system_instruction=[
                system_message
            ],
            tool_config=tool_config
        )
        print("config created")
        if messages is None:
            messages = convert_conversation()
            
            
        raw_messages = raw_conversation()
        print("messages loaded")
        
        plain_text = ""
        function_calls = []
        response = client.models.generate_content_stream(
            model=prefs.model_gemini,
            contents=messages,
            config=generate_content_config,
        )
        for chunk in response:
            if chunk.function_calls is not None:
                
                # print(YELLOW, chunk, RESET)
                # print(chunk.function_calls)
                # print()
                for call in chunk.function_calls:
                    
                    if call is None:
                        print("THe call is none")
                        continue
                    function_calls.append(call.name)
                    result = tools.execute_tool(call.name, call.args)   
                    raw_messages.append(
                        {                        
                            "role":"model",
                            "content" : f"The result of calling the {call.name} function with parameters ({call.args}) was: {result}."
                        }
                    )
                    if len(raw_messages) > prefs.history_depth:
                        raw_messages = raw_messages[prefs.history_depth // 4:]
                    print("new function call (appended)")

        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(raw_messages, indent=4, ensure_ascii=False))
        return function_calls
    except Exception as e:
        print(RED, e, RESET)
        
    
    
    
def update_context():
    try:
        print("starting context updating")
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%D-%M-%Y %H:%M:%S %Z')
        
        
            
        system_message = types.Part.from_text(text=f"Current time is {current_datetime} {prefs.system_msg()}")   
        
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
        
        query = types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=f"""
Используй контекст.
Обнови контекст немного.
В обновленном контексте должны быть:
    состояние текущей беседы и ее история.
    описание текущих событий, если они есть.
    примерные предположения о намерениях пользователей.
    Свои цели и намерения, прогресс в их достижении.
    Опиши свои желания.
    
Обновляй, основываясь на истории действий. Для давних действий уменьшай детализацию описания, а со временем - удалай. Нужно не ответить на сообщение а обновить контескт. Не добавляй ответ в конце. Не оставляй больше одногоостартового сообщения в контексте. Следи за временем и иногда добавляй временные помтки к записям. Группируй записи по времени.

[история действий]
{conversation[len(conversation) // 5:]}
            """),
            ],
        )
        
        generate_content_config = types.GenerateContentConfig(
            temperature=prefs.TEMPERATURE,
            top_p=0.9,
            top_k=40,
            max_output_tokens=10000,
            response_mime_type="text/plain",
            system_instruction=[
                system_message
            ],
        )
        plain_text = ""
        for chunk in client.models.generate_content_stream(
            model=prefs.model_gemini,
            contents=[query],
            config=generate_content_config,
        ):
            if not chunk.function_calls:
                plain_text += chunk.text
           
        with open("static_storage/context.txt", "w", encoding="utf-8") as f:
            f.write(plain_text)

        
        print("context updated")
    except Exception as e:
        print(RED, e , RESET)
        error_msg = f"Context_failure {str(e )}"
        bot.send_message(prefs.TST_chat_id, f"🔴\n```{error_msg}```", parse_mode="Markdown")
        return 1
    