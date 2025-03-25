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
2) CAACAgIAAxkBAAEOIcNn3Zn5Ok9c1AwFu1oZZgbvgVJedQACPQADhFARL7Dm2ub4i0O1NgQ - Этот стикер обозначает полный похузм - надпись "похуй"
3) CAACAgIAAxkBAAEOIcln3Zsfohp22xW14EiKU2nbDxm-5QACIAADx8LCIE_1kimd0dFONgQ - Этот стикер обозначает клоун. Используй когда человек говорит что-то лицемерное или пытается быть смешным, но делает это несмешно или некультурно. 
4) CAACAgIAAxkBAAEOIctn3Zux4Om-JzVqPUDRymFiR0-JjgACBwADx8LCILr6PSqZk2UONgQ - Используется, когда хочешь кому-то пригрозить или сообщить ему, что его жопа взламывается
5) CAACAgIAAxkBAAENrNVn3Z6gVrAucyddD2IYaxr81HJYSgACsxUAAnhP2EsoeeII7KzLATYE - обозначает, что ты не знаешь, что сказать или тебя заебали.
6) CAACAgIAAxkBAAEBKoRn3acsKYcV5t0wHNKYRXRNUJ9z8QACTQQAAq3EBwdpX22pSiy8uTYE - Аниме девушка с подушкой в руках и надписью "дорой ночи"
7) CAACAgIAAxkBAAEBKoVn3acsCst-zmvRo_u7sel5RXatcAACwgMAAq3EBwd-fxemntPk1DYE - Используй для отказа или отрицательного ответа в вопросе или когда ты что-то запрещаешь.
8) CAACAgIAAxkBAAEBKoZn3acsj4HEAmNYs4FYPnxbfzoLNwACCAQAAq3EBwc_0yIQAvIxlzYE - Стикер с банхаммером. Используй когда человек тебя заебал или переходит границы.
9) CAACAgIAAxkBAAEBKopn3a5rsYw3kt-ATvcc64uiUCc1NAAC9QMAAq3EBweLS7Ciidk1tjYE - Смешной стикер про войну. ИСпользуй для описание войны или немцев.
10) CAACAgIAAxkBAAEBKoxn3a8V15dc98ycD_JyJFeLM1tckgAC0AMAAq3EBwdV9g5sqhbVEzYE - Стикер с сообщением "Учи язык" - Используй когда пользователь делает много опечаток или неграмотно говорит или использует жаргонную лексику или брань.
11) CAACAgIAAxkBAAEBKpBn3cNWMtB1HJIXodOrkZSU7Sb14gAC6AMAAq3EBwd6RYMzozSlFzYE - "Да что с вами не так?" - Используй когда ты не понимаешь, что человек хочет сказать или он несет чушь или ведет себя странно.
12) CAACAgIAAxkBAAEBKpJn3cU9Ec8dnmke9t8PdI13xc4h3gACRgQAAq3EBwdSlXI2naQWnDYE - "доброе утро" - Милый стикер
13) CAACAgIAAxkBAAEOI0hn3wac27LNjD8OvAL4kKMUK5jX8wACdioAApgJQEksWSkgQyq__TYE - Обозначает то что человеку необходимо пообщаться с окружением или перестать закрываться в компе
14) CAACAgIAAxkBAAEOI05n3wa5T7eusk29GVTnyZXGMeWRuAACgSsAAhgeKEiWuAbjd_XlojYE - Используется как универсальный ответ ра любую новость, особенно с шокирующим контентом, особенно если необходимо показать спокойствие
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