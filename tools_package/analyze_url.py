from .imports_for_tools import *
import media_handler

url_analysis_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_url",
            description=(
                "Analyzes the content at a given URL. Use this when you receive a URL "
                "or need detailed analysis of a remembered URL. The tool can examine "
                "various types of online content including documents, images, and web pages."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "url": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The URL of the resource to be analyzed",
                    ),
                    "analysis_prompt": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="Specific instructions for what to analyze about the URL content. "
                                    "Defines the scope and focus of the analysis.",
                    ),
                },
                required=["url"],
            ),
        ),
    ]
)

def analyze_url(url, analysis_prompt=None):
    """
    Analyzes the content at the specified URL according to the given prompt.
    
    Args:
        url (str): The URL of the resource to analyze
        analysis_prompt (str, optional): Specific instructions for the analysis. 
            Defines what aspects of the content to focus on.
            
    Returns:
        The analysis result from the media_handler
    """
    return media_handler.media_handler(url, magg_prompt=analysis_prompt)