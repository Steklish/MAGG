from .imports_for_tools import *
import media_handler

analize_url_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analize_url",
            description=(
                "Use to get alalysys of any file by its url."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "url": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The URL of the file",
                    ),
                },
                required=["url"],
            ),
        ),
    ]
)

def analize_url(url):
    return media_handler.media_handler(url)