import uuid
import jsonpickle
from datetime import datetime
from model.transaction import Transaction
from model.account_list import AccountList
from model.transaction_list import TransactionList
from flask_restx import Namespace, Resource, fields

print('hi from transaction. __name__ is %s' % (__name__))

api = Namespace('transaction', description='Transaction operations')

transaction = api.model('Transaction', {
    'transaction_id': fields.String(required=True, description='Transaction id'),
    'account_id': fields.String(required=True, description='Account id'),
    'amount': fields.Float(required=True, description='Transaction amount'),
    'created_at': fields.String(required=True, description='Creation time'),
})

transactions = []
transactions.append(Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 10))
transactions.append(Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 20))
transactions.append(Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 30))
print('newTransaction at init %s' % jsonpickle.encode(Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 30)))

# There is no separate account resource
# accounts = [
#     {'account_id': '566944be-2dab-460b-b3ed-eeeebd8c5618', 'balance': 60},
# ]

TransactionRequest = api.model('TransactionRequest', {
    'amount': fields.Integer(required=True, description='The transaction amount'),
    'account_id': fields.String(description='The account ID for the transaction (UUID)'),
})

@api.route('/transaction')
class PostTransactionResource(Resource):
    @api.expect(TransactionRequest)
    @api.response(201, 'Transaction created successfully')
    @api.response(400, 'Mandatory body parameters missing or have incorrect type.')
    def post(self):
        print('welcome to post transaction. transactions are %s' % jsonpickle.encode(transactions))
        print('newTransaction %s' % jsonpickle.encode(Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 30)))

        data = api.payload
        amount = data.get('amount')
        account_id = data.get('account_id')
        if not amount or amount <= 0:
            return {'message': 'Mandatory body parameters missing or have incorrect type.'}, 400
        try:
            uuid.UUID(account_id)
        except ValueError:
            return {'message': "Mandatory body parameters missing or have incorrect type."}, 400

        account = AccountList().GetAccount(account_id)
        if not account:
            AccountList().AddAccount(account_id, 0)
            account = AccountList().GetAccount(account_id)

        newTransaction = Transaction('566944be-2dab-460b-b3ed-eeeebd8c5618', 10)
        print('newTransaction %s' % jsonpickle.encode(newTransaction))

        newTransaction = Transaction(account_id, amount)
        print('newTransaction %s' % jsonpickle.encode(newTransaction))
        transactions.append(newTransaction)

        # TODO: We do this last since this operation is the least likely to fail and we don't have time to implement transactions
        # TODO: Refactor. For now it's only 1 bad line of code
        account.balance += amount

        return {'transaction_id': newTransaction.transaction_id}, 201

    @api.doc('list_transactions')
    @api.response(200, 'List of transactions')
    def get(self):
        print('welcome to get transactions. transactions are %s' % jsonpickle.encode(transactions))
        return jsonpickle.encode(transactions), 200

@api.route('/transaction/<transaction_id>')
@api.param('transaction_id', 'Transaction id')
@api.response(200, 'Transaction')
@api.response(400, 'Mandatory body parameters missing or have incorrect type.')
@api.response(404, 'Transaction not found')
class GetTransaction(Resource):
    @api.doc('get_transaction')
    # @api.marshal_with(transaction)
    def get(self, transaction_id):
        print('welcome to get transaction. transactions are %s' % (jsonpickle.encode(transactions)))
        print('welcome to get transaction. transaction_id is %s' % (transaction_id))
        try:
            uuid.UUID(transaction_id)
        except ValueError:
            return {'message': "Mandatory body parameters missing or have incorrect type. - transaction_id must be a uuid"}, 400
        for transaction in transactions:
            if transaction.transaction_id == transaction_id:
                return jsonpickle.encode(transaction), 200
        return {'message': "Transaction not found"}, 404
