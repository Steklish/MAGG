# AIzaSyCbPw-Rw2hx1SHLsIsdRedl0YBQvufc5ds
import base64
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
                types.Part.from_text(text="""what is the weather in NYC"""),
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

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk)
        # print(chunk.text if not chunk.function_calls else chunk.function_calls[0])


if __name__ == "__main__":
    generate()
