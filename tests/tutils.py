import inspect
import random
from unittest.mock import Mock

import peewee

from models import Chat, Transaction

test_users = [
    "@Pupa",
    "@Lupa",
    "@Buhg",
    "@Alte",
    "@Riya",
    "@Zarp",
    "@Lata",
    "@Pere",
    "@Put",
    "@Ali",
    "@Polu",
    "@Chil"
]


def generate_test_set():
    group = random.sample(test_users, random.randrange(1, len(test_users)))
    balances = { user: random.randrange(-2**32, 2**32) for user in test_users }
    ss = sum(balances[user] for user in group)
    return balances, ss


def set_or_create_chat(id=-1, inited=True):
    try:
        chat = Chat.create(id=id, inited=inited)
    except:
        chat = Chat.get(id=id)
        chat.inited = inited

    chat.save()

    return chat


def destroy_chat(id=-1, inited=True):
    try:
        Chat.get(id=id).delete_instance(recursive=True)
    except:
        pass


def make_transaction_mock(**kwargs):
    mock = Mock(Transaction)
    mock.configure_mock(**kwargs)

    return mock


def check_annotated(module_name):
    from importlib import import_module
    module = import_module(module_name)

    functions = inspect.getmembers(module, inspect.isfunction)

    not_annotated = [
        function[1].__name__ for function in functions if inspect.getmodule(function[1]).__name__ == module_name
    ]

    return not_annotated
