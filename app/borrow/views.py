from flask import session
from flask_restful import Resource, reqparse

from app.models import BORROWS, abort_if_same_book_already_borrowed, get_active_borrow
from app.models import Borrow
from app.models import abort_if_book_does_not_exist
from app.utils.data_validators import string_validator


class BorrowResource(Resource):

    book_parser = reqparse.RequestParser()

    book_parser.add_argument('book_id', type=string_validator, required=True,
                                  location='json')

    def post(self):
        # check if user is logged in first
        if 'userID' not in session:
            return {"message": "Kindly Login first: Forbidden Action"}, 401

        book_args = self.book_parser.parse_args()
        book_id = book_args['book_id']
        abort_if_book_does_not_exist(book_id)

        user_id = session['userID']
        abort_if_same_book_already_borrowed(user_id, book_id)

        borrow_id = len(BORROWS) + 1

        borrow_id = 'borrow%i' % borrow_id
        new_borrow = Borrow(user_id, book_id)

        BORROWS[borrow_id] = new_borrow.__dict__
        response = {
            "message": "You have successfully Borrowed the book"
        }
        return response, 201


class ReturnResource(Resource):

    def put(self, book_id):

        # check if user is logged in first
        if 'userID' not in session:
            return {"message": "Kindly Login first: Forbidden Action"}, 401

        user_id = session['userID']

        # check if book is borrowed
        response = get_active_borrow(user_id, book_id)

        if response is not None:
            # return the book
            borrow = get_active_borrow(user_id, book_id)
            borrow['is_active'] = False
            response = {"message":"Book has been successfully returned"}
            return response, 200
        # book needs to be borrowed first
        response = {"message": "You Need to borrow the book first"}
        return response, 403