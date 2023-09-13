import uuid

class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def is_valid(self):
        try:
            uuid.UUID(account_id)
        except ValueError:
            return False
        finally:
            return True
