from .imports_for_tools import *

google_send_private_message_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="send_private_message",
            description="Send a direct message to a specific user. Use this tool when asked to message someone privately. Use to continue a personal conversation."
            """
[user id for users]
Steklish(SKLS) - Антон [1911742158]
Andrew/Geroundiy [1464191308],
Santa/Zawarkich  [5718185452],
Appolonir - [1895097067],
Dr.DZE  [822091135],
Cyclodor [1887803023] 
DedPogran [978523669] 
IWTDPLZZZ [622933104]
""",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "message": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "user_id": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                },
                required=["message", "user_id"],
            ),
        ),
    ]
)
    
def send_private_message(user_id: str, message: str):
    print("tryna send DM")
    print(f"{MAGENTA}[Private to {user_id}/{bot.get_chat(int(user_id)).username}]: {message}{RESET}")
    # print(fix_markdown_v2(message))
    try:
        bot.send_message(
            int(user_id),  # Send to the specified user ID
            fix_markdown_v2(message),
            parse_mode="Markdown"
        )
    
        return "send successfully"
    except Exception as e:
        print(e)
        bot.send_message(
            prefs.TST_chat_id,
            f"🔴\n```Cannot_send_private_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )
        return "Error sending message"