import base64
import os
from google import genai
from google.genai import types

import mimetypes
import mammoth
from bot_instance import client_google as client
from stuff import *
import prefs
import datetime
import json
import conf_info
import telebot
from bot_instance import bot
import google.genai as genai
import base64
from PIL import Image
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def convert_docx_to_html(docx_path):
    with open("tmp/" + docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value
    # return pypandoc.convert_file("tmp/" + docx_path, 'html')

#!text docs only
def extract_doc(url:str, file_path, message:telebot.types.Message=None):
    file_path = file_path.split("/")[-1]
    os.makedirs("tmp", exist_ok=True)
    download_file(url,"tmp/" + file_path)
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg()
    }
    
    
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())
                
    if message and bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    if is_readable_text(file_path="tmp/" + file_path):
        with open("tmp/" + file_path, 'r') as f:
            file = f.read()
    else:
        if message is None:
            msg = {
                "role": "model",
                "content": json.dumps({
                    "message": "[file] *Unreadable file format*" + file_path,
                    "from" : "Magg's request"
                }, indent=4, ensure_ascii=False)
            }
        else:
            msg = {
                "role": "user",
                "content": json.dumps({
                    "sender": f"{message.from_user.full_name} / {message.from_user.username} - [{message.from_user.id}]",
                    "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                    "from" : origin,
                    "message": "[file] *Unreadable file format*" + "[file name]" + str(message.document.file_name) + f"{'[caption]' + message.caption if message.caption else "."}"
                }, indent=4, ensure_ascii=False)
            }
        msgs.append(msg)
        if len(msgs)  >prefs.history_depth:
            msgs = msgs[10:]
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        print("Done with the doc")
        delete_files_in_directory("tmp")
        return "completed successfully"
    
    if file:
        if message:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    json.dumps(sys_m),
                    'Describe what is inside the file. To do it use language of the document. Provide a detailed summary and dont miss important or interesting details. Take a message history into account when making conclusion' + "[file name]" + str(message.document.file_name) + f"{'[caption]' + message.caption if message.caption else "."}",
                    file,
                ]
            )
        else:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    json.dumps(sys_m),
                    "Describe what is inside the file. To do it use language of the document. Provide a detailed summary and dont miss important or interesting details. Take a message history into account when making conclusion [file name]" + file_path,
                    file,
                ]
            )
        if message is None:
            return response.text
        else:
            msg = {
                "role": "user",
                "content": json.dumps({
                    "sender": f"{message.from_user.full_name} / {message.from_user.username} - [{message.from_user.id}]",
                    "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                    "from" : origin,
                    "message": "[file] " + response.text + "[file name]" + str(message.document.file_name) + f"{'[caption]' + message.caption if message.caption else "."}"
                }, indent=4, ensure_ascii=False)
            }
                
        msgs.append(msg)
        if len(msgs)  >prefs.history_depth:
            msgs = msgs[10:]
        with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(msgs, indent=4, ensure_ascii=False))

    print("Done with the doc")
    delete_files_in_directory("tmp")


#!image
def extract_img(url:str, file_path, message:telebot.types.Message=None, magg_caption:str=None):
    print(MAGENTA, "starting img processing", RESET)
    file_path = file_path.split("/")[-1]
    os.makedirs("tmp", exist_ok=True)
    download_file(url,"tmp/" + file_path)
    with open("tmp/" + file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg()
    }
    
    message_text = None
    
    if message and message.caption:
        message_text = message.caption
    mime_type = mimetypes.guess_type("tmp/" + file_path)[0] or 'image/jpeg'
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(
                        mime_type=mime_type,
                        data=base64.b64decode(
                        encoded_string
                        ),
                    ),
                    types.Part.from_text(text="""what is th photo? Make a brief analysis in russian.""" if magg_caption is None else magg_caption),
                ],
            ),
        ]
    )
    
    print(BLUE, "IMG ANALYSIS PROMPT" , ("Make a detailed description of the image. Describe what is inside the file. Extract every label on the photo. Use russian. \n[caption]" + str(message_text)) if magg_caption is None else str(magg_caption), RESET)
    
    print(MAGENTA, "received response from llm", RESET)
    print(YELLOW, response.text, RESET)
    #update context of conversation
    msgs = []
    if message and bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())
    if message is None:
        return response.text
    else:
        msg = {
            "role": "model",
            "content": json.dumps({
                "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                "message": "[brief analysis of the photo by magg] " + url + str(response.text)
            }, indent=4, ensure_ascii=False)
        }
    
    msgs.append(msg)
    
    
    if len(msgs)  >prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
   
    delete_files_in_directory("tmp")
    print("Done with the img")
    
    
#!voice
def extract_voice(url:str, file_path, message:telebot.types.Message=None):
    file_path = file_path.split("/")[-1]
    download_file(url, "tmp/" + file_path)
    file = client.files.upload(file='tmp/' + file_path)
    
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())
    
    
    
    
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg_char
    }
    sys_m = [sys_m, *msgs]
    
    should_delete = False
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            json.dumps(sys_m),
            'Extract text from audio. It is likely to be in Russian. Describe emotions and intonations of the speaker. Consider the conte of the conversation. Example "*Тон: игривый, слышен смех* «Ну что, как успехи с проектом?», mak full analysis of the audio"',
            file,
        ]
    )
    if message and bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    
    print(YELLOW, response, RESET)
    # Update context of conversation
    if message is None:
        return response.text
    else:
        msg = {
            "role": "user",
            "content": json.dumps({
                "sender": f"{message.from_user.full_name} / {message.from_user.username} - [{message.from_user.id}]",
                "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                "from" : origin,
                "message": f"[voice message] " + response.text,
                "from" : origin
            }, indent=4, ensure_ascii=False)
        }
    msgs.append(msg)
    if len(msgs) >prefs.history_depth:
        msgs = msgs[10:]
    
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
    
    # Delete the file
    for file_google in client.files.list():
        client.files.delete(name=file_google.name)
        print("file deleted")
            
    delete_files_in_directory("tmp")
    print("Done with the voice")
    
#!sticker
def extract_sticker(message: telebot.types.Message):
    
    msgs = []
    if message and bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())

    msg = {
        "role": "user",
        "content": json.dumps({
            "sender": f"{message.from_user.full_name} / {message.from_user.username} - [{message.from_user.id}]",
            "from" : origin,
            "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            "message": "[sticker] " + str(message.sticker.emoji) + "[sticker id]" + str(message.sticker.file_id)
        }, indent=4, ensure_ascii=False)
    }
    
    msgs.append(msg)
    if len(msgs)  >prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))

    
def media_handler(url: str, magg_prompt=None):
    # Extract filename from url

    # Check if the URL is a web page
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme in ['http', 'https'] and not any(url.endswith(ext) for ext in ['.txt', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.ogg', '.mp3', '.wav']):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content from the webpage
            text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
            return client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                "Summarize this webpage content: ",
                text[:8000]  # Limit text length to avoid token limits
            ]
            ).text
    except Exception as e:
        print(f"Error processing webpage: {e}")
        # Continue with file processing if webpage handling fails
    
    file_path = url.split('/')[-1]
    # Get file extension from the URL
    file_extension = file_path.split('.')[-1].lower()

    # Handle different file types
    if file_extension in ['txt', 'doc', 'docx']:
        return extract_doc(url, file_path)
    elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return extract_img(url, file_path, magg_caption=magg_prompt)
    elif file_extension in ['ogg', 'mp3', 'wav']:
        return extract_voice(url, file_path)
    else:
        return extract_doc(url, file_path)
