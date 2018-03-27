from flask_restful import Resource, reqparse

from app.models import Book

BOOKS = {
    'book1': {'name': 'welcome to flask'},
    'book2': {'name': 'Welcome to flask API DIY'},
    'book3': {'name': 'Welcome to flask flask-restful'},
}


class BookListResource(Resource):

    def get(self):
        return BOOKS
