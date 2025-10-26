import unittest
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_hi_user_page(self):
        response = self.client.get("/users/hi/John?age=30&role=User")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, John!", response.data)
        self.assertIn(b"30", response.data)
        self.assertIn(b"User", response.data)

    def test_user_page_redirect(self):
        response = self.client.get("/users/user", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to User Page", response.data)

    def test_admin_page_redirect(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Admin Page", response.data)

    def test_product_page(self):
        response = self.client.get("/products/Guitar?price=499")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product: Guitar", response.data)
        self.assertIn(b"499", response.data)

if __name__ == "__main__":
    unittest.main()
