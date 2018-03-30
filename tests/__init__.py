from unittest import TestCase

from app import create_app


class TestBase(TestCase):
    """
    Defines the base requirements of a any tests
    """
    def setUp(self):
        self.app = create_app(config_env_name="testing_env")
        self.client = self.app.test_client()

    def tearDown(self):
        pass