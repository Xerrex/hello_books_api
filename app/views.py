from flask_restful import Resource


BOOKS = {
    'book1': {'name': 'welcome to flask'},
    'book2': {'name': 'Welcome to flask API DIY'},
    'book3': {'name': 'Welcome to flask flask-restful'},
}

class Book(Resource):
    def get(self):
        return BOOKS

    def post(self):
        pass