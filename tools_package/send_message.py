from .imports_for_tools import *

google_send_message_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="send_message",
            description="Use to send a text message. Always use when need to send a message. If you need to answer to group chat use this function too and pass group id as a parameter. "
            f"""
[user id for users]
Steklish(SKLS) - Антон [1911742158]
Andrew/Geroundiy [1464191308],
Santa/Zawarkich  [5718185452],
Appolonir - [1895097067],
Dr.DZE  [822091135],
Cyclodor [1887803023] 
DedPogran [978523669] 
IWTDPLZZZ [622933104]
[group id]
group_id - [{prefs.chat_to_interact}]
""",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "message": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "chat_to_send_id": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                },
                required=["message", "chat_to_send_id"],
            ),
        ),
    ]
)
    
def send_message(chat_to_send_id: str, message: str):
    # print(fix_markdown_v2(message))
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    print(MAGENTA, f"urls: {urls}", RESET)
    # Send each URL as a separate document
    for url in urls:
        try:
            # Check if it's a Telegram link
            if 'telegram' in url:
                # Create tmp directory if it doesn't exist
                os.makedirs('./tmp', exist_ok=True)
                # Download file from Telegram link
                response = requests.get(url)
                filename = os.path.join('./tmp', url.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(response.content)
                # Send downloaded file
                with open(filename, 'rb') as f:
                    bot.send_document(int(chat_to_send_id), f)
                # Clean up
                os.remove(filename)
                # Handle regular image URLs
            elif any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                bot.send_photo(int(chat_to_send_id), url)
            else:
                bot.send_document(int(chat_to_send_id), url)
            message = message.replace(url, '').strip()
        except Exception as e:
            print(RED, f"URL EXCEPTION {str(e)}", RESET)
            continue
    try:
        print(MAGENTA, f"message(no urls): {message}", RESET)
        if message.replace("\n", " ").strip():
            bot.send_message(
                int(chat_to_send_id),  # Send to the specified user ID
                fix_markdown_v2(message),
                parse_mode="Markdown"
            )
    
        return "send successfully"
    except Exception as e:
        print(e)
        
        bot.send_message(
            prefs.TST_chat_id,
            f"🔴\n```Cannot_send_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )
        return "Error sending message"