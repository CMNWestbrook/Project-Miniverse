import unittest

from import
from model import 


class MiniverseTests(unittest.TestCase):
    """Tests for Project Miniverse site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

     def test_homepage(self):
    result = self.client.get("/")
    self.assertIn("Welcome to Project Miniverse", result.data)


class MiniverseTestsDatabase(unittest.TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        """Stuff to do before every test"""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":

    unittest.main()
