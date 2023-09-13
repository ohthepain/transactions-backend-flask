import uuid
from .transaction import Transaction

class TransactionList:
    transactions = []
    def __new__(cls):
        print('ctor: %s' % (__name__))
        if not hasattr(cls, 'instance'):
            print('ctor: create singleton instance of %s' % (__name__))
            cls.instance = super(TransactionList, cls).__new__(cls)
        print('ctor: access singleton instance of %s' % (__name__))
        return cls.instance

    def AddTransaction(self, account_id, amount):
        try:
            uuid.UUID(account_id)
            if amount == 0:
                raise Exception("Transaction amount cannot be 0")
            self.transactions.append(Transaction(account_id, amount))
            return True
        except ValueError:
            return False

    def GetTransaction(self, transaction_id):
        if not uuid.UUID(transaction_id):
            raise ValueError('Bad uuid format')
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction

TransactionList()
TransactionList().AddTransaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 10)
