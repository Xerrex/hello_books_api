from flask import Blueprint
from flask_restful import Api

from .views import BorrowResource, ReturnResource

borrow_BP = Blueprint('borrow', __name__, url_prefix='/api/v1/users')

api = Api(borrow_BP)

api.add_resource(BorrowResource, '/books', endpoint='borrow book')
api.add_resource(ReturnResource, '/books/<book_id>', endpoint='return book')