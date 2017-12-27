from enum import Enum

from peewee import *

import config

from . import BaseModel
from .Chat import Chat
from .User import User


class TransactionType(Enum):
    DEBT = 0
    CANCEL = 1


class Transaction(BaseModel):
    chat = ForeignKeyField(Chat)
    transaction_id = UUIDField()
    transaction_type = IntegerField(default=TransactionType.DEBT.value)
    date = DateTimeField()
    debtor = ForeignKeyField(User, related_name='debtor')
    creditor = ForeignKeyField(User, related_name='creditor')
    amount = DecimalField(decimal_places=2)
    currency = CharField(default=config.default_currency, max_length=3)
    original_amount = DecimalField(decimal_places=2)
    original_currency = CharField(default=config.default_currency, max_length=3)
    description = CharField(null=True, max_length=4096)
    extra = UUIDField(null=True)

    def __str__(self):
        if self.transaction_type == TransactionType.CANCEL.value:
            return "[%(transaction_id)s] cancel of [%(extra)s]" % {
                "transaction_id": self.transaction_id,
                "extra": self.extra
            }

        return "[%(transaction_id)s] | %(date)s | (%(creditor)s)>-(%(amount)d%(currency)s)->(%(debtor)s) | %(original_amount)s%(original_currency)s -- %(description)s" % {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "creditor": self.creditor.username,
            "debtor": self.debtor.username,
            "amount": self.amount,
            "currency": self.chat.currency,
            "original_amount": self.original_amount,
            "original_currency": self.original_currency,
            "description": self.description
        }
