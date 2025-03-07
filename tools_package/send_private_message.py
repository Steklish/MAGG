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
                    "description": "The ID of the user to send the private message to."
                },
                "message": {
                    "type": "string",
                    "description": "The text to send to the user. Keep it personal and relevant to the context."
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
    
    # Print the message (for debugging/logging purposes)
    print(f"{MAGENTA}[Private to {user_id}/{bot.get_chat(int(user_id)).username}]: {message}{RESET}")
    
    # Add the message to the conversation history with a special mark
    messages.append(
        {
            'role': 'assistant',
            'content': message,
            'to':f"[direct message to {user_id}/{bot.get_chat(int(user_id)).username}]"
        }
    )
    
    # Send the private message
    try:
        bot.send_message(
            int(user_id),  # Send to the specified user ID
            normalize_string(message),
            parse_mode="Markdown"
        )
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(messages, indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        bot.send_message(
            prefs.TST_chat_id,
            f"```Cannot_send_private_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )