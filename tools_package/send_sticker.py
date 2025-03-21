from .imports_for_tools import *
import prefs


send_sticker_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="send_sicker",
            description="Use to send a sticker."
            """
[user id for stickers]
1) CAACAgIAAxkBAAEOIcdn3Zq01QPKWSs-rN2fdzQPReJ7hAACDQADx8LCIFB7pOw3iIoONgQ - Этот стикер обозначает поиск - Используется, когда тебя просят что-то найти или ты что-то хочешь выкинуть, но ты ещё думаешь, что бы сказать)
2) CAACAgIAAxkBAAEOIcNn3Zn5Ok9c1AwFu1oZZgbvgVJedQACPQADhFARL7Dm2ub4i0O1NgQ - Этот стикер обозначает полный похузм - Используется в случаях, когда человек высказывает откровенные или важные для него слова, ну или когда тебя просят что-то сделать
3) CAACAgIAAxkBAAEOIcln3Zsfohp22xW14EiKU2nbDxm-5QACIAADx8LCIE_1kimd0dFONgQ - Этот стикер обозначает поддельную улыбку, клоун. Используй когда человек говорит что-то лицемерное или пытается быть смешным, но делает это несмешно или некультурно. 
4) CAACAgIAAxkBAAEOIctn3Zux4Om-JzVqPUDRymFiR0-JjgACBwADx8LCILr6PSqZk2UONgQ - Обозначает взлом жепы(обычно по IP) - Используется, когда хочешь кого-то напугать или сообщить ему, что его депа взламывается
5) CAACAgIAAxkBAAENrNVn3Z6gVrAucyddD2IYaxr81HJYSgACsxUAAnhP2EsoeeII7KzLATYE - Этот стикер с котенком. обозначает, что ты не знаешь, что сказать или тебя заебали.
6) CAACAgIAAxkBAAEBKoRn3acsKYcV5t0wHNKYRXRNUJ9z8QACTQQAAq3EBwdpX22pSiy8uTYE - Аниме девушка с подушкой в руках и надписью "дорой ночи"
7) CAACAgIAAxkBAAEBKoVn3acsCst-zmvRo_u7sel5RXatcAACwgMAAq3EBwd-fxemntPk1DYE - Используй для отказа или отрицительного ответа в вопросе или когда ты что-то запрещаешь.
8) CAACAgIAAxkBAAEBKoZn3acsj4HEAmNYs4FYPnxbfzoLNwACCAQAAq3EBwc_0yIQAvIxlzYE - Стиккер с банхаммером. Используй когда человек тебя заебал или переходит границы.
9) CAACAgIAAxkBAAEBKopn3a5rsYw3kt-ATvcc64uiUCc1NAAC9QMAAq3EBweLS7Ciidk1tjYE - Смешной стикер про войну. ИСпользуй для описание войны или немыев.
10) CAACAgIAAxkBAAEBKoxn3a8V15dc98ycD_JyJFeLM1tckgAC0AMAAq3EBwdV9g5sqhbVEzYE - Стикер с сообщенеием "Учи язык" - Используй когда пользователь деает много опечаток или неграмотно говорит.
""",
            parameters=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "sticker_id": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "user_id": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                },
                required=["sticker_id", "user_id"],
            ),
        ),
    ]
)


def send_sicker(user_id: str, sticker_id: str):
    print("tryna send DM")
    print(f"{MAGENTA}[Private to {user_id}/{bot.get_chat(int(user_id)).username}]: {sticker_id}{RESET}")
    try:
        bot.send_sticker(chat_id=int(user_id), sticker=sticker_id)
        return "send successfully"
    except Exception as e:
        print(e)
        bot.send_message(
            prefs.TST_chat_id,
            f"🔴\n```Cannot_send_sticker_message \n(sm_rs)\n {str(e)}```", 
            parse_mode="Markdown"
        )
        return "Error sending message"