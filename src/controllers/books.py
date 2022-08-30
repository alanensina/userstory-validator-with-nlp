from flask_restx import Resource

from src.server.instance import server
from src.models.books import book

app, api = server.app, server.api


books = [
    {'id': 1, 'title': 'Sandman 1'},
    {'id': 2, 'title': 'Clean code'},
    {'id': 3, 'title': 'War and Peace'},
    {'id': 4, 'title': 'The Lord of the Rings'},
    {'id': 5, 'title': 'The Wise'}
]

@api.route('/books')
class BookList(Resource):
    @api.marshal_list_with(book)
    def get(self, ):
        return books
    
    @api.expect(book, validate=True)
    @api.marshal_with(book)
    def post(self, ):
        response = api.payload
        books.append(response)
        return response, 200