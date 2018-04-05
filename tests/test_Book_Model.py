"""
Test  CRUD operation on that book model
"""
import json

from tests import TestBase
from app.models import Book

from app.models import BOOKS


class BookModelCase(TestBase):

    def test_book_init_is_accurate(self):
        """
        Test that Book initialization via the model works
        """

        book1 = Book('chenco the dev', 'The struggles of getting mad skills', 'biography', 4)

        self.assertEqual(book1.name, 'chenco the dev')

    def test_book_creation(self):
        """Test Book creation

        Ensure that a valid POST request to /api/v1/books
        will create a new book.
        """

        book_data = {
            'name': 'chenco the dev',
            'description': 'The struggles of getting mad skills',
            'section': 'biography',
            'quantity': 4
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')

        self.assert201(response)
        self.assertIn(book_data['name'], response.get_data(as_text=True))

    def test_book_creation_no_blanks(self):
        """Test empty book creation request

        Confirm that an empty POST request to /api/v1/books to
        create a book fails with Bad request error
        """

        book_data = {}

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')
        self.assert400(response)

    def test_editing_of_book(self):
        """Test that a editing of a book is possible

        Ensure that a valid PUT request to /api/v1/books/<bookId>
        edits a book.
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography',
            'quantity': 42
        }

        response = self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        edited_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles to get blinding skills2',
            'section': 'biography',
            'quantity': 30
        }

        response = self.client.put('/api/v1/books/book1', data=json.dumps(edited_book),
                                   content_type='application/json')

        self.assert200(response)

    def test_editing_of_non_existent_book(self):
        """Test that editing of non existent book

        Ensure that a valid PUT request to /api/v1/books/<bookId>
        to edit a book fails.
        """
        edited_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles to get blinding skills2',
            'section': 'biography',
            'quantity': 30
        }

        response = self.client.put('/api/v1/books/book5000', data=json.dumps(edited_book),
                                   content_type='application/json')
        response_data = response
        self.assert404(response)
        self.assertIn("Book:book5000 doesn't exist", response.get_data(as_text=True))

    def test_for_empty_edit_request(self):
        """Test that empty data to book edit request

        Ensure and empty data PUT Request to /api/v1/books/<bookId>
        will not update Book details.
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography2',
            'quantity': 42
        }

        edit_book_data = {}

        # create  book
        response = self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        # edit book
        response = self.client.put('/api/v1/books/book1', data=json.dumps(edit_book_data),
                                   content_type='application/json')

        self.assert400(response)

    def test_book_info_accurate(self):
        """Test that correct book is returned

        Ensure that a valid Get request to /api/v1/books/<bookId>
        returns the correct book with the correct info
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography',
            'quantity': 42
        }

        # check books available
        book_id = len(BOOKS)

        self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        book_id = book_id+1

        response = self.client.get('/api/v1/books/book%s' %book_id, content_type='application/json')

        self.assertTrue('chenco the dev2' in response.get_data(as_text=True))

    def test_response_if_book_doesnt_esist(self):
        """Test that getting a book with non-existing Id

        Ensure that a valid GET request to /api/v1/books/<bookId>
        with bookId that does not exists fails with status code 404.
        """

        response = self.client.get('/api/v1/books/book100', content_type='application/json')

        self.assert404(response)

    def test_delete_of_a_book(self):
        """Test deleting a book

        Ensure that a valid DELETE request to /api/v1/books/<bookId>
        deletes a book
        """

        # get id of the last created book
        book_id = len(BOOKS)

        response = self.client.delete('/api/v1/books/book%s' % book_id, content_type='application/json')
        self.assert204(response)

    def test_deleting_book_doesnt_exist(self):
        """Test deleting a non existent

        Ensure that a Delete request to /api/v1/books/<bookId>
        returns NOT FOUND error when book with bookId does NOT exist.
        """

        response = self.client.delete('/api/v1/books/100000', content_type='application/json')
        self.assert404(response)
