from flask_restful import Resource, reqparse

from app.data_repo.book_repo import get_all_books, create_book, abort_if_book_exists, \
    get_book_by_id, abort_if_book_not_found, update_book, delete_book

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
        abort_if_book_not_found(bookId)
        book_args = self.book_parser.parse_args()

        book_name = book_args['name']
        book_desc = book_args['description']
        book_section = book_args['section']
        book_qty = book_args['quantity']

        book = update_book(bookId, name=book_name, description=book_desc,
                                  section=book_section, quantity=book_qty)

        response = {'message': "Book:%s was updated" % bookId, 'data': book}
        return response, 200

    def get(self, bookId):
        abort_if_book_not_found(bookId)
        return get_book_by_id(bookId)

    def delete(self, bookId):
        abort_if_book_not_found(bookId)
        delete_book(bookId)

        response = {'message': "Book:%s was deleted" % bookId}
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
        return get_all_books()

    def post(self):
        book_args = self.book_parser.parse_args()

        book_name = book_args['name']
        book_desc = book_args['description']
        book_section = book_args['section']
        book_qty = book_args['quantity']

        abort_if_book_exists(book_name)

        new_book = create_book(book_name, book_desc, book_section, book_qty)

        return new_book.__dict__, 201
