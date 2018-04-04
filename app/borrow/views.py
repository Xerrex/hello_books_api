from flask import session
from flask_restful import Resource

from app.models import BORROWS, abort_if_same_book_already_borrowed
from app.models import Borrow
from app.models import abort_if_book_does_not_exist


class BorrowResource(Resource):

    def post(self, bookId):
        # check if user is logged in first
        if 'userID' not in session:
            return {"message": "Kindly Login first: Forbidden Action"}, 401
        abort_if_book_does_not_exist(bookId)

        user_id = session['userID']
        abort_if_same_book_already_borrowed(user_id, bookId)

        borrow_id = len(BORROWS) + 1

        borrow_id = 'borrow%i' % borrow_id
        new_borrow = Borrow(user_id, bookId)

        BORROWS[borrow_id] = new_borrow.__dict__
        response = {
            "message": "You have successfully Borrowed the book"
        }
        return response, 201
