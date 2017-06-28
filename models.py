from peewee import *
import datetime
import config

db = SqliteDatabase(config.db)


class BaseModel(Model):
    class Meta:
        database = db


class Chat(BaseModel):
    chat_id = IntegerField(unique=True)
    currency = TextField(default=config.default_currency)


class User(BaseModel):
    username = TextField(unique=True)


class Debt(BaseModel):
    src = ForeignKeyField(User, related_name='src')
    dst = ForeignKeyField(User, related_name='dst')
    amount = DecimalField(decimal_places=2)
    date = DateTimeField(default=datetime.datetime.now)

db.create_tables([Chat, User, Debt], safe=True)
