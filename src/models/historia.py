from flask_restx import fields
from src.server.instance import server

historia = [server.api.model('História', {
    'idioma': fields.String(required=True, description='Idioma do texto a ser processado', enum=['en', 'ptbr']),
    'historia': fields.String(required=True, description='História a ser processada', min_length=1)
})]