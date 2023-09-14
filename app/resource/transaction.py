import uuid
from datetime import datetime
from model.transaction import Transaction
from model.account_list import AccountList
from model.transaction_list import TransactionList
from flask_restx import Namespace, Resource, fields

api = Namespace('transaction', description='Transaction operations')

transaction = api.model('Transaction', {
    'transaction_id': fields.String(required=True, description='Transaction id'),
    'account_id': fields.String(required=True, description='Account id'),
    'amount': fields.Float(required=True, description='Transaction amount'),
    'created_at': fields.String(required=True, description='Creation time'),
})

TransactionRequest = api.model('TransactionRequest', {
    'amount': fields.Integer(required=True, description='The transaction amount'),
    'account_id': fields.String(description='The account ID for the transaction (UUID); i.e, 566944be-2dab-460b-b3ed-eeeebd8c5618'),
})

@api.route('transaction')
class PostTransactionResource(Resource):
    @api.expect(TransactionRequest)
    @api.response(201, 'Transaction created successfully')
    @api.response(400, 'Mandatory body parameters missing or have incorrect type.')
    def post(self):
        data = api.payload
        amount = data.get('amount')
        account_id = data.get('account_id')
        if not amount or amount == 0:
            return {'message': 'Mandatory body parameters missing or have incorrect type.'}, 400
        try:
            uuid.UUID(account_id)
        except ValueError:
            return {'message': "Mandatory body parameters missing or have incorrect type."}, 400

        account = AccountList().GetAccount(account_id)
        if not account:
            AccountList().AddAccount(account_id, 0)
            account = AccountList().GetAccount(account_id)

        newTransaction = Transaction(account_id, amount)
        TransactionList().AddTransaction(newTransaction)

        # TODO: We do this last since this operation is the least likely to fail and we don't have time to implement transactions
        # TODO: Refactor. For now it's only 1 bad line of code
        account.balance += amount

        return {'transaction_id': newTransaction.transaction_id}, 201

    @api.doc('list_transactions')
    @api.response(200, 'List of transactions')
    @api.marshal_list_with(transaction)
    def get(self):
        return TransactionList().GetTransactions(), 200

@api.route('transaction/<transaction_id>')
@api.param('transaction_id', 'Transaction id')
@api.response(200, 'Transaction')
@api.response(400, 'Mandatory body parameters missing or have incorrect type.')
@api.response(404, 'Transaction not found')
class GetTransaction(Resource):
    @api.doc('get_transaction')
    @api.marshal_with(transaction)
    def get(self, transaction_id):
        try:
            uuid.UUID(transaction_id)
        except ValueError:
            return {'message': "Mandatory body parameters missing or have incorrect type."}, 400
        transaction = TransactionList().GetTransaction(transaction_id)
        if transaction:
            return transaction, 200
        return {'message': "Transaction not found"}, 404
