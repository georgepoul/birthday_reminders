"""
Tests for the user api.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

TEST_NAME = 'Test Name'
TEST_EMAIL = 'testuser@example.com'
TEST_PASS_VALID = 'test1234'
TEST_PASS_INVALID = '123'

def create_user(**params):
    """Creates and return a new user"""

    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        """Create a new user."""
        self.client = APIClient()


    def test_creat_success(self):
        """Test creating a user is successful."""

        payload = {
            'email': TEST_EMAIL,
            'password' : TEST_PASS_VALID,
            'name' : TEST_NAME,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""

        payload = {
            'email': TEST_EMAIL,
            'password': TEST_PASS_VALID,
            'name': TEST_NAME,
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""

        payload = {
            'email': TEST_EMAIL,
            'password': TEST_PASS_INVALID,
            'name': TEST_NAME,
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_creat_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            "email": TEST_EMAIL,
            "password": TEST_PASS_VALID,
            "name": TEST_NAME,
        }
        create_user(**user_details)
        payload = {
            "email": user_details['email'],
            "password": user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_creat_token_bad_credentials(self):
        """Test returns error if credentials invalid"""

        create_user(email=TEST_EMAIL, name= TEST_NAME, password=TEST_PASS_VALID)

        res = self.client.post(TOKEN_URL, email=TEST_EMAIL, password=TEST_PASS_INVALID)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creat_token_blank_password(self):
        """Test posting a blank password returns an error"""

        res = self.client.post(TOKEN_URL, email=TEST_EMAIL, password='')

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)