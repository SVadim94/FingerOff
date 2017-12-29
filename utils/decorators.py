from models import Chat
from functools import wraps
import peewee


def check_inited(needs_to_be_existed, needs_to_be_checked=True):
    def wrapper(foo):
        @wraps(foo)
        def wrapped(*args, **kwargs):
            if not needs_to_be_checked:
                return foo(*args, **kwargs)

            try:
                chat = Chat.get(id=args[0].chat.id)
                exists = True
            except peewee.DoesNotExist:
                exists = False

            if needs_to_be_existed == exists:
                return foo(*args, **kwargs)

            if needs_to_be_existed:
                return "Please, /init first"
            else:
                return "Already inited"

        wrapped.checks_inited = True
        return wrapped

    return wrapper


def add_desc(desc):
    def wrapper(foo):
        foo.desc = desc
        return foo

    return wrapper
