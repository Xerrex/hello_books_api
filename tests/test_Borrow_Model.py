"""Test Operations Involving the Borrow model

Operations include: initialisation, borrow_book, return_book
"""
from unittest import main
import json

from tests import TestBase
from app.models import Borrow
from app.models import USERS, BOOKS


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

        Ensure that only logged in user can borrow books.
        """
        book = {
            'book_id':'book1'
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert401(response)

    def test_borrowing_books_that_do_not_exist(self):
        """Test cannot borrow non existent book

        Ensure that a user can only borrow books that exist.
        """
        self.setup_things()

        book = {
            'book_id': 'book100'
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')
        self.assert404(response)

        self.reset_things()

    def test_user_can_borrow_book(self):
        """Test that a user can borrow a book

        Ensure that a valid POST request to /api/v1/users/books
        borrows book.
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

        book = {
            'book_id': book_id
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert201(response)

        self.reset_things()

    def test_duplicate_borrowing(self):
        """Test that no borrowing same book twice

        Ensure that a valid POST request to /api/v1/users/books
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

        book= {
            'book_id': book_id
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert409(response)

    def test_returning_book(self):
        """Test that use can return a book

        Ensure that valid PUT request to /api/v1/users/books/<bookId>
        returns a borrowed book.
        """
        self.setup_things()

        # create book
        book_data = {
            'name': 'chenco the dev34',
            'description': 'The struggles of getting mad skills34',
            'section': 'biography34',
            'quantity': 4
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')

        # book id
        book_id = len(BOOKS)
        book_id = 'book%i' % book_id

        book = {
            'book_id':book_id
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        response = self.client.put('/api/v1/users/books/{}'.format(book_id), content_type='application/json')
        self.assert200(response)

    def test_returning_book_not_borrowed(self):
        """ Test that user cannot return a book not borrowed

        Ensure that a valid PUT request to /api/v1/users/books/<bookId>
        to return a book not borrowed fails.
        """
        self.setup_things()

        respone = self.client.put('/api/v1/users/books/book2', content_type='application/json')

        self.assert403(respone)


if __name__ == '__main__':
    main(verbosity=2)