from .imports_for_tools import *

send_private_message_tool = {
    "type": "function",
    "function": {
        "name": "send_private_message",
        "description": (
            "Send a direct message to a specific user. Use this tool when asked to message someone privately or when discussing sensitive topics. Use to continue a personal convarsation."
            "Always respond to private messages."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The decimal user_id of the user to send the private message to. Should be on of the id's of the members from the list."
                    """
                        # [user id for users]
                        # Chelovek - Черный, Рома - ему писать не надо - он говно кушает,
                        # Steklish(SKLS) - Антон [1911742158] - он разработчик и создал тебя,
                        # Andrew/Geroundiy – Gay [1464191308],
                        # Santa/Zawarkich – Санта [5718185452],
                        # Appolonir – Руслан [1895097067],
                        # Dr.DZE – Алексей, Голова, Головко [822091135],
                        # Cyclodor – Александр, Саня [1887803023] - ты его очень любишь и флиртеушь с ним,
                        # DedPogran - Дед [978523669] - еме 19 но его называют так за его поведение,
                        # IWTDPLZZZ - Матвей [622933104] - скуф.
                        # """
                },
                "message": {
                    "type": "string",
                    "description": "The text to send to the user. Keep it personal and relevant to the context. You may use markdown in text."
                }
            },
            "required": ["user_id", "message"]
        }
    }
}

    
def send_private_message(user_id: str, message: str):
    messages = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        messages = json.loads(f.read())
    
    print(f"{MAGENTA}[Private to {user_id}/{bot.get_chat(int(user_id)).username}]: {message}{RESET}")
    print(fix_markdown_v2(message))
    try:
        bot.send_message(
            int(user_id),  # Send to the specified user ID
            fix_markdown_v2(message),
            parse_mode="Markdown"
        )
    
        return "send"
    except Exception as e:
        print(e)
        bot.send_message(
            prefs.TST_chat_id,
            f"🔴\n```Cannot_send_private_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )
        return "Error sending message"