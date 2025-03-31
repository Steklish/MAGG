import datetime
import json
import requests
import os
import chardet

import prefs

def delete_files_in_directory(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Loop through all files in the directory

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            # Check if it's a file and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    else:
        print(f"Directory {directory_path} does not exist.")

def is_readable_text(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        
    # Detect encoding
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    
    if encoding:
        try:
            decoded_data = raw_data.decode(encoding)
            # Check if the decoded data contains readable text
            return True
        except (UnicodeDecodeError, TypeError):
            return False
    else:
        return False

    
def download_file(url, dest_path):
    response = requests.get(url)
    with open(dest_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded file {GREEN}saved{RESET} to: {dest_path}")

def file_to_bits(filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
    return file_data


def normalize_string(broken_string):
    encodings = ['utf-8', 'windows-1251', 'koi8-r', 'iso-8859-5', 'latin-1']
    
    for encoding in encodings:
        try:
            # Try decoding with different encodings
            decoded_string = broken_string.encode().decode(encoding)
            return decoded_string
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    
    try:
        # If still not properly decoded, try unicode escape
        return broken_string.encode().decode('unicode_escape')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # If all fails, return original
    return broken_string



# Basic Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Bright Colors
BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'

# Background Colors
BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m'
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_MAGENTA = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_WHITE = '\033[47m'

# Bright Background Colors
BACKGROUND_BRIGHT_BLACK = '\033[100m'
BACKGROUND_BRIGHT_RED = '\033[101m'
BACKGROUND_BRIGHT_GREEN = '\033[102m'
BACKGROUND_BRIGHT_YELLOW = '\033[103m'
BACKGROUND_BRIGHT_BLUE = '\033[104m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
BACKGROUND_BRIGHT_CYAN = '\033[106m'
BACKGROUND_BRIGHT_WHITE = '\033[107m'

# Reset
RESET = '\033[0m'



def log_message_with_sender(message:str, direction, sender=None):
    today = datetime.datetime.now(prefs.timezone).strftime('%Y-%m-%d')
    log_file = f'logs/{today}.txt'
    
    timestamp = datetime.datetime.now(prefs.timezone).strftime('%Y-%m-%d %H:%M:%S')
    sender_info = f" from {sender}" if sender else ""
    log_entry = f"[{timestamp}] {direction}{sender_info}: {message}\n"
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        