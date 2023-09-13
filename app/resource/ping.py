from flask_restx import Namespace, Resource, fields

api = Namespace('ping', description='Healthcheck to make sure the service is up.')

@api.route('/ping')
class Ping(Resource):
    @api.doc('Healthcheck to make sure the service is up.')
    def get(self):
        return 'pong'
