from utils.decorators import check_inited

from .balance import balance
from .foff import foff
from .init import init
from .show import show
from .transfer import transfer

__all__ = ["handlers", "balance", "foff", "init", "show", "transfer"]


@check_inited(False, False)
def usage(_):
    """/usage
    show this message"""

    return \
"""Usage:

%s

TBD:
/cancel <transaction_id>
    cancels transaction by its id
/archive
    archives debts history and returns archive's id
/get <archive_id>
    get archive by id
/purge
    cleans debts history (history will be archived)""" % "\n".join(handler.__doc__ for handler in handlers.values())

handlers = {
    "/init": init,
    "/transfer": transfer,
    "/balance": balance,
    "/foff": foff,
    "/show": show,
    "/usage": usage
}
