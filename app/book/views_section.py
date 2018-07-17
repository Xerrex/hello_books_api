from flask import session
from flask_restful import Resource, reqparse, abort

from app.utils.data_validators import string_validator
from app.data_repo.book_repo import create_section, abort_if_book_section_found, get_book_sections
from app.data_repo.user_repo import  get_user_by_id

def check_active_session():
    if 'userID' not in session:
        msg = "Kindly Login first: Forbidden Action"
        link = "/api/v1/auth/login"
        abort(401, message=msg, login_link=link)


def check_if_admin(action):
    """Check that current logged in user is an admin"""
    user = get_user_by_id(session['userID'])
    if user.is_admin:
        return
    msg = f"Your not authorised to {action}"
    abort(401, message=msg)


class SectionResource(Resource):
    """Class handles the /api/v1/section/<section_id> endpoint.

    The following Http verbs are handled: PUT, GET, DELETE.
    """
    def get(self, section_id):
        pass

    def put(self, section_id):
        pass

    def delete(self, section_id):
        pass


class SectionsResource(Resource):
    """Class handles the /api/v1/sections endpoint

    The following Http verbs are handled: GET, POST.
    """
    section_parser = reqparse.RequestParser()
    section_parser.add_argument('name', type=string_validator, required=True,
                                location='json')

    def get(self):
        check_active_session()
        sections = get_book_sections()
        if not sections:
            return {
                "message": "There are no book sections at the moment"
            }
        book_sections = {}

        for section in sections:
            book_sections[section.id] = section.__repr__()

        return book_sections, 200

    def post(self):
        """ handles the POST Http request"""
        check_active_session()
        check_if_admin("create a book section")

        section_args = self.section_parser.parse_args()
        name = section_args['name']

        abort_if_book_section_found(name)
        book_section = create_section(name)

        return {
                   "message":"The '{}' book Section was created".format(book_section.name)
               }, 201