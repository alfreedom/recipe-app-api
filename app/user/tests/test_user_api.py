from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_USER_TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTest(TestCase):
    """Test the public user API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            'email': 'testapiuser@test.com',
            'password': 'Test123',
            'name': 'testuser'
        }

    def test_create_valid_user_success(self) -> None:
        """Test creatin user with payload is successful"""
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload.get('password')))
        self.assertNotIn('password', response.data)

    def test_user_exists(self) -> None:
        """Test creating a user that already exists fails"""
        create_user(**self.payload)

        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self) -> None:
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'testapiuser@test.com',
            'password': 'pw',
            'name': 'testuser'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload.get('email')
        ).exists()
        self.assertFalse(user_exists)

    def test_user_create_token(self):
        """Creates a user token and return it"""
        create_user(**self.payload)
        payload = {
            'email': 'testapiuser@test.com',
            'password': 'Test123',
        }

        response = self.client.post(CREATE_USER_TOKEN_URL, payload)
        print(response.data.get('token'))
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_token_wrong_email(self):
        """Test create a token with invalid email"""
        create_user(**self.payload)
        wrong_payload = {
            'email': 'anotheruser@test.com',
            'password': 'Test123'
        }
        response = self.client.post(CREATE_USER_TOKEN_URL, wrong_payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_token_wrong_password(self):
        """Test create a token with invalid password"""
        create_user(**self.payload)
        wrong_payload = {
            'email': 'testapiuser@test.com',
            'password': 'pw'
        }
        response = self.client.post(CREATE_USER_TOKEN_URL, wrong_payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_token_empty_email(self):
        """Test create a user token with empty email"""
        create_user(**self.payload)
        wrong_payload = {
            'email': '',
            'password': 'Test123'
        }
        response = self.client.post(CREATE_USER_TOKEN_URL, wrong_payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_token_empty_password(self):
        """Test create a user token with empty password"""
        create_user(**self.payload)
        wrong_payload = {
            'email': 'testapiuser@test.com',
            'password': ''
        }
        response = self.client.post(CREATE_USER_TOKEN_URL, wrong_payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
