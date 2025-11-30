import unittest
from app import create_app, db, bcrypt
from app.users.models import User

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_page_loads(self):
        resp = self.client.get('/auth/register')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Register", resp.data)

    def test_login_page_loads(self):
        resp = self.client.get('/auth/login')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Login", resp.data)

    def test_user_is_saved_on_register(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678",
        }

        resp = self.client.post('/auth/register', data=form_data, follow_redirects=True)

        with self.app.app_context():
            user = User.query.filter_by(email="test@example.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")

    def test_login_and_logout(self):
        with self.app.app_context():
            pw_hash = bcrypt.generate_password_hash("123456").decode('utf-8')
            user = User(username="tester", email="t@test.com", password=pw_hash)
            db.session.add(user)
            db.session.commit()

        resp = self.client.post('/auth/login', data={
            "username": "tester",
            "password": "123456"
        }, follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
