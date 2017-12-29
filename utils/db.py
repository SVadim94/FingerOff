from models import User, UserBalance, db


def merge_transaction(transaction):
    with db.atomic():
        creditor, _ = UserBalance.get_or_create(chat=transaction.chat, user=transaction.creditor)
        creditor.balance -= transaction.amount

        if creditor.balance == 0:
            creditor.delete_instance()
        else:
            creditor.save()

        debtor, _ = UserBalance.get_or_create(chat=transaction.chat, user=transaction.debtor)
        debtor.balance += transaction.amount

        if debtor.balance == 0:
            debtor.delete_instance()
        else:
            debtor.save()


def get_or_create_user(username):
    return User.get_or_create(username=username.lower())[0]
