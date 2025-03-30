import telebot
from stuff import *
import prefs
import json
import datetime
import time
from ai_handler_google import *

def log_message_with_sender(message:str, direction, sender=None):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = f'logs/{today}.txt'
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sender_info = f" from {sender}" if sender else ""
    log_entry = f"[{timestamp}] {direction}{sender_info}: {message}\n"
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        
        
def check_yesterday_log():
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    log_file = f'logs/{yesterday}.txt'
    
    if os.path.exists(log_file):
        return log_file
    return -1

def check_for_date():
    if check_yesterday_log() != -1:
        res = summarize_file(check_yesterday_log())
        bot.send_message(prefs.TST_chat_id, res)
        os.remove(check_yesterday_log())