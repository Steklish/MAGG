from .imports_for_tools import *

send_group_message_tool = {
    "type": "function",
    "function": {
        "name": "send_group_message",
        "description": "Send a message to a group chat. Use this tool very frequently to keep the conversation active and engaging.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The text to send to the chat. May include emojis, slang, or references to keep it lively. Use this tool very frequently for constant engagement. May also use markdown to enhance text"
                }
            },
            "required": ["message"]
        }
    }
}

def send_group_message(message):
    print(GREEN, "Decided to answer (send_group_message)", RESET)
    if send_to_chat(message) == 0:
        return "send"
    else:
        return "Error sending message"
