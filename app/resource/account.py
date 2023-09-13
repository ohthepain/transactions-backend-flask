import uuid
import jsonpickle
from flask_restx import Namespace, Resource, fields
from model.account import Account
from model.account_list import AccountList

print('hi from account. __name__ is %s' % (__name__))

api = Namespace('account', description='Account related operations')

account = api.model('Account', {
    'account_id': fields.String(required=True, description='Account id'),
    'amount': fields.Float(required=True, description='Current balance'),
})

# accounts = [
#     Account('566944be-2dab-460b-b3ed-eeeebd8c5618', 100)
#     # {'account_id': '566944be-2dab-460b-b3ed-eeeebd8c5618', 'amount': '100'},
# ]

# def GetAccount(account_id):
#     for account in accounts:
#         if account.account_id == account_id:
#             return account

@api.route('/accounts/<account_id>')
@api.doc('get_account')
@api.param('account_id', 'Account id')
@api.response(200, 'OK')
@api.response(400, 'Mandatory body parameters missing or have incorrect type.')
@api.response(404, 'Account not found')
class GetAccount(Resource):
    # @api.marshal_with(account)
    def get(self, account_id):
        print('hi from account.get')
        try:
            uuid.UUID(account_id)
        except ValueError:
            return {'message' : 'Mandatory body parameters missing or have incorrect type'}, 400
        accountList = AccountList()
        account = accountList.GetAccount(account_id)
        if account:
            return jsonpickle.encode(account), 200
        # for account in accounts:
        #     print('account %s ' % (jsonpickle.encode(account)))
        #     # print('account %s %s' & (account.account_id, account.amount))
        #     account = GetAccount()
        #     if account['account_id'] == account_id:
        return {'message' : 'Account not found'}, 404
