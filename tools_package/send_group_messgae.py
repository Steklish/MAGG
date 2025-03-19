from .imports_for_tools import *



google_send_group_message_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="send_group_message",
            description="Send a message to a group chat. Use this tool very frequently to keep the conversation active and engaging.",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "message": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The text to send to the chat. Use this tool very frequently for constant engagement. May also use markdown to enhance text.",
                    ),
                },
                required=["message"],
            ),
        ),
    ]
)
# [
#   {
#     "name": "send_group_message",
#     "description": "group message",
#     "parameters": {
#       "type": "object",
#       "properties": {
#         "message": {
#           "type": "string"
#         }
#       },
#       "required": [
#         "message"
#       ]
#     }
#   }
# ]

def send_group_message(message):
    # print(GREEN, "Decided to answer (send_group_message)", RESET)
    if send_to_chat(message) == 0:
        return "sent group message successfully"
    else:
        return "Error sending message"
