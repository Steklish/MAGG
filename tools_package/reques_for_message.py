from .imports_for_tools import *

google_reques_for_message_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="reques_for_message",
            description=(
                "Use to launch additional interactoin cycle. Use if have not fullfilled user's request or your own goal."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={},
                required=[],
            ),
        ),
    ]
)
