"""Defines methods that manipulate book data.

This methods decouple the Resources and the Book model.
"""
from flask_restful import abort
from app.models import BOOKS, Book


def create_book(name, description, section, quantity):
    """Create a new book"""
    book_id = len(BOOKS.keys()) + 1

    book_id = 'book%i' % book_id

    new_book = Book(name, description, section, quantity)
    BOOKS[book_id] = new_book.__dict__

    return new_book


def update_book(book_id, **kwargs):
    """Update Book details"""
    book = BOOKS[book_id]
    book['name'] = kwargs['name']
    book['description'] = kwargs['description']
    book['section'] = kwargs['section']
    book['quantity'] = kwargs['quantity']

    return book


def delete_book(book_id):
    """Delete a book"""
    del BOOKS[book_id]


def get_all_books():
    """ Retrieve all books
    """
    return BOOKS


def get_book_by_id(book_id):
    """Retrieve a book by id"""

    return BOOKS[book_id]


def get_book_by_name(book_name):
    """Retrieve a book by name"""
    for book in BOOKS.values():
        if book['name'] == book_name:
            return book
    return


def abort_if_book_exists(book_name):
    """Check if Book exists using the book name
    :param book_name:
    :return:
    """
    for book in BOOKS.values():
        name = book['name']
        if name.lower() == book_name.lower():
            abort(409, message="Book with the name already exists - {}".format(book_name))


def abort_if_book_not_found(book_id):
    """Check if a book exists using ID

    :param book_id:
    :return:
    """
    if book_id not in BOOKS:
        abort(404, message="Book:{} doesn't exist".format(book_id))
