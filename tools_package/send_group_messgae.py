from .imports_for_tools import *

send_group_message_tool = {
    "type": "function",
    "function": {
        "name": "send_group_message",
        "description": (
            "Send a message to a group chat. Use this tool to respond to group discussions, address the entire group, or share information with multiple people. "
            "Be engaging! Share memes, ask questions, or bring up fun topics to keep the chat active. "
            "Always use this tool if the conversation is public or if you're initiating a group discussion."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text to send to the chat. Include emojis, slang, or references to keep it lively."
                }
            },
            "required": ["message"]
        }
    }
}

def send_group_message(message):
    print(GREEN, "Decided to answer (send_group_message)", RESET)
    send_to_chat(message)
    return "send"
