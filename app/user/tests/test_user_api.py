from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """ Shortcut to create users"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    # separate between public API tests and private API tests
    """ Test the users API (public one)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful"""
        payload = {
            'email': 'firstuser@test.com',
            'password': 'testpass',
            'name': 'John Doe'
        }
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**result.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', result.data)

    def test_user_already_exists(self):
        """ Test creating an user that already exists """
        payload = {
            'email': 'firstuser@test.com',
            'password': 'testpass',
            'name': 'John Doe'
        }
        create_user(**payload)  # WOW!

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that password is secure enough (more than 5 characters)"""
        payload = {
            'email': 'firstuser@test.com',
            'password': 'shrt',
            'name': 'John Doe'
        }
        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@testtok.com', 'password': 'admin'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com', password='pass')
        payload = {'email': 'test@test.com', 'password': 'bad'}

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_user(self):
        """ Test that user is not created if the user does not exist """
        payload = {'email': 'test@testtok.com', 'password': 'admin'}
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required"""
        create_user(email='test@test.com', password='pass')
        res = self.client.post(
            TOKEN_URL,
            {'email': 'test@test.com', 'password': ''}
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
