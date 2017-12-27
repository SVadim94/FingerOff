import peewee
from models import Chat

def set_or_create_chat(id=-1, inited=True):
    try:
        chat = Chat.create(id=id, inited=inited)
    except:
        chat = Chat.get(id=id)
        chat.inited = inited

    chat.save()

    return chat

def destroy_chat(id=-1, inited=True):
    try:
        Chat.get(id=id).delete_instance(recursive=True)
    except:
        pass
