from flask import session
from flask_restful import Resource, reqparse, abort

from app.data_repo.book_repo import get_all_books, create_book, abort_if_book_exists, \
    get_book_by_id, abort_if_book_not_found, update_book, delete_book

from app.data_repo.user_repo import get_user_by_id

from app.utils.data_validators import string_validator


def check_active_session():
    if 'userID' not in session:
        msg = "Kindly Login first: Forbidden Action"
        link = "/api/v1/auth/login"
        abort(401, message=msg, login_link=link)


def check_if_admin(action):
    """Check that current logged in user is an admin"""
    user = get_user_by_id(session['userID'])
    if user.is_admin:
        return
    msg = f"Your not authorised to {action}"
    abort(401, message=msg)


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
        check_active_session()
        abort_if_book_not_found(bookId)
        book = get_book_by_id(bookId)
        return {
            "name": book.name,
            "description": book.description,
            "section": book.section.name,
            "quantity": book.quantity
        }, 200

    def put(self, bookId):
        check_active_session()

        check_if_admin("update a book")

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
            'book_name': book.name,
            'book_decription': book.description,
            'book_section': book.section.name,
            'book_copies': book.quantity
        }, 200

    def delete(self, bookId):
        check_active_session()
        check_if_admin("delete a book")

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
                                      help="Book Section is a Number & cannot be blank",
                                      location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank',
                                      location='json')

    def get(self):
        check_active_session()
        books = get_all_books()
        if not books:
            return {
                "message": "There are no books at the moment"
            }
        book_list = {}
        for book in books:
            book_list[book.id] = book.__repr__()

        return book_list, 200

    def post(self):
        check_active_session()
        check_if_admin("create a book")
        book_args = self.book_parser.parse_args()

        name = book_args['name']
        description = book_args['description']
        section = book_args['section']
        quantity = book_args['quantity']

        abort_if_book_exists(name)

        book = create_book(name, description, section, quantity)

        return {
            "message": 'Book Created - {}'.format(book.name)
        }, 201
