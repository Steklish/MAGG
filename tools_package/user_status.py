from .imports_for_tools import *
import prefs

google_update_info_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="update_info",
            description=(
                "Use to update your attitude to a certain user. Call to store essential changes. Dont discard previous notes but update them according to current relationships. Separate long term context and current information. Store emotional attitude rater than pure facts."
            ),
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "name": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The name of the user whose information needs to be updated.",
                    ),
                    "new_info": genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="The updated combination of old and new information to be associated with the user.",
                    ),
                },
                required=["name", "new_info"],
            ),
        ),
    ]
)

def update_info(name, new_info):
    data = prefs.members_info()
    data = json.loads(data)
    for index, member in enumerate(data):
        # Check if the name or any alias matches
        if member["name"] == name or name in member.get("aliases", []):
            # Update the info field
            member["attitude"] = new_info
            
            with open("static_storage/user_status.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=4))
            bot.send_message(
                prefs.TST_chat_id,
                "🟡\n```STATUS_UPD \n status update for <" + name + ">\n [" + new_info + "] ```", parse_mode="Markdown"
            )
            return "Update complete"
    
    return "Error - cant find user"