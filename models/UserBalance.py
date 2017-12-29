from peewee import DecimalField, ForeignKeyField, CompositeKey

from models import Chat, User, db

from . import BaseModel


class UserBalance(BaseModel):
    class Meta:
        primary_key = CompositeKey('chat', 'user')
        database = db

    chat = ForeignKeyField(Chat)
    user = ForeignKeyField(User)
    balance = DecimalField(default=0, decimal_places=3)

    def __str__(self):
        return "%s: %s" % (self.user.username, self.balance)
