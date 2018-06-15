from flask_restful import Resource, reqparse

from app.data_repo.book_repo import get_all_books, create_book, abort_if_book_exists, \
    get_book_by_id, abort_if_book_not_found, update_book, delete_book

from app.utils.data_validators import string_validator


class BookResource(Resource):
    """
    Handles request to : /api/v1/books/<bookId>
    """

    def __init__(self):

        self.book_update_parser = reqparse.RequestParser()

        self.book_update_parser.add_argument('name', type=string_validator, required=True,
                                      location='json')

        self.book_update_parser.add_argument('description', type=string_validator, required=True,
                                      location='json')

        self.book_update_parser.add_argument('section', type=int, required=True,
                                             help="Book Section is a Number & cannot ne blank",
                                             location='json')

        self.book_update_parser.add_argument('quantity', type=int, required=True,
                                             help='Book quantity is a Number & cannot be blank ',
                                             location='json')

    def get(self, bookId):
        abort_if_book_not_found(bookId)
        return get_book_by_id(bookId).__dict__, 200

    def put(self, bookId):
        abort_if_book_not_found(bookId)
        book_args = self.book_update_parser.parse_args()

        name = book_args['name']
        description = book_args['description']
        section = book_args['section']
        quantity = book_args['quantity']

        book = update_book(bookId, name=name, description=description,
                                  section=section, quantity=quantity)

        return {
                   'message': "Book:%s was updated" % bookId,
                   'book': book.__dict__
               }, 200

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

        self.book_parser.add_argument('section', type=int, required=True, 
                                        help="Book Section is a Number & cannot ne blank", 
                                        location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank ',
                                      location='json')

    def get(self):
        books = get_all_books()

        book_list = {}
        for book in books:
            book_list[book.id] = book.__repr__()

        return book_list, 200

    def post(self):
        book_args = self.book_parser.parse_args()

        name = book_args['name']
        description = book_args['description']
        section = book_args['section']
        quantity = book_args['quantity']

        abort_if_book_exists(name)

        book = create_book(name, description, section, quantity)

        return {
                   "message": 'Book Created- {}'.format(book.name),
                   "book": book.__dict__
               }, 201
