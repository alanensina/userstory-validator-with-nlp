from flask_restx import fields
from src.server.instance import server

response_historia = server.api.model('Response', {
    'texto': fields.String(description='Texto processado'),
    'tecnologia': fields.String(description='Tecnologia utilizada'),
    'tempo': fields.String(description='Tempo de processamento'),
    'bemFormada': fields.Boolean(description='Critério de qualidade se a história é bem formada'),
    'atomica': fields.Boolean(description='Critério de qualidade se a história é atômica'),
    'minima': fields.Boolean(description='Critério de qualidade se a história é mínima'),
    'ator': fields.String(description='Ator que desempenha a ação na história'),
    'acao': fields.String(description='Ação realizada pelo ator'),
    'finalidade': fields.String(description='Finalidade da ação. É opcional.'),
    'erros': fields.String(description='Possíveis erros encontrados')
})

response_cenario = server.api.model('Response', {
    'texto': fields.String(description='Texto processado'),
    'tecnologia': fields.String(description='Tecnologia utilizada'),
    'tempo': fields.String(description='Tempo de processamento'),
    'bemFormado': fields.Boolean(description='Critério de qualidade se o cenário é bem formado'),
    'atomico': fields.Boolean(description='Critério de qualidade se o cenário é atômico'),
    'minimo': fields.Boolean(description='Critério de qualidade se o cenário é mínimo'),
    'preCondicao': fields.String(description='Pré-condição do cenário'),
    'acao': fields.String(description='Ação realizada'),
    'finalidade': fields.String(description='Finalidade da ação. É opcional.'),
    'erros': fields.String(description='Possíveis erros encontrados')
})