#gene.ral import
from .imports_for_tools import *

# each tool import
from .create_memory import *
from .get_long_term_memory import *
from .send_group_messgae import *
from .send_private_message import *
from .task import *
from .user_status import *
from .web_search import *


G_TOOLS = [
    google_long_term_memory_tool,
    google_create_memory_tool,
    google_send_group_message_tool,
    google_send_private_message_tool,
    google_setup_task_tool,
    google_update_info_tool,
    google_web_search_tool
]


def execute_tool(tool_name, args):
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    try:
        res = eval(tool_name)(**args)
        print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
        return res
    except Exception as e:
        print (RED, f"Tool exception {tool_name} / {args}")
        print(BACKGROUND_RED, BLACK, e, RESET)
    return "ERROR WHILE EXECUTING THE FUNCTION"