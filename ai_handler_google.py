import time

import portalocker
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
        portalocker.lock(f, portalocker.LOCK_EX)
        conversation = json.load(f)
        portalocker.unlock(f)
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
        portalocker.lock(f, portalocker.LOCK_EX)
        conversation = json.load(f)
        portalocker.unlock(f)
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
            system_message = types.Part.from_text(text=f"Current time is {current_datetime} {prefs.system_msg() or ''}")   
            
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
            max_output_tokens=12000,
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
        function_calls = []
        response = client.models.generate_content_stream(
            model=prefs.model_gemini,
            contents=messages,
            config=generate_content_config,
        )
        for chunk in response:
            if chunk.function_calls is not None:
                
                # print(YELLOW, chunk, RESET)
                # print()
                for call in chunk.function_calls:
                    
                    if call is None:
                        print("The call is none")
                        continue
                    function_calls.append(call.name)
                    # Start the timer
                    start_time = time.time()

                    # Call the function
                    result = tools.execute_tool(call.name, call.args)
                    # End the timer
                    end_time = time.time()

                    # Calculate the elapsed time in seconds
                    execution_time = end_time - start_time 
                    if call.name != "send_message":
                        log_message_with_sender(result, f"function{call.name} ({call.args})", "MAGG")
                    raw_messages = raw_conversation()
                    raw_messages.append(
                        {                        
                            "role":"model",
                            "content" : f"The result of calling the {call.name} function with parameters ({call.args}) was: {result}.  [additional info] execution time {execution_time} s. "
                        }
                    )
                    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
                        portalocker.lock(f, portalocker.LOCK_EX)
                        f.write(json.dumps(raw_messages, indent=4, ensure_ascii=False))
                        portalocker.unlock(f)
                    if len(raw_messages) > prefs.history_depth:
                        raw_messages = raw_messages[prefs.history_depth // 4:]
                    print("new function call (appended)")

        print(YELLOW, function_calls, RESET)
        return function_calls
    except Exception as e:
        print(RED, "from smart response", RESET)
        print(RED, e, RESET)
        
    
    
    
def update_context():
    try:
        print("starting context updating")
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%D-%M-%Y %H:%M:%S %Z')
        
        
            
        system_message = types.Part.from_text(text=f"Current time is {current_datetime} {prefs.system_msg() or ''}")   
        
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
    описание текущих событий.
    Свои чувства и желания, настроение.
    Свои цели и намерения, прогресс в их достижении.
    Опиши, какая информация нудна для продолжения беседы и имеется ли она у тебя. Это для дальнейшего запроса на получение.
    Сохраняй важную системную информацию.
    
Обновляй, основываясь на истории действий. Раздели долгосрочный контекст и текущую информацию. Для давних действий уменьшай детализацию описания, а со временем - удаляй. Нужно не ответить на сообщение, нужно только обновить контекст. Следи за временем и иногда добавляй временные пометки к записям. Группируй записи по времени. Долгосрочный контекст меняй реже, чем текущий. Текущий контекст меняй чаще. Помечай данные, которые нельзя заменять и помечай, при каком условии можно обновить записи. Сохраняй важные ссылки, url's и ключевые слова или события. Сохраняй ссылки.

[история последних действий]
{conversation[len(conversation) // 5:]}
            """),
            ],
        )
        
        generate_content_config = types.GenerateContentConfig(
            temperature=prefs.TEMPERATURE,
            top_p=0.9,
            top_k=50,
            max_output_tokens=8000,
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
                plain_text += str(chunk.text)
           
        with open("static_storage/context.txt", "w", encoding="utf-8") as f:
            f.write(plain_text)

        print("context updated")
    except Exception as e:
        print(RED, e , RESET)
        error_msg = f"Context_failure {str(e)}"
        bot.send_message(prefs.TST_chat_id, f"🔴\n```{error_msg}```", parse_mode="Markdown")
        return 1



def summarize_file(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        system_message = types.Part.from_text(text=f"[character] {prefs.system_msg_char} [context] {prefs.get_context()}")
        query = types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"Summarize todays message history, store meaningful names, statements, important urls etc [message and function logs]\n{content}"),
            ],
        )

        generate_content_config = types.GenerateContentConfig(
            temperature=0.3,
            top_p=0.9,
            top_k=40,
            max_output_tokens=1000,
            response_mime_type="text/plain",
            system_instruction=[system_message]
        )

        summary = ""
        for chunk in client.models.generate_content_stream(
            model=prefs.model_gemini,
            contents=[query],
            config=generate_content_config,
        ):
            if not chunk.function_calls:
                summary += str(chunk.text)

        timestamp = (datetime.datetime.now(prefs.timezone) - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S %Z')
        memory_entry = {
            "date created": timestamp,
            "content": summary
        }

        try:
            with open("static_storage/long_term_memory.json", "r", encoding="utf-8") as f:
                portalocker.lock(f, portalocker.LOCK_EX)
                memories = json.load(f)
                portalocker.unlock(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        memories.append(memory_entry)
        with open("static_storage/long_term_memory.json", "w", encoding="utf-8") as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            json.dump(memories, f, indent=4, ensure_ascii=False)
            portalocker.unlock(f)

        return summary
    except Exception as e:
        print(RED, f"Summarization error: {e}", RESET)
        return None