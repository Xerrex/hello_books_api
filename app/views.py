from flask_restful import Resource, reqparse

from app.models import Book

BOOKS = {
    'book1': {'name': 'welcome to flask'},
    'book2': {'name': 'Welcome to flask API DIY'},
    'book3': {'name': 'Welcome to flask flask-restful'},
}

books_list=[]


class BookResource(Resource):



    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('name', type=str, required=True,
                                   help='Book name cannot be blank', location='json')

        self.reqparse.add_argument('description', type=str, required=True,
                                   help='Book description cannot be blank', location='json')

        self.reqparse.add_argument('section', type=str, required=True,
                                   help='Please select Book section, empty be blank', location='json')

        self.reqparse.add_argument('quantity', type=int, required=True,
                                   help='Book quantity is a Number cannot be blank ', location='json')

        super(BookResource, self).__init__()

    def get(self):
        return BOOKS

    def post(self):
        args = self.reqparse.parse_args()
        name = args['name']
        description = args['description']
        section = args['section']
        quantity = args['quantity']


        #check if book exists in list

        for book in books_list:
            if book.name == name:
                return {'message': 'A Book with that name already exists'}, 409
            else:
                new_book = Book(name=name, description=description, section=section, quantity=quantity)
                books_list.append(new_book)
                return {'message': 'Book name: %s has been succesfully created' % new_book.name}, 200
