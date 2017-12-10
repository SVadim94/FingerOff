from peewee import BigIntegerField, CharField
from . import BaseModel
import config


class Chat(BaseModel):
    id = BigIntegerField(unique=True, primary_key=True)
    currency = CharField(default=config.default_currency, max_length=3)
