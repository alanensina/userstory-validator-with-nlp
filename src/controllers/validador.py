from flask_restx import Resource

from src.server.instance import server
from src.models.historia import historia
from src.models.cenario import cenario

from src.services.NLTK import NLTK
from src.services.spaCy import spaCy

app, api = server.app, server.api

@api.route('/historia')
class AnalisarHistoria(Resource):
    @api.expect(historia, validate=True)
    def post(self, ):
        payload = api.payload
        response = []
        
        for p in payload:
            idioma = p.get('idioma')
            historia = p.get('historia')
            response.append(NLTK.processarHistoria(idioma, historia))
            response.append(spaCy.processarHistoria(idioma, historia))
        
        return response
    
@api.route('/cenario')
class AnalisarCenario(Resource):
    @api.expect(cenario, validate=True)
    def post(self, ):
        payload = api.payload
        response = []
        
        for p in payload:
            idioma = p.get('idioma')
            cenario = p.get('cenario')
            response.append(NLTK.processarCenario(idioma, cenario))
            response.append(spaCy.processarCenario(idioma, cenario))
        
        return response
    