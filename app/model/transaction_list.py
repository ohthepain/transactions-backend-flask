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

    def AddTransaction(self, transaction):
        assert(transaction.is_valid())
        self.transactions.append(transaction)
        return True

    def GetTransaction(self, transaction_id):
        if not uuid.UUID(transaction_id):
            raise ValueError('Bad uuid format')
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction

    def GetTransactions(self):
        return self.transactions

TransactionList()
