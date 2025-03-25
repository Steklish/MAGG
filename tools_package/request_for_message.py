from .imports_for_tools import *

google_request_for_message_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="request_for_message",
            description=(
                "Use to launch additional interaction cycle. Use if one message is not enough to achieve your goal"
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "dummy_property": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="A dummy property to satisfy the schema requirements."
                    )
                },
                required=[],
            ),
        ),
    ]
)

def request_for_message():
    return "Message request accepted now launch another interaction cycle"