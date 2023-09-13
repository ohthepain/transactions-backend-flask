import uuid
from datetime import datetime

class Transaction:
    def __init__(self, account_id, amount):
        self.account_id = account_id
        self.amount = amount
        self.transaction_id = str(uuid.uuid4())
        self.created_at = datetime.now()

    def is_valid(self):
        try:
            uuid.UUID(self.transaction_id)
            uuid.UUID(self.account_id)
            if self.amount == 0:
                raise Exception("Transaction amount cannot be 0")
            return True
        except ValueError:
            return False
