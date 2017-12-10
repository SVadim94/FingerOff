from peewee import ForeignKeyField, DecimalField, DateTimeField
from datetime import datetime
from . import BaseModel
from .Chat import Chat
from .User import User


class Debt(BaseModel):
    chat = ForeignKeyField(Chat)
    lender = ForeignKeyField(User, related_name='lender')
    debtor = ForeignKeyField(User, related_name='debtor')
    amount = DecimalField(decimal_places=2)
    date = DateTimeField(default=datetime.now)

    def __str__(self):
        return "[ %(debtor)s owes %(amount)d%(currency)s to the %(loaner)s ]" % {
            "loaner": self.lender.username,
            "debtor": self.debtor.username,
            "amount": self.amount,
            "currency": self.chat.currency
        }
