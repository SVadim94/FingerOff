from models import Chat, UserBalance
from utils.decorators import check_inited
from utils.output import join_columns


@check_inited(True)
def balance(message):
    """/balance
    shows balance for current chat"""
    return join_columns(UserBalance.select().where(UserBalance.chat == Chat.get(Chat.id == message.chat.id)))
