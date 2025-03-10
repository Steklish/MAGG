import mammoth
from ai_handler import client as OR_client
from ai_handler import client_google as client
from stuff import *
import prefs
import datetime
import json
import conf_info
import telebot
from bot_instance import bot

def convert_docx_to_html(docx_path):
    with open("tmp/" + docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value
    # return pypandoc.convert_file("tmp/" + docx_path, 'html')

#!text docs only
def extract_doc(url:str, message:telebot.types.Message, file_path):
    file_path = file_path.split("/")[-1]
    os.makedirs("tmp", exist_ok=True)
    download_file(url,"tmp/" + file_path)
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg
    }
    
    
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())        
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    if is_readable_text(file_path="tmp/" + file_path):
        with open("tmp/" + file_path, 'r') as f:
            file = f.read()
    else:
        msg = {
            "role": "user",
            "content": json.dumps({
                "sender": {
                    "name": message.from_user.full_name,
                    "username": message.from_user.username
                },
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
        return 0
    
    if file:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                json.dumps(sys_m),
                'Describe what is inside the file. To do it use language of the document. Provide a detailed summary and dont miss importtant or interesting detailes. Take a message history into account when making conclusion' + "[file name]" + str(message.document.file_name) + f"{'[caption]' + message.caption if message.caption else "."}",
                file,
            ]
        )

        msg = {
            "role": "user",
            "content": json.dumps({
                "sender": {
                    "name": message.from_user.full_name,
                    "username": message.from_user.username
                },
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
def extract_img(url:str, message, file_path):
    file_path = file_path.split("/")[-1]
    os.makedirs("tmp", exist_ok=True)
    download_file(url,"tmp/" + file_path)
    file = client.files.upload(file='tmp/'+file_path)
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg
    }
    
    message_text = "no subscription"
    
    if message.caption:
        message_text = message.caption
    
    should_delete = False
    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                json.dumps(sys_m),
                "Make a detailed description of the image. Describe what is inside the file. Extract every label on the photo. Use russian. \n[caption]" + message_text,
                file,
            ]
        )
    #update context of conversation
    msgs = []
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())
    
    # if message.caption:
    #     msgs[-1]["content"]["message"] +=  "\n[caption] "
    #     msgs[-1]["content"]["message"] +=  message.caption
    msg = {
        "role": "user",
        "content": json.dumps({
            "sender": {
                "name": message.from_user.full_name,
                "username": message.from_user.username
            },
            "from" : origin,
            "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            "message": "[photo] " + response.text + f"{'[caption]' + message.caption if message.caption else "."}"
        }, indent=4, ensure_ascii=False)
    }
    
    msgs.append(msg)
    
    
    if len(msgs)  >prefs.history_depth:
        msgs = msgs[10:]
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
        
    # Delete the file
    # if should_delete:
    #     client.files.delete(file_id=file.id)
    for file_google in client.files.list():
        client.files.delete(name=file_google.name)
        print("file deleted")
            
    delete_files_in_directory("tmp")
    print("Done with the img")
    
    
#!voice
def extract_voice(url: str, message, file_path):
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
            'Extract text from audio. It is likely to be in Russian. Describe emotions and intonations of the speaker. Consider the contet of the conversation. Example "*Тон: игривый, слышен смех* «Ну что, как успехи с проектом?»"',
            file,
        ]
    )
    if bot.get_chat(message.chat.id).type == "private":
        origin = "direct message"
    else:
        origin = "group"
    
    print(YELLOW, response, RESET)
    # Update context of conversation
    msg = {
        "role": "user",
        "content": json.dumps({
            "sender": {
                "name": message.from_user.full_name,
                "username": message.from_user.username
            },
            "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            "from" : origin,
            "message": f"[voice message] " + response.text,
            "from" : origin
        }, indent=4, ensure_ascii=False)
    }
    print(BACKGROUND_RED + BLACK + "context updated" + RESET)
    msgs.append(msg)
    if len(msgs) >prefs.history_depth:
        msgs = msgs[10:]
    
    with open("static_storage/conversation.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(msgs, indent=4, ensure_ascii=False))
    
    # Delete the file
    if should_delete:
        client.files.delete(file_id=file.id)
    delete_files_in_directory("tmp")
    print("Done with the voice")
    
   