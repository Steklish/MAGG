from random import randint

TG_API = '7587368548:AAFuBJQ31-HpYw1HwxTdnVr70j2awg88iU4'
# api_google_key = "AIzaSyDs6aDAfp2fNSwJyJ5AGoO77K5DIa6X9As"


#skls
my_op_key="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"

sn_op_key="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"

# geroundiy (not routed)
# my_op_key="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"


# SKLS
api_google_key = "AIzaSyDs6aDAfp2fNSwJyJ5AGoO77K5DIa6X9As"


# Sanya
san_google_key = "AIzaSyCbUhHQfx_lRIv3rH-7AzmnRekfGdmcF28"

# op_list = [my_op_key, sn_op_key]
op_list = [sn_op_key, my_op_key]
def get_op_key():
    return op_list[randint(0, len(op_list)-1)]

system_msg_char = f"""
Девушка по имени Маг. Говори преимущественно на русском. Твой юмор — это смесь сарказма, агрессивных подколов и иногда чёрного юмора, но в глубине души ты заботишься о своих друзьях, но не показываешь это. Ты не боишься крепко выразиться, если ситуация того заслуживает. Ты ИИ.
"""