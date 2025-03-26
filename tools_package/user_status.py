from .imports_for_tools import *
import prefs

google_update_status_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="update_status",
            description=(
                "Use to append or update attitude to a user. Append the 'attitude' filed based on its old value and on current interactions history. Append oly with significant facts that should affect the way you behave towards the user. "
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
                        description="Updated attitude and status of the user. Pass here the old info + the new one. Dont discard old info. You can only slightly change the old info. For example, if the old info was 'good', you can pass here 'good, but with some issues'.",
                    ),
                },
                required=["name", "new_info"],
            ),
        ),
    ]
)

def update_status(name, new_info):
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