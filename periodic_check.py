import ai_handler
import asyncio
from stuff import *
import tools_package.tools as tools
#functuin that 
async def check_state() -> None:
    while True:
        print(YELLOW, "tick", RESET)
        if tools.reminder_check(): 
            ai_handler.smart_response(TEMP=2, tool_choice="any", TOOLSET=tools.TOOLS_FORCE_SEND)
        
        # repeat every 10 minutes
        await asyncio.sleep(10*60)