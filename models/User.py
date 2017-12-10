from . import BaseModel
from peewee import CharField


class User(BaseModel):
    username = CharField(unique=True, primary_key=True)
