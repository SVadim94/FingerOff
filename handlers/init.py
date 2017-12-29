from utils.decorators import check_inited


@check_inited(False)
def init(message, currency=None):
    """/init <currency>
    set default currency for transfers"""
    currency = check_currency(currency)

    if currency is None:
        return available_currencies()

    chat = Chat.create(id=message.chat.id, currency = currency)

    return "Default currency was set to %s" % chat.currency
