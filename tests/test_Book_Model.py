'''
Test that book creation is accurate
'''
import unittest
import json

from app import create_app
from app.models import Book


class BookModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_env_name="testing_env")
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_book_init_is_accurate(self):
        book1 = Book('chenco the dev', 'The struggles of getting mad skills', 'biography', 4)

        self.assertEqual(book1.name, 'chenco the dev')

    def test_book_creation(self):
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
        book_data = {}

        response = self.client.post('/api/v1/books', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_editing_of_book(self):
        '''
        Test that a editing of a book is possible
        '''

        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography',
            'quantity': 42
        }

        response = self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        edited_book ={
            'name': 'chenco the dev2',
            'description': 'The struggles to get blinding skills2',
            'section': 'biography',
            'quantity': 30
        }

        response = self.client.put('/api/v1/books/book1', data=json.dumps(edited_book),
                                   content_type='application/json')

        self.assertTrue(response.status_code == 200)

    def test_for_empty_edit_request(self):
        '''
        Ensure that empty data to Put Request will not update Book details.
        '''
        new_book = {
            'name': 'chenco the dev2',
            'description': 'The struggles of getting mad skills2',
            'section': 'biography2',
            'quantity': 42
        }

        edit_book_data = {}

        #create  book
        response = self.client.post('/api/v1/books', data=json.dumps(new_book), content_type='application/json')

        #edit book
        response = self.client.put('/api/v1/books/book1', data=json.dumps(edit_book_data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)




if __name__ == '__main__':
    unittest.main(verbosity=2)
