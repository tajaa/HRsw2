import unittest

from app import app  # Make sure this import matches your project structure


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Employee List", response.get_data(as_text=True))
        self.assertIn("Add New Employee", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
