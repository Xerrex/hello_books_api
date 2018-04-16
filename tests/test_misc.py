"""
Test Operations of serving templates.
"""

from . import TestBase


class MiscCase(TestBase):

    def test_home_route(self):
        response = self.client.get('/')
        self.assert200(response)