import ai_handler
import asyncio
from stuff import *
import tools_package.tools as tools
import prefs

async def check_state():
    while True:
        print(YELLOW, "tick", RESET)
        if tools.reminder_check(): 
            ai_handler.smart_response(TEMP=prefs.TEMPERATURE, tool_choice="required", TOOLSET=tools.TOOLS_FORCE_SEND)
        
        # repeat every 5 minutes
        await asyncio.sleep(5*60)