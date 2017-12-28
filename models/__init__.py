from peewee import SqliteDatabase, Model
import config


db = SqliteDatabase(config.db)


class BaseModel(Model):
    class Meta:
        database = db


from .Chat import Chat
from .User import User
from .UserBalance import UserBalance
from .Transaction import Transaction, TransactionType

db.create_tables([Chat, User, UserBalance, Transaction], safe=True)
