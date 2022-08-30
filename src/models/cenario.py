from flask_restx import fields
from src.server.instance import server

cenario = [server.api.model('Cenário', {
    'idioma': fields.String(required=True, description='Idioma do texto a ser processado', enum=['en', 'ptbr']),
    'cenario': fields.String(required=True, description='Cenário a ser processado')
})]