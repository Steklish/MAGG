#gene.ral import
from .imports_for_tools import *

# each tool import
from .create_memory import *
from .get_long_term_memory import *
from .send_message import *
from .task import *
from .user_status import *
from .web_search import *
from .analize_url import *
from .send_sticker import *
from .reques_for_message import *

G_TOOLS = [
    google_long_term_memory_tool,
    google_create_memory_tool,
    google_send_message_tool,
    google_instruct_tool,
    google_update_info_tool,
    google_web_search_tool,
    analize_url_tool,
    send_sticker_tool,
    google_reques_for_message_tool
]


def execute_tool(tool_name, args):
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    try:
        if tool_name == 'reques_for_message':
            return "Message request accepted now launch another interaction cycle"
        res = eval(tool_name)(**args)
        print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
        return res
    except Exception as e:
        print (RED, f"Tool exception {tool_name} / {args}")
        print(BACKGROUND_RED, BLACK, e, RESET)
    return "ERROR WHILE EXECUTING THE FUNCTION"