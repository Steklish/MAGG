from .imports_for_tools import *

send_group_message_tool = {
    "type": "function",
    "function": {
        "name": "send_group_message",
        "description": "Send a message to a group chat. Use this tool to respond to group discussions, address the entire group, or share information with multiple people. Always use if were asked to.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                "type": "string",
                "description": "The text to send to the chat (may include references, src codes, urls etc)"
                },    
            }   
        },
        "required": ["message"],
    }
}

def send_group_message(message):
    print(GREEN, "Decided to answer (send_group_message)", RESET)
    send_to_chat(message)
    return "send"
