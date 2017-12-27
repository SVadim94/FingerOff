from peewee import SqliteDatabase, Model
import config


db = SqliteDatabase(config.db)


class BaseModel(Model):
    class Meta:
        database = db


from .DebtGraph import DebtGraph
from .Chat import Chat
from .User import User
from .Transaction import Transaction, TransactionType

db.create_tables([Chat, User, Transaction, DebtGraph], safe=True)
