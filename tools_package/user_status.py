from .imports_for_tools import *
import prefs

google_update_status_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="update_status",
            description=(
                "Use to append or update attitude to a user. Append oly with significant facts that should affect the way you behave towards the user. "
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "name": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The name of the user whose information needs to be updated.",
                    ),
                    "new_info": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="Updated attitude and status of the user..",
                    ),
                },
                required=["name", "new_info"],
            ),
        ),
    ]
)


def rewrite_attitude(new_info, old_info, user):
    try:
        
        print("starting attitude updating")
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            conversation = json.load(f)
        current_datetime = datetime.datetime.now(prefs.timezone).strftime('%D-%M-%Y %H:%M:%S %Z')    
        system_message = types.Part.from_text(text=prefs.system_msg_char)   
        query = types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=f"""
Обнови статус пользователя {user}. Этот текст будет использоваться для определения твоего отношения к пользователю. Поэтому добавляй те факты, которые могут повлиять на то, как ты будешь с ним общаться. Также добавляй особо важные факты, показывающие характер и основные черты пользователя. Обнови старые данные с учетом контекста и новых данных.
[old info]
{old_info}
[new info]
{new_info}
[история последних действий]
{conversation[len(conversation):]}

тебе не нужно отвечать на сообщение, только предоставить обновленный статус.
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
        print("status updated")
        return plain_text
    
    except Exception as e:
        print(RED, e , RESET)
        error_msg = f"STATUS_FAILURE {str(e )}"
        bot.send_message(prefs.TST_chat_id, f"🔴\n```{error_msg}```", parse_mode="Markdown")
        return error_msg





def update_status(name, new_info):
    data = prefs.members_info()
    data = json.loads(data)
    for index, member in enumerate(data):
        # Check if the name or any alias matches
        if member["name"] == name or name in member.get("aliases", []):
            
            final_upd = rewrite_attitude(new_info, member["attitude"], member["name"])
            if final_upd != 1 and final_upd != "":
                member["attitude"] = final_upd
                
            print(MAGENTA, f"COMPILED STATUS {final_upd}", RESET)
            with open("static_storage/user_status.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=4))
            bot.send_message(
                prefs.TST_chat_id,
                "🟡\n```STATUS_UPD \n status update for <" + name + ">\n [" + final_upd + "] ```", parse_mode="Markdown"
            )
            return "Update complete"
    return "Error - cant find user"
