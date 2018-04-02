"""Test Operations Involving the Borrow model

Operations include: initialisation, borrow_book, return_book
"""
import json

from tests import TestBase
from app.models.borrow import Borrow
from app.views import USERS
from app.views import BOOKS


class BorrowModelCase(TestBase):

    def setup_things(self):
        """
        Creates a new User and log's them in
        """
        new_user = {
            "name": "Alex33",
            "email": "alex@dev.com33",
            "password": "12345678933",
            "aboutme": "mad skills you33"
        }

        # register user
        self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                         content_type='application/json')
        # log in
        login_credentials = {
            "email": "alex@dev.com33",
            "password": "12345678933"
        }

        self.client.post('/api/v1/auth/login', data=json.dumps(login_credentials),
                                    content_type='application/json')

    def reset_things(self):

        # get user id
        loggedIn_userid = len(USERS)
        loggedIn_userid = "user{}".format(loggedIn_userid)

        loggedIn_userid = {
            'userID': loggedIn_userid
        }

        response = self.client.post('/api/v1/auth/logout', data=json.dumps(loggedIn_userid),
                                    content_type='application/json')

    def test_borrow_book_initialisation(self):
        """Test that borrow model init is accurate

        Ensure that borrow book initialisation works.
        """
        borrow_bk = Borrow('user1','book1')

        self.assertTrue(borrow_bk.is_active == True)
        self.assertEqual('user1',borrow_bk.user_id)

    def test_only_logged_in_user_can_borrow_books(self):
        """ Test that login first to borrow book

        Ensure that only logged in user can login.
        """
        response = self.client.get('/api/v1/users/books/book1', content_type='application/json')

        self.assert401(response)

    def test_borrowing_books_that_do_not_exist(self):
        """Test that you cannot borrow non existent book

        Ensure that a user can only borrow books that exist.
        """
        self.setup_things()

        # borrow non existent book
        response = self.client.get('/api/v1/users/books/book100', content_type='application/json')

        self.assert404(response)

        self.reset_things()

    def test_user_can_borrow_book(self):
        """Test that a user can borrow a book

        Ensure that a valid GET request to /api/v1/users/books/<bookId>
        borrows book with id <bookId>
        """
        self.setup_things()

        # create book
        book_data = {
            'name': 'chenco the dev33',
            'description': 'The struggles of getting mad skills33',
            'section': 'biography33',
            'quantity': 4
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')

        # book id
        book_id = len(BOOKS)
        book_id = 'book%i' % book_id
        response = self.client.get('/api/v1/users/books/{}'.format(book_id), content_type='application/json')

        self.assert201(response)

        self.reset_things()

    def test_duplicate_borrowing(self):
        """Test that no borrowing same book twice

        Ensure that a valid GET request to /api/v1/users/books/<bookId>
        with the same bookId twice fails
        """
        self.setup_things()

        # create book
        book_data = {
            'name': 'chenco the dev333',
            'description': 'The struggles of getting mad skills333',
            'section': 'biography333',
            'quantity': 43
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')

        # book id
        book_id = len(BOOKS)
        book_id = 'book%i' % book_id

        response = self.client.get('/api/v1/users/books/{}'.format(book_id), content_type='application/json')

        response = self.client.get('/api/v1/users/books/{}'.format(book_id), content_type='application/json')

        self.assert409(response)


