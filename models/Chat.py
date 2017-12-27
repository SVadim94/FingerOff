from peewee import BigIntegerField, CharField, BooleanField
from . import BaseModel
import config


class Chat(BaseModel):
    id = BigIntegerField(unique=True, primary_key=True)
    currency = CharField(default=config.default_currency, max_length=3)
    inited = BooleanField(default=False)
