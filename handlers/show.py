import peewee

from models import Chat, Transaction, User
from utils.decorators import check_inited
from utils.misc import is_int
from utils.output import join_columns


@check_inited(True)
def show(message, *args):
    """/show [N] [@nickname] [@nickname]
    prints transactions:
        N - last N transactions (default 10)
        @nickname - transactions related to @nickname user"""
    usernames = [_ for _ in args if _.startswith('@')]
    numbers = [_ for _ in args if is_int(_)]

    query = Chat.id == message.chat.id

    if usernames:
        for username in usernames:
            username = username.lower()

            try:
                user = User.get(User.username == username)
            except peewee.DoesNotExist:
                return "No such user %s" % username

            query &= (Transaction.creditor == user) | (Transaction.debtor == user)

    if numbers:
        N = int(numbers[0])
    else:
        N = 10

    return join_columns(Transaction.select().join(Chat).where(query).order_by(Transaction.timestamp.desc()).limit(N))
