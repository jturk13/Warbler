import os
from unittest import TestCase

from models import db, User, Message, Follows

# Set the environmental variable to use a different database for tests
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Import the Flask app after setting the environmental variable
from app import app

# Create the tables for testing
db.create_all()


class UserModelTestCase(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up test data after each test."""
        db.session.rollback()

    def test_user_repr(self):
        """Test __repr__ method of User model."""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(repr(u), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_user_following(self):
        """Test user can follow other users."""
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        user1.following.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))