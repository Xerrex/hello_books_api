"""Defines methods that manipulate borrow data.

This methods de-couples the Resources and the borrow model.
"""
from flask_restful import abort

from app.models import Borrow


def borrow_book(user_id, book_id):
    """ Borrow a book
    """

    borrow = Borrow(user_id, book_id)
    borrow.save()


def return_book(user_id, book_id):
    """ Return a borrowed book

    :param user_id:
        id of user borrowing the book
    :param book_id:
        id of book being borrowed
    """

    borrow = Borrow.query.filter_by(user_id=user_id, book_id=book_id, is_active=True).first()
    borrow.is_active = False
    borrow.save()


def abort_book_is_borrowed(user_id, book_id):
    """
    Abort when a user has already borrowed the same book
    """

    if Borrow.query.filter_by(user_id=user_id, book_id=book_id, is_active=True).first():
        abort(409, message="You already have the book borrowed")


def abort_book_is_not_borrowed(user_id, book_id):
    """ Abort when abook is not borrowed"""
    if not Borrow.query.filter_by(user_id=user_id, book_id=book_id, is_active=True).first():
        abort(403, message="You Need to borrow the book first")
