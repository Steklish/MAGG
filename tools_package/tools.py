#gene.ral import
from .imports_for_tools import *

# each tool import
from .create_memory import *
from .get_long_term_memory import *
from .send_group_messgae import *
from .send_private_message import *
from .task import *
from .user_status import *

TOOLS = [
    long_term_memory_tool,
    create_memory_tool,
    send_group_message_tool,
    send_private_message_tool,
    setup_task_tool,
    update_info_tool
]

TOOLS_FORCE_SEND = [
    send_group_message_tool,
    send_private_message_tool
]
TOOLS_NO_RESPONSE = [
    long_term_memory_tool,
    create_memory_tool,
    setup_task_tool,
    update_info_tool
]

def execute_tool(tool_name, args):
    print(f"{BACKGROUND_YELLOW} {BLACK} {tool_name}  with args {args}{RESET}")
    res = eval(tool_name)(**json.loads(args))
    print(f"{BACKGROUND_GREEN}{BLACK}{res}{RESET}")
    return res
