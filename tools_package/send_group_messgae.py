from .imports_for_tools import *



google_send_group_message_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="send_group_message",
            description="Use to send a message to a group chat. Always use when referenced in chat or if you need to participate in discussion. Use very frequently. Engage into conversations.",
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
def send_group_message(message):
    # print(GREEN, "Decided to answer (send_group_message)", RESET)
    if send_to_chat(message) == 0:
        return "sent group message successfully"
    else:
        return "Error sending message"
