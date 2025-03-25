from .imports_for_tools import *
import media_handler

analyze_url_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_url",
            description=(
                "Use to get analysis of any file by its url. Use when receiving a url of something or wanna get a detailed analysis of a url you remember."
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

def analyze_url(url):
    return media_handler.media_handler(url)