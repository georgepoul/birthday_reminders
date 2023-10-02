from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_creat_user_with_email_successful(self):
        """Test creating a user with an email is successful"""

        email = "test@example.com"
        password = 'restpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXample.com', 'Test2@example.com'],
            ['TEST3@EXample.com', 'TEST3@example.com'],
            ['TEST4@EXample.COM', 'TEST4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "pass123@")
            self.assertEqual(user.email, expected)
