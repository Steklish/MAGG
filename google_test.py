# AIzaSyCbPw-Rw2hx1SHLsIsdRedl0YBQvufc5ds
from stuff import *
import os
from google import genai
from google.genai import types


tools_g = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="getWeather",
                    description="gets the weather for a requested city",
                    parameters=genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        properties = {
                            "city": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
            ])
    ]

def generate():
    client = genai.Client(
        api_key="AIzaSyCbPw-Rw2hx1SHLsIsdRedl0YBQvufc5ds",
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""hi
"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Hi there! How can I help you today?
"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                # types.Part.from_text(text="""what is the weather in NYC and in london"""),
                types.Part.from_text(text="""hi"""),
            ],
        ),
    ]
    tools = tools_g
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""system_message"""),
        ],
    )


    plain_text = ""
    function_calls = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk)
        print()
        if not chunk.function_calls:
            plain_text += chunk.text
        else:
            for call in chunk.function_calls:
                function_calls.append(call.function_name)
                
                
    print(GREEN)
    print(plain_text, function_calls)
    print(RESET)
    
    

if __name__ == "__main__":
    generate()
