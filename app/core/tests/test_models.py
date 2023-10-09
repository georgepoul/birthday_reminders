"""
Tests fot models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models


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

    def test_new_user_without_email_raises_value_error(self):
        """Test that creating a user without an email raises a ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','pass123')

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_birthday(self):
        """Test creating a recipe is successful."""

        user = get_user_model().objects.create_user(
            "test@example.com",
            "test1234",
        )

        birthday = models.Birthday.objects.create(
            user = user,
            name = "Test Name",
            email = "birthday@example.com",
            date_of_birth = "1990-05-19"
        )

        self.assertEqual(str(birthday), birthday.name)