"""Test Operations Involving the Borrow model

Operations include: initialisation, borrow_book, return_book
"""
from unittest import main
import json

from app import create_app, db
from app.models import Borrow
from app.data_repo.user_repo import get_user_by_email
from .my_testbase import TestBase


class BorrowModelCase(TestBase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.test_request_context():
            db.create_all()

            test_user = {
                "name": "Milka Borrows",
                "email": "milkaborrows@dev.com",
                "password": "milkyway12345",
                "about_me": "Welcome to the Milky way"
            }
            self.client.post('/api/v1/auth/register', data=json.dumps(test_user),
                             content_type='application/json')

            test_login = {
                "email": "milkaborrows@dev.com",
                "password": "milkyway12345"
            }
            user = get_user_by_email("milkaborrows@dev.com")
            user.is_admin = True
            user.save()

            self.client.post('/api/v1/auth/login', data=json.dumps(test_login),
                             content_type='application/json')

            self.client.post('/api/v1/sections', data=json.dumps({"name": "tests"}),
                             content_type='application/json')

            book_data = {
                "name": 'chenco the dev',
                "description": 'The struggles of getting mad skills',
                "section": "1",
                "quantity": "4"
            }
            self.client.post('/api/v1/books', data=json.dumps(book_data),
                             content_type='application/json')

    def tearDown(self):
        self.client.post('/api/v1/auth/logout', content_type='application/json')
        with self.app.test_request_context():
            db.drop_all()
            self.client = None
            self.app = None


    def test_borrow_book_initialisation(self):
        """Test that can initialise a borrow model

        Ensure that borrow book initialisation works.
        """
        borrow_bk = Borrow('user1','book1')

        self.assertTrue(borrow_bk.is_active == True)
        self.assertEqual('user1',borrow_bk.user_id)

    def test_only_logged_in_user_can_borrow_books(self):
        """ Test that user must login to borrow book

        Ensure that only logged in user can borrow books.
        """
        self.client.post('/api/v1/auth/logout', content_type='application/json')

        book = {
            'book_id':'1'
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert401(response)

    def test_borrowing_books_that_do_not_exist(self):
        """Test that user cannot borrow non existent book

        Ensure that a user can only borrow books that exist.
        """

        book = {
            'book_id': '100'
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book),
                                    content_type='application/json')
        self.assert404(response)


    def test_user_can_borrow_book(self):
        """Test that user can borrow a book

        Ensure that a valid POST request to /api/v1/users/books
        borrows book.
        """

        book = {
            'book_id': "1"
        }

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert201(response)

    def test_duplicate_borrowing(self):
        """Test that user cannot borrow same book twice

        Ensure that a valid POST request to /api/v1/users/books
        with the same bookId twice fails
        """

        book= {
            'book_id': "1"
        }

        self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        response = self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        self.assert409(response)

    def test_returning_book(self):
        """Test that user can return a book

        Ensure that valid PUT request to /api/v1/users/books/<bookId>
        returns a borrowed book.
        """

        book = {
            'book_id': "1"
        }

        self.client.post('/api/v1/users/books', data=json.dumps(book), content_type='application/json')

        response = self.client.put('/api/v1/users/books/1', content_type='application/json')
        self.assert200(response)

    def test_returning_book_not_borrowed(self):
        """ Test that user cannot return a book not borrowed

        Ensure that a valid PUT request to /api/v1/users/books/<bookId>
        to return a book not borrowed fails.
        """

        respone = self.client.put('/api/v1/users/books/1', content_type='application/json')

        self.assert403(respone)


if __name__ == '__main__':
    main(verbosity=2)