from flask import session
from flask_restful import Resource, reqparse

from app.data_repo.book_repo import abort_if_book_not_found
from app.data_repo.borrow_repo import abort_if_book_is_borrowed, borrow_book, return_book

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
        abort_if_book_not_found(book_id)

        user_id = session['userID']
        abort_if_book_is_borrowed(user_id, book_id)


        borrow_book(user_id, book_id)

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

        if return_book(user_id, book_id):
            response = {"message":"Book has been successfully returned"}
            return response, 200

        # book needs to be borrowed first
        response = {"message": "You Need to borrow the book first"}
        return response, 403