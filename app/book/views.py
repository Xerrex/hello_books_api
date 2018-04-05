from flask_restful import Resource, reqparse

from app.models import BOOKS, abort_if_book_does_not_exist
from app.models import Book


class BookResource(Resource):
    """
    Handles request to : /api/v1/books/<bookId>
    """

    def __init__(self):
        super().__init__()

        self.book_parser = reqparse.RequestParser()

        self.book_parser.add_argument('name', type=str, required=True,
                                      help='Book name cannot be blank',
                                      location='json')

        self.book_parser.add_argument('description', type=str, required=True,
                                      help='Book description cannot be blank',
                                      location='json')

        self.book_parser.add_argument('section', type=str, required=True,
                                      help='Please select Book section, empty be blank',
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


class BookListResource(Resource):
    """
    Handles requests to :/api/v1/books
    """

    def __init__(self):
        super().__init__()

        self.book_parser = reqparse.RequestParser()

        self.book_parser.add_argument('name', type=str, required=True,
                                      help='Book name cannot be blank',
                                      location='json')

        self.book_parser.add_argument('description', type=str, required=True,
                                      help='Book description cannot be blank',
                                      location='json')

        self.book_parser.add_argument('section', type=str, required=True,
                                      help='Please select Book section, empty be blank',
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

        book_id = len(BOOKS.keys()) + 1

        book_id = 'book%i' % book_id

        new_book = Book(book_name, book_desc, book_section, book_qty)
        BOOKS[book_id] = new_book.__dict__

        return BOOKS[book_id], 201
