import unittest
from app import create_app, db
from app.posts.models import Post


class PostBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        response = self.client.post(
            "/post/create",
            data={
                "title": "Test Title",
                "content": "Some test content",
                "category": "TECH",
                "author": "John",
                "is_active": True
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post created successfully!", response.data)

        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertIsNotNone(post)
            self.assertEqual(post.title, "Test Title")

    def test_list_posts(self):
        with self.app.app_context():
            post = Post(title="List Test", content="abc", category="NEWS")
            db.session.add(post)
            db.session.commit()

        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"List Test", response.data)

    def test_show_post(self):
        with self.app.app_context():
            post = Post(title="Detail Post", content="details", category="OTHER")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.get(f"/post/{post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail Post", response.data)
        self.assertIn(b"details", response.data)

    def test_update_post(self):
        with self.app.app_context():
            post = Post(title="Old Title", content="Old content", category="TECH")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/update",
            data={
                "title": "New Title",
                "content": "Updated content",
                "category": "NEWS",
                "author": "Admin",
                "is_active": True
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post updated successfully!", response.data)

        with self.app.app_context():
            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.title, "New Title")
            self.assertEqual(updated.content, "Updated content")

    def test_delete_post(self):
        with self.app.app_context():
            post = Post(title="Delete Me", content="bye", category="OTHER")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post deleted successfully!", response.data)

        with self.app.app_context():
            deleted = db.session.get(Post, post_id)
            self.assertIsNone(deleted)


if __name__ == "__main__":
    unittest.main()
