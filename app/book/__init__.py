from flask import Blueprint
from flask_restful import Api

from .views import BookResource, BookListResource

book_BP = Blueprint('book', __name__)

api = Api(book_BP)

api.add_resource(BookListResource, '/api/v1/books', endpoint="lists")
api.add_resource(BookResource, '/api/v1/books/<bookId>', endpoint="list")
