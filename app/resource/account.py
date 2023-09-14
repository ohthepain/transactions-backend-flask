import uuid
from flask_restx import Namespace, Resource, fields
from model.account import Account
from model.account_list import AccountList

api = Namespace('account', description='Account related operations')

account = api.model('Account', {
    'account_id': fields.String(required=True, description='Account id; i.e., 566944be-2dab-460b-b3ed-eeeebd8c5618'),
    'balance': fields.Float(required=True, description='Current balance'),
})

@api.route('accounts/<account_id>')
@api.doc('get_account')
@api.param('account_id', 'Account id')
@api.response(200, 'OK')
@api.response(400, 'Mandatory body parameters missing or have incorrect type.')
@api.response(404, 'Account not found')
class GetAccount(Resource):
    @api.marshal_with(account)
    def get(self, account_id):
        try:
            uuid.UUID(account_id)
        except ValueError:
            return {'message' : 'Mandatory parameters missing or have incorrect type'}, 400
        accountList = AccountList()
        account = accountList.GetAccount(account_id)
        if account:
            return account, 200
        return {'message' : 'Account not found'}, 404
