"""Defines methods that manipulate borrow data.

This methods de-couples the Resources and the borrow model.
"""
from flask_restful import abort

from app.models import BORROWS, Borrow


def borrow_book(user_id, book_id):
    """ Borrow a book
    """
    borrow_id = len(BORROWS) + 1

    borrow_id = 'borrow%i' % borrow_id
    new_borrow = Borrow(user_id, book_id)

    BORROWS[borrow_id] = new_borrow.__dict__


def return_book(user_id, book_id):
    """ Return a borrowed book

    :param user_id:
        id of user borrowing the book
    :param book_id:
        id of book being borrowed
    """
    for borrow in BORROWS.values():
        if borrow['user_id'] == user_id and borrow['book_id'] == book_id:
            if borrow['is_active'] is True:
                borrow['is_active'] = False
                # return borrow
                return True
    return None


def abort_if_book_is_borrowed(user_id, book_id):
    """
    Abort when a user has already borrowed the same book
    """
    for borrow in BORROWS.values():
        if borrow['user_id'] == user_id and borrow['book_id'] == book_id:
            if borrow['is_active'] is True:
                abort(409, message="You already have the book borrowed")
