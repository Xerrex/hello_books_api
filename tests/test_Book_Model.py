"""
Test  CRUD operation on that book model
"""
from unittest import main
import json

from tests import TestBase
from app.models.book import Book

from app.views import BOOKS


class BookModelCase(TestBase):

    def test_book_init_is_accurate(self):
        """
        Test that Book initialization via the model works
        """

        book1 = Book('chenco the dev', 'The struggles of getting mad skills', 'biography', 4)

        self.assertEqual(book1.name, 'chenco the dev')

    def test_book_creation(self):
        """
        Test that a valid POST request to /api/v1/books
        will create a new book
        """

        book_data = {
            'name': 'chenco the dev',
            'description': 'The struggles of getting mad skills',
            'section': 'biography',
            'quantity': 4
        }

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(book_data['name'], response.get_data(as_text=True))

    def test_book_creation_no_blanks(self):
        """
        Test that a empty POST request to /api/v1/books to
        create a book failsith Bad request error
        """

        book_data = {}

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_editing_of_book(self):
        """
        Test that a editing of a book is possible
        via PUT request to /api/v1/books/<bookId>
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

        self.assertTrue(response.status_code == 200)

    def test_for_empty_edit_request(self):
        """
        Test that empty data to PUT Request to /api/v1/books/<bookId>
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

        self.assertEqual(response.status_code, 400)

    def test_book_info_accurate(self):
        """
        Test that the correct book is returned on
        Get request to /api/v1/books/<bookId>
        """

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography',
            'quantity': 42
        }

        # check books avaible
        book_id = len(BOOKS)

        self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        book_id = book_id+1

        response = self.client.get('/api/v1/books/book%s' %book_id, content_type='application/json')

        self.assertTrue('chenco the dev2' in response.get_data(as_text=True))

    def test_response_if_book_doesnt_esist(self):
        """
        Test that a GET request to /api/v1/books/<bookId>
        with bookId that does not exists fails with status code 404.
        """

        response = self.client.get('/api/v1/books/book100', content_type='application/json')

        self.assertTrue(response.status_code == 404)

    def test_delete_of_a_book(self):
        """
        Test that a valid DELETE request to /api/v1/books/<bookId>
        deletes a book
        """

        # delete book created from previous test: test_book_info_accurate

        book_id = len(BOOKS)
        response = self.client.delete('/api/v1/books/book%s' % book_id, content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_deleting_book_doesnt_exist(self):
        """
        Test that Delete request to /api/v1/books/<bookId>
        returns NOT FOUND error when book with bookId does NOT exist.
        """

        response = self.client.delete('/api/v1/books/100000', content_type='application/json')
        self.assertTrue(response.status_code == 404 )


if __name__ == '__main__':
    main(verbosity=2)
