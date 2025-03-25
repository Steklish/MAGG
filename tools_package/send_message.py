from .imports_for_tools import *

google_send_message_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="send_message",
            description="Use to send a text message. Always use when need to send a message. If you need to answer to group chat use this function too and pass group id as a parameter. "
            f"""
[user id for users]
Steklish(SKLS) - Антон [1911742158]
Andrew/Geroundiy [1464191308],
Santa/Zawarkich  [5718185452],
Appolonir - [1895097067],
Dr.DZE  [822091135],
Cyclodor [1887803023] 
DedPogran [978523669] 
IWTDPLZZZ [622933104]
[group id]
group_id - [{prefs.chat_to_interact}]
""",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "message": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "chat_to_send_id": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                },
                required=["message", "chat_to_send_id"],
            ),
        ),
    ]
)
    
def send_message(chat_to_send_id: str, message: str):
    # print(fix_markdown_v2(message))
    try:
        bot.send_message(
            int(chat_to_send_id),  # Send to the specified user ID
            message,
            # parse_mode="Markdown"
        )
    
        return "send successfully"
    except Exception as e:
        print(e)
        
        bot.send_message(
            prefs.TST_chat_id,
            f"🔴\n```Cannot_send_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )
        return "Error sending message"