from .imports_for_tools import *
import prefs

update_info_tool = {
    "type": "function",
    "function": {
        "name": "update_info",
        "description": (
            "Use to update info that forms your relationship with a certain user. Call to store significant changes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the user whose information needs to be updated."
                },
                "new_info": {
                    "type": "string",
                    "description": "The combinaton of old and new information to be associated with the member."
                }
            },
            "required": ["name", "new_info"]
        }
    }
}

def update_info(name, new_info):
    data = prefs.members_info()
    data = json.loads(data)
    for index, member in enumerate(data):
        # Check if the name or any alias matches
        if member["name"] == name or name in member.get("aliases", []):
            # Update the info field
            member["info"] = new_info
            
            with open("static_storage/user_status.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=4))
            bot.send_message(
                prefs.TST_chat_id,
                "```STATUS_UPD \n status update for <" + name + ">\n [" + new_info + "] ```", parse_mode="Markdown"
            )
            return "Update complete"
    
    return "Error - cant find user"