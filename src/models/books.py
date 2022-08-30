from pydoc import describe
from flask_restx import fields
from src.server.instance import server

book = server.api.model('Book', {
    'id': fields.Integer(description='Id do livro'),
    'title': fields.String(required=True, description='Título do livro')
})