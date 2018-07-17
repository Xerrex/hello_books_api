from unittest import main
import json

from .my_testbase import  TestBase
from app import create_app, db
from app.models import Book
from app.data_repo.user_repo import get_user_by_email


class BookModelCase(TestBase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.test_request_context():
            db.create_all()

            new_user = {
                "name": "Alex",
                "email": "alex@dev.com",
                "password": "123456789",
                "about_me": "mad skills you"
            }

            self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                             content_type='application/json')
            user = get_user_by_email("alex@dev.com")
            user.is_admin = True
            user.save()
            logins = {
                "email": "alex@dev.com",
                "password": "123456789"
            }

            self.client.post('/api/v1/auth/login', data=json.dumps(logins),
                             content_type='application/json')

            self.client.post('/api/v1/sections', data=json.dumps({"name":"tests"}),
                             content_type='application/json')

    def tearDown(self):
        self.client.post('/api/v1/auth/logout', content_type='application/json')

        with self.app.test_request_context():
            db.drop_all()
            self.client = None
            self.app = None

    def test_book_init_is_accurate(self):
        """
        Test that can initialize a book model
        """

        book1 = Book('chenco the dev', 'The struggles of getting mad skills', 'biography', 4)

        self.assertEqual(book1.name, 'chenco the dev')

    def test_list_all_books(self):
        """ Test that can fetch all books"""

        response = self.client.get('/api/v1/books')

        self.assert200(response)

    def test_book_creation(self):
        """Test that can create a book

        Ensure that a valid POST request to /api/v1/books
        will create a new book.
        """

        book_data = {
            "name": 'chenco the dev',
            "description": 'The struggles of getting mad skills',
            "section": "1",
            "quantity": "4"
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data),
                                    content_type='application/json')

        self.assert201(response)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Book Created - chenco the dev', data['message'])

    def test_book_creation_no_blanks(self):
        """Test that cannot create an empty book

        Confirm that an empty POST request to /api/v1/books to
        create a book fails with Bad request error
        """

        book_data = {}

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')
        self.assert400(response)

    def test_no_duplicates_in_creation(self):
        """Test that cannot create books with same name twice
        """

        book ={
            'name': 'chenco the dev',
            'description': 'The struggles of getting mad skills',
            'section': 1,
            'quantity': 4
        }

        self.client.post('/api/v1/books', data=json.dumps(book), content_type='application/json')

        response = self.client.post('/api/v1/books', data=json.dumps(book), content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert409(response)
        self.assertIn(book['name'], response_data['message'])

    def test_editing_of_book(self):
        """Test that can update book details

        Ensure that a valid PUT request to /api/v1/books/<bookId>
        edits a book.
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 1,
            'quantity': 42
        }

        self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        edited_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles to get blinding skills2',
            'section': 1,
            'quantity': 30
        }

        response = self.client.put('/api/v1/books/1', data=json.dumps(edited_book),
                                   content_type='application/json')

        self.assert200(response)

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(edited_book['quantity'], data['book_copies'])

    def test_editing_of_non_existent_book(self):
        """Test that cannot update non existent book

        Ensure that a valid PUT request to /api/v1/books/<bookId>
        to edit a book fails.
        """
        edited_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles to get blinding skills2',
            'section': 'biography',
            'quantity': 30
        }

        response = self.client.put('/api/v1/books/1000', data=json.dumps(edited_book),
                                   content_type='application/json')

        self.assert404(response)
        self.assertIn("Book:1000 doesn't exist", response.get_data(as_text=True))

    def test_for_empty_edit_request(self):
        """Test that cannot update book with empty data

        Ensure and empty data PUT Request to /api/v1/books/<bookId>
        will not update Book details.
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 1,
            'quantity': 42
        }

        edit_book_data = {}

        # create  book
        response = self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        # edit book
        response = self.client.put('/api/v1/books/1', data=json.dumps(edit_book_data),
                                   content_type='application/json')

        self.assert400(response)

    def test_book_info_accurate(self):
        """Test that can fetch a book

        Ensure that a valid Get request to /api/v1/books/<bookId>
        returns the correct book with the correct info
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 1,
            'quantity': 42
        }

        self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        response = self.client.get('/api/v1/books/1', content_type='application/json')

        self.assertTrue('chenco the dev2' in response.get_data(as_text=True))

    def test_response_if_book_doesnt_exist(self):
        """Test that cannot fetch book with non-existing Id

        Ensure that a valid GET request to /api/v1/books/<bookId>
        with bookId that does not exists fails with status code 404.
        """

        response = self.client.get('/api/v1/books/100', content_type='application/json')

        self.assert404(response)

    def test_delete_of_a_book(self):
        """Test that can delete a book

        Ensure that a valid DELETE request to /api/v1/books/<bookId>
        deletes a book
        """
        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 1,
            'quantity': 42
        }

        self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        response = self.client.get('/api/v1/books/1', content_type='application/json')
        self.assert200(response)

        response = self.client.delete('/api/v1/books/1', content_type='application/json')
        self.assert204(response)

    def test_deleting_book_doesnt_exist(self):
        """Test that cannot delete a non existent existent book

        Ensure that a Delete request to /api/v1/books/<bookId>
        returns NOT FOUND error when book with bookId does NOT exist.
        """

        response = self.client.delete('/api/v1/books/1', content_type='application/json')
        self.assert404(response)


if __name__ == '__main__':
    main(verbosity=2)