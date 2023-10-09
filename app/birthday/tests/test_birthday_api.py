"""
Tests fot birthday apis.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from birthday.serializers import BirthdaySerializer
from core.models import Birthday

BIRTHDAY_URL= reverse('birthday:birthday-list')

def create_birthday(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'name': "Example One",
        'email': "example@birthday.com",
        'date_of_birth': "1990-05-19",
    }

    defaults.update(params)

    birthday = Birthday.objects.create(user=user, **defaults)
    return birthday

class PublicBirthdayAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BIRTHDAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBirthdayAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'test1234',
        )

    def test_retrieve_birthday(self):
        """Test retrieve a list of birthdays."""
        self.client.force_authenticate(self.user)

        create_birthday(user=self.user)
        create_birthday(user=self.user, email='example2@birthday.com')

        res = self.client.get(BIRTHDAY_URL)

        birthdays = Birthday.objects.filter(user=self.user).order_by('-id')
        serializer = BirthdaySerializer(birthdays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_birthday_list_limited_to_user(self):
        """test list of birthdays is limited to authenticated user."""
        self.client.force_authenticate(self.user)

        other_user = get_user_model().objects.create_user(
            'seconduser@example.com',
            'test1234',
        )

        create_birthday(user=other_user, email='example3@birthday.com')
        create_birthday(user=self.user, email='example4@birthday.com')

        res = self.client.get(BIRTHDAY_URL)

        birthdays = Birthday.objects.filter(user=self.user).order_by('-id')
        serializer = BirthdaySerializer(birthdays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_creat_birthday(self):
        """Test creating a birthday"""
        self.client.force_authenticate(self.user)

        payload = {
            'name': 'example name',
            'email': 'example5@birthday.com',
            'date_of_birth': "1990-05-19",
        }

        res = self.client.post(BIRTHDAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        birthday = Birthday.objects.get(id=res.data['id'])
        self.assertEqual(birthday.name,payload['name'])
        self.assertEqual(birthday.email,payload['email'])
        self.assertEqual(birthday.user, self.user)


    def test_birthday_error_for_the_same_email(self):
        """Test error when the email already exists in the database"""

        self.client.force_authenticate(self.user)

        payload = {
            'name': 'example name',
            'email': 'example5@birthday.com',
            'date_of_birth': "1990-05-19",
        }
        self.client.post(BIRTHDAY_URL, payload)
        res = self.client.post(BIRTHDAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

