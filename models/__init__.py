from peewee import SqliteDatabase, Model
import config


db = SqliteDatabase(config.db)


class BaseModel(Model):
    class Meta:
        database = db


from .DebtGraph import DebtGraph
from .Chat import Chat
from .User import User
from .Debt import Debt

db.create_tables([Chat, User, Debt, DebtGraph], safe=True)
