import ai_handler
import asyncio
from stuff import *
import tools_package.tools as tools
#functuin that 
async def check_state() -> None:
    while True:
        print(YELLOW, "tick", RESET)
        tools.reminder_check() 
        ai_handler.smart_response()
        # repeat every 10 minutes
        await asyncio.sleep(10*60)