from peewee import DecimalField, ForeignKeyField

from models import Chat, User

from . import BaseModel


class UserBalance(BaseModel):
    chat = ForeignKeyField(Chat)
    user = ForeignKeyField(User)
    balance = DecimalField(default=0, decimal_places=3)

    def __str__(self):
        return "%s: %s" % (self.user.username, self.balance)
