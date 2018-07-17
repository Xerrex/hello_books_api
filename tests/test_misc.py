"""
Test Operations of serving templates.
"""
from app import create_app
from .my_testbase import TestBase


class MiscCase(TestBase):

    def test_home_route(self):
        """Test the home route"""
        app = create_app("testing")
        client = app.test_client()

        response = client.get('/')
        self.assert200(response)