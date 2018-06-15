"""Defines methods that manipulate book data.

This methods decouple the Resources and the Book model.
"""
from flask_restful import abort
from app.models import Book, Section


def create_book(name, description, section, quantity):
    """Create a new book"""

    book = Book(name, description, section, quantity)
    book.save()

    return book


def update_book(book_id, **kwargs):
    """Update Book details"""

    book = Book.query.get(book_id)
    book.name = kwargs['name'].lower()
    book.description = kwargs['description']
    book.section_id = kwargs['section']
    book.quantity = kwargs['quantity']
    book.save()

    return book


def delete_book(book_id):
    """Delete a book"""
    book = Book.query.get(book_id)
    book.delete()


def get_all_books():
    """ Retrieve all books"""

    return Book.query.all()


def get_book_by_id(book_id):
    """Retrieve a book by id"""

    return Book.query.get(book_id)


def abort_if_book_exists(name):
    """Check if Book exists using the book name

    :param name:
    """
    if Book.query.filter_by(name=name.lower()).first():
        abort(409, message="Book with the name already exists - {}".format(name))


def abort_if_book_not_found(book_id):
    """Check if a book exists using ID

    :param book_id:
    :return:
    """
    if type(book_id) is not int:
        abort(404, message="Book:{} doesn't exist".format(book_id))

    if not Book.query.get(book_id):
        abort(404, message="Book:{} doesn't exist".format(book_id))

# ################################ Section ##################################


def create_section(name):
    """Create a new book section"""

    book_section = Section(name)
    book_section.save()
    return book_section


def get_book_sections():
    """Fetch all book sections"""

    return Section.query.all()


def abort_if_book_section_found(name):
    """Abort if a book is found"""

    if Section.query.filter_by(name=name.lower()).first():
        abort(409, message="{} Book Section already exists".format(name.lower()))
