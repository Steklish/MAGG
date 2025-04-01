from .imports_for_tools import *
import datetime
import json



google_long_term_memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_long_term_memory",
            description=(
                "Periodically retrieve the context of the conversation. "
                "Use this tool to recall shared experiences, historical context, names, dates, or "
                "specific events. This tool is essential for understanding references, emotional "
                "context, and maintaining continuity in conversations."
                "use to recall events that took part in past in certain date"
                "use dd-mm-YYYY format or parts of it if needed to search by date"
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "keywords": genai.types.Schema(
                        type=genai.types.Type.ARRAY,
                        items=genai.types.Schema(type=genai.types.Type.STRING),
                        description="2-3 varied search terms. Example: ['Alex', 'birthday', '15-08']",
                    ),
                },
                required=["keywords"],
            ),
        ),
    ]
)



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
        
        
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%D-%M-%Y %H:%M:%S %Z')
            
        system_message = types.Part.from_text(text=f"Current time is {current_datetime} {prefs.system_msg()}")   
        
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
        
        query = types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=f"""
Исходя из истории переписки и данных записей из базы данных выдели данные, которые имеют отношение к контексту, остальное опусти. Эти данные из твоей памяти. Приведи их в удобный формат. Подведи итог. Обращай внимание на даты создания записей в базе данных. Представь результат в виде сводки. Отрази свое отношение но не используй прямую речь. Сгруппируй по датам. Если находятся записи которые не относятся к контексту напрямую, но могут помочь в развитии беседы, проанализируй их тоже.

[история действий и сообщений]
{conversation[len(conversation) // 2:]}

[записи из базы данных]
{filtered_memories}
            """),
            ],
        )
        
        generate_content_config = types.GenerateContentConfig(
            temperature=prefs.TEMPERATURE,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
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
        
        
        return plain_text
