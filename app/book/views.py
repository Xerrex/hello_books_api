from flask_restful import Resource, reqparse

from app.models import BOOKS, abort_if_book_does_not_exist, abort_if_book_exists
from app.models import Book

from app.utils.data_validators import string_validator


class BookResource(Resource):
    """
    Handles request to : /api/v1/books/<bookId>
    """

    def __init__(self):

        self.book_parser = reqparse.RequestParser()

        self.book_parser.add_argument('name', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('description', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('section', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank ',
                                      location='json')

    def put(self, bookId):
        abort_if_book_does_not_exist(bookId)
        book_args = self.book_parser.parse_args()

        book_name = book_args['name']
        book_desc = book_args['description']
        book_section = book_args['section']
        book_qty = book_args['quantity']

        edited_book = Book(book_name, book_desc, book_section, book_qty)

        BOOKS[bookId] = edited_book.__dict__

        response = {'message': "Book:%s was updated" % bookId, 'data': BOOKS[bookId]}
        return response, 200

    def get(self, bookId):
        abort_if_book_does_not_exist(bookId)
        return BOOKS[bookId]

    def delete(self, bookId):
        abort_if_book_does_not_exist(bookId)
        del BOOKS[bookId]

        response = {'message': "Book:%s was deleted" % bookId, }
        return response, 204


class BooksResource(Resource):
    """
    Handles requests to :/api/v1/books
    """

    def __init__(self):
        super().__init__()

        self.book_parser = reqparse.RequestParser()

        self.book_parser.add_argument('name', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('description', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('section', type=string_validator, required=True,
                                      location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank ',
                                      location='json')

    def get(self):
        return BOOKS

    def post(self):
        book_args = self.book_parser.parse_args()

        book_name = book_args['name']
        book_desc = book_args['description']
        book_section = book_args['section']
        book_qty = book_args['quantity']

        abort_if_book_exists(book_name)

        book_id = len(BOOKS.keys()) + 1

        book_id = 'book%i' % book_id

        new_book = Book(book_name, book_desc, book_section, book_qty)
        BOOKS[book_id] = new_book.__dict__

        return BOOKS[book_id], 201
