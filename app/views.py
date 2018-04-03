from flask import session
from flask_restful import Resource, reqparse, abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.book import Book
from app.models.user import User
from app.models.borrow import Borrow

BOOKS = {}  # stores Book models

USERS = {}  # stores User models

BORROWS = {}  # stored Borrow models


def get_user_id(email):
    for user_id in USERS.keys():
        user_email = USERS[user_id]['email']
        if user_email == email:
            return user_id
    return


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
    def abort_if_book_does_not_exist(book_id):
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
        self.abort_if_book_does_not_exist(bookId)
        return BOOKS[bookId]

    def delete(self, bookId):
        self.abort_if_book_does_not_exist(bookId)
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


class UserLoginResource(Resource):
    """
    Handle login request
    """
    def __init__(self):
        super().__init__()

        self.login_parser = reqparse.RequestParser()

        self.login_parser.add_argument('email', type=str, required=True,
                                       help="Email cannot be empty", location='json')

        self.login_parser.add_argument('password', type=str, required=True,
                                       help="password cannot be empty", location='json')

    def post(self):
        login_args = self.login_parser.parse_args()

        user_email = login_args['email']
        user_password = login_args['password']

        for userID in USERS.keys():
            user = USERS[userID]
            if user['email'] == user_email and check_password_hash(user['password'], user_password):
                if 'userID' not in session:
                    session['userID'] = userID
                    return {"message": "Welcome back {}".format(user['name'])}, 200

                return {"message": "Your already logged in {}".format(user['name'])}, 409

        return{"message": "Invalid email or password. Makes sure to register first"}, 401


class UserLogoutResource(Resource):

    logout_parser = reqparse.RequestParser()
    logout_parser.add_argument('userID', type=str, required=True,
                               help="Forbidden Request", location='json')

    def post(self):
        logout_arg = self.logout_parser.parse_args()
        user_id = logout_arg['userID']

        if 'userID' not in session:
            return {"message":"Kindly Login first: Forbidden Action"}, 403

        session.pop('userId', None)

        user_name = USERS[user_id]['name']
        return {"message": "You have been successfully logged out {}".format(user_name)}, 200


class UserResetPasswordResource(Resource):

    reset_pass_parser = reqparse.RequestParser()

    reset_pass_parser.add_argument('email', type=str, required=True,
                                   help='Email cannot be empty', location='json')

    reset_pass_parser.add_argument('reset_token', type=str, location='json')
    reset_pass_parser.add_argument('new_password', type=str, location='json')

    def post(self):

        reset_pass_args = self.reset_pass_parser.parse_args()
        user_email = reset_pass_args['email']
        user_token = reset_pass_args['reset_token']
        new_password = reset_pass_args['new_password']

        # generate token just email was passed.
        if not user_token:
            user_id = get_user_id(user_email)
            if user_id is None:
                response = {
                    'message': "Your email was Not found. Please register first to reset password"
                }
                return response, 404

            # gen token
            token = User.generate_token_value(user_email)
            response = {
                'message': 'Token generated successfully.Use the token value to reset your password',
                'reset_token': token
            }

            return response, 201

        # verify token value and take new password
        elif not new_password:
            response = {
                'message': "New password is required to reset password"
            }

            return response, 400

        # verify token & reset set password: email, reset_token, new_password are set
        else:
            user_email_token = User.verify_token_value(user_token)

            if user_email_token is None:
                response = {
                    'message': 'Password Reset failed'
                }
                return response, 401

            for userId in USERS.keys():
                user_email_ds = USERS[userId]['email'].lstrip('@')
                if user_email_ds == user_email_token:
                    USERS[userId]['password'] = generate_password_hash(new_password)

                    response = {
                        'message': 'Your password has been successfully reset'
                    }
                    return response, 200
            response = {
                'message': "Something Went wrong with password reset"
            }
            return response, 401


class BorrowResource(Resource):

    def post(self, bookId):
        
        # check if user is logged in first
        if 'userID' not in session:
            return {"message":"Kindly Login first: Forbidden Action"}, 401
        BookResource.abort_if_book_does_not_exist(bookId)

        user_id = session['userID']
        self.abort_if_same_book_already_borrowed(user_id, bookId)

        borrow_id = len(BORROWS) + 1

        borrow_id = 'borrow%i' % borrow_id
        new_borrow = Borrow(user_id, bookId)

        BORROWS[borrow_id] = new_borrow.__dict__
        response = {
            "message": "You have successfully Borrowed the book"
        }
        return response, 201

    @staticmethod
    def abort_if_same_book_already_borrowed(user_id, book_id):
        """
        Abort when a user has already borrowed the same book
        """

        for borrow in BORROWS.values():
            if borrow['user_id'] == user_id and borrow['book_id'] == book_id:
                if borrow['is_active'] is True:
                    abort(409, message="You already have the book borrowed")
        return None









