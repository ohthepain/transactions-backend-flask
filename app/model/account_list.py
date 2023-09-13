import uuid
from .account import Account

class AccountList:
    accounts = []
    def __new__(cls):
        print('ctor: %s' % (__name__))
        if not hasattr(cls, 'instance'):
            print('ctor: create singleton instance of %s' % (__name__))
            cls.instance = super(AccountList, cls).__new__(cls)
        print('ctor: access singleton instance of %s' % (__name__))
        return cls.instance

    def AddAccount(self, account_id, balance):
        try:
            uuid.UUID(account_id)
            if balance == 0:
                raise Exception("Transaction amount cannot be 0")
            self.accounts.append(Account(account_id, balance))
            return True
        except ValueError:
            return False

    def GetAccount(self, account_id):
        if not uuid.UUID(account_id):
            raise ValueError('Bad uuid format')
        for account in self.accounts:
            if account.account_id == account_id:
                return account

AccountList()
AccountList().AddAccount('566944be-2dab-460b-b3ed-eeeebd8c5618', 100)
