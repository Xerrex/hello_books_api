from flask import Blueprint
from flask_restful import Api

from .views import BookResource, BooksResource

book_BP = Blueprint('book', __name__)

api = Api(book_BP)

api.add_resource(BooksResource, '/api/v1/books', endpoint="books")
api.add_resource(BookResource, '/api/v1/books/<bookId>', endpoint="book")
