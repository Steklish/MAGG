from .imports_for_tools import *
from daily_memory import log_message_with_sender

google_send_message_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="send_message",
            description="Use to send any message to a user. Use every time you need to send anything to a user. Use also to provide users with information they need. Usage of this tool has the highest priority. Use to send links and url's"
            f"""
[users id]
Steklish(SKLS) - Антон [1911742158]
Andrew/Geroundiy [1464191308],
Santa/Zawarkich  [5718185452],
Appolonir - [1895097067],
Dr.DZE  [822091135],
Cyclodor [1887803023] 
DedPogran [978523669] 
IWTDPLZZZ [622933104]
group chat id - [{prefs.chat_to_interact}]
""",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "message": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description=(
                            "The message you wanna send to a user.May include URL's, src code, formatted text and anything you need to send"
                        ),
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
    
def extract_integer(text):
    # This regex matches both positive and negative integers
    match = re.search(r'-?\d+', text)
    if match:
        return int(match.group())
    else:
        return prefs.chat_to_interact  # or raise an error if no match is found

    
def send_message(chat_to_send_id: str, message: str):
    log_message_with_sender(message, "SEND", "MAGG")
    # print(fix_markdown_v2(message))
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    print(MAGENTA, f"urls: {urls}", RESET)
    # Send each URL as a separate document
    for url in urls:
        message_pre = message.split(url)[0]
        message_post = message.split(url)[1]
        
        message_pre.replace(url, '').strip()
        message_post.replace(url, '').strip()
        
        if message_pre.replace("\n", " ").strip():
            bot.send_message(
                extract_integer(chat_to_send_id),  # Send to the specified user ID
                fix_markdown_v2(message),
                parse_mode="Markdown"
            )
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
                    bot.send_document(extract_integer(chat_to_send_id), f)
                # Clean up
                os.remove(filename)
                # Handle regular image URLs
            elif any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                bot.send_photo(extract_integer(chat_to_send_id), url)
            else:
                bot.send_document(extract_integer(chat_to_send_id), url)
            message = message.replace(url, '').strip()
        except Exception as e:
            print(RED, f"URL EXCEPTION {str(e)}", RESET)
            continue
        message = message_post
    try:
        print(MAGENTA, f"message(no urls): {message}", RESET)
        if message.replace("\n", " ").strip():
            bot.send_message(
                extract_integer(chat_to_send_id),  # Send to the specified user ID
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