import uuid
from .account import Account

class AccountList:
    accounts = []
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AccountList, cls).__new__(cls)
        return cls.instance

    def AddAccount(self, account_id, balance):
        try:
            uuid.UUID(account_id)
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
