from peewee import CharField

from . import BaseModel


class User(BaseModel):
    username = CharField(unique=True, primary_key=True)
