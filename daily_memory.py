import telebot
from stuff import *
import prefs
import json
import datetime
import time
from ai_handler_google import *
import ai_handler_google

        
def check_yesterday_log():
    yesterday = (datetime.datetime.now(prefs.timezone) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    log_file = f'logs/{yesterday}.txt'
    
    if os.path.exists(log_file):
        return log_file
    return -1

def check_for_date():
    if check_yesterday_log() != -1:
        res = ai_handler_google.summarize_file(check_yesterday_log())
        bot.send_message(prefs.TST_chat_id, res)
        os.remove(check_yesterday_log())