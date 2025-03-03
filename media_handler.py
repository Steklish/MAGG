import mammoth
from ai_handler import client as OR_client
from ai_handler import client_google as client
from stuff import *
import prefs
import datetime
import json

def convert_docx_to_html(docx_path):
    with open("tmp/" + docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value
    # return pypandoc.convert_file("tmp/" + docx_path, 'html')

#!text docs only
def extract_doc(url:str, message, file_path):
    file_path = file_path.split("/")[-1]
    os.makedirs("tmp", exist_ok=True)
    download_file(url,"tmp/" + file_path)
    sys_m = {
        'role': 'system',
        'content': prefs.system_msg
    }
    if is_readable_text(file_path="tmp/" + file_path):
        with open("tmp/" + file_path, 'r') as f:
            file = f.read()
    if file:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                json.dumps(sys_m),
                'Describe what is inside the file. To do it use language of the document. Provide a detailed summary and dont miss importtant or interesting detailes. Take a message history into account when making conclusion',
                file,
            ]
        )

        #update context of conversation
        msgs = []
        with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
            msgs = json.loads(f.read())        
        msg = {
            "role": "user",
            "content": json.dumps({
                "sender": {
                    "name": message.from_user.full_name,
                    "username": message.from_user.username
                },
                "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                "message": response.text
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
                'Make a detailed description of the image. Describe what is inside the file. Extract every label on the photo. Use russian',
                file,
                "\nsender subscription: " + normalize_string(message_text),
            ]
        )
    #update context of conversation
    msgs = []
    with open("static_storage/conversation.json", "r", encoding="utf-8") as f:
        msgs = json.loads(f.read())
    
    msg = {
        "role": "user",
        "content": json.dumps({
            "sender": {
                "name": message.from_user.full_name,
                "username": message.from_user.username
            },
            "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            "message(assistant analysys)": normalize_string(response.text)
        }, indent=4, ensure_ascii=False)
    }
    
    msgs.append(msg)
    
    
    if message.caption:
        message_text = message.caption
    
        bonus_mwssage = msg = {
            "role": "user",
            "content": json.dumps({
                "sender": {
                    "name": message.from_user.full_name,
                    "username": message.from_user.username
                },
                "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
                "message": normalize_string(message_text)
            }, indent=4, ensure_ascii=False)
        }

        
        msgs.append(bonus_mwssage)
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
        'content': prefs.system_msg
    }
    sys_m = [sys_m, *msgs]
    
    should_delete = False
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            json.dumps(sys_m),
            'Extract text from audio. It is likely to be Russian. Also describe emotions and intonations of the speaker in Russsian. Think about the context (it can improve spelling recognition) of the conversation',
            file,
        ]
    )
    
    print(YELLOW + response.text + RESET)
    # Update context of conversation
    msg = {
        "role": "user",
        "content": json.dumps({
            "sender": {
                "name": message.from_user.full_name,
                "username": message.from_user.username
            },
            "date": datetime.datetime.fromtimestamp(message.date, prefs.timezone).strftime('%d-%m-%Y %H:%M:%S %Z'),
            "extra" : "voice message from user (user sent a voice message), so description provided not a real text",
            "message": normalize_string(response.text)
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
    
   