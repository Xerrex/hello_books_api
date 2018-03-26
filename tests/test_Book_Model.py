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
        book1 = Book('chenco the dev','The struggles of getting mad skills', 'biography', 4)

        self.assertEqual(book1.name, 'chenco the dev')

    def test_book_creation(self):

        book_data = {
            'name':'chenco the dev',
            'description':'The struggles of getting mad skills',
            'section':'biography',
            'quantity':4
        }

        response = self.client.post('/api/books', data=json.dumps(book_data),  content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.assertIn(book_data['name'], response.get_data(as_text=True))



    def test_book_creation_no_blanks(self):
        book_data ={}

        response = self.client.post('/api/books', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_no_creation_of_duplicates(self):
        book_data1 ={
            'name':'chenco the dev',
            'description':'The struggles of getting mad skills',
            'section':'biography',
            'quantity':4
        }

        response = self.client.post('/api/books', data=json.dumps(book_data1), content_type='application/json')
        self.assertEqual(response.status_code, 409)




if __name__ == '__main__':
    unittest.main(verbosity=2)