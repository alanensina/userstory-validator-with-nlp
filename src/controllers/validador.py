from flask_restx import Resource

from src.server.instance import server
from src.models.historia import historia
from src.models.cenario import cenario
from src.models.response import response_historia, response_cenario
from src.services.ProcessadorService import processador


app, api = server.app, server.api


@api.route('/historia')
class AnalisarHistoria(Resource):
    @api.expect(historia, validate=True)
    @api.marshal_list_with(response_historia, mask=None)
    def post(self, ):
        payload = api.payload   
        return processador.processar(payload, 'historia')
    
    
@api.route('/cenario')
class AnalisarCenario(Resource):
    @api.expect(cenario, validate=True)
    @api.marshal_list_with(response_cenario, mask=None)
    def post(self, ):
        payload = api.payload
        return processador.processar(payload, 'cenario')
    