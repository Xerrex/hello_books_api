from flask_restful import Resource, reqparse, abort

from app.models.book import Book
from app.models.user import User

BOOKS = {}  # stores Book models

USERS = {}  # stores User models

class BookResource(Resource):
    """
    Handles request to : /api/v1/books/<bookId>
    """

    def __init__(self):
        super().__init__()

        self.book_parser = reqparse.RequestParser()

        self.book_parser.add_argument('name', type=str, required=True,
                                      help='Book name cannot be blank', location='json')

        self.book_parser.add_argument('description', type=str, required=True,
                                      help='Book description cannot be blank', location='json')

        self.book_parser.add_argument('section', type=str, required=True,
                                      help='Please select Book section, empty be blank', location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank ', location='json')

    @staticmethod
    def abort_if_book_does_not_esist(book_id):
        if book_id not in BOOKS:
            abort(404, message="Book:{} doesn't exist".format(book_id))

    def put(self, bookId):
        self.book_args = self.book_parser.parse_args()

        book_name = self.book_args['name']
        book_desc = self.book_args['description']
        book_section = self.book_args['section']
        book_qty = self.book_args['quantity']

        edited_book = Book(book_name, book_desc, book_section, book_qty)

        BOOKS[bookId] = edited_book.__dict__

        response = {'message': "Book:%s was updated" % bookId, 'data': BOOKS[bookId]}
        return response, 200

    def get(self, bookId):
        self.abort_if_book_does_not_esist(bookId)
        return BOOKS[bookId]

    def delete(self, bookId):
        self.abort_if_book_does_not_esist(bookId)
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
                                      help='Book name cannot be blank', location='json')

        self.book_parser.add_argument('description', type=str, required=True,
                                      help='Book description cannot be blank', location='json')

        self.book_parser.add_argument('section', type=str, required=True,
                                      help='Please select Book section, empty be blank', location='json')

        self.book_parser.add_argument('quantity', type=int, required=True,
                                      help='Book quantity is a Number cannot be blank ', location='json')

    def get(self):
        return BOOKS

    def post(self):
        self.book_args = self.book_parser.parse_args()

        book_name = self.book_args['name']
        book_desc = self.book_args['description']
        book_section = self.book_args['section']
        book_qty = self.book_args['quantity']

        book_id = len(BOOKS.keys()) + 1

        book_id = 'book%i' % book_id

        new_book = Book(book_name, book_desc, book_section, book_qty)
        BOOKS[book_id] = new_book.__dict__

        return BOOKS[book_id], 201


class UserRegisterResource(Resource):
    """
    Resource handles user Login
    """
    def __init__(self):
        super().__init__()
        self.user_parser = reqparse.RequestParser()

        self.user_parser.add_argument('name', type=str, required=True,
                                      help='Name cannot be blank', location='json')

        self.user_parser.add_argument('email', type=str, required=True,
                                      help="Email cannot be empty", location='json')

        self.user_parser.add_argument('password', type=str, required=True,
                                      help="password cannot be empty", location='json')

        self.user_parser.add_argument('aboutme', type=str, location='json')

    def post(self):
        user_args = self.user_parser.parse_args()

        user_name = user_args['name']
        user_email = user_args['email']
        user_password = user_args['password']
        user_aboutme = user_args['aboutme']

        for id in USERS.keys():
            user = USERS[id]
            if user['email'] == user_email:
                return {'message': "User with that email already exists"}, 409

        new_user = User(user_name, user_email, user_password, user_aboutme)

        user_id = len(USERS) + 1

        user_id = 'user%i' % user_id

        USERS[user_id] = new_user.__dict__

        return {"message":"User registration was successful", "details":new_user.__repr__()}, 201