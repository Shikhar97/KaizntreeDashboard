from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_api.models import User


class AuthApiTests(APITestCase):
    def test_create_account(self):
        """
        Register a new user.
        """
        url = reverse('register')
        data = {
            'email': 'testcase1@gmail.com',
            'password1': 'pass$12345',
            'password2': 'pass$12345'
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('username' in response_data)
        self.assertEqual(response_data['username'], data['email'])

        # Ensure password is not returned
        self.assertFalse('password' in response_data)

    def test_login_account(self):
        """
        Login with a user.
        """
        user = User.objects.create_user(username='testcase2@gmail.com', password='pass$12345')
        url = reverse('login')
        data = {
            'username': 'testcase2@gmail.com',
            'password': 'pass$12345',
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue('username' in response_data)
        self.assertEqual(response_data['username'], data['email'])

        self.assertTrue('access_token' in response_data)
        self.assertTrue('refresh_token' in response_data)

        # Ensure password is not returned
        self.assertFalse('password' in response_data)

    def test_login_invalid_username(self):
        """
        Login fails with invalid username.
        """
        url = reverse('login')
        data = {
            'username': 'testcase3@gmail.com',
            'password': 'pass$12345',
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_fail(self):
        """
        Login fails with wrong password.
        """
        url = reverse('login')
        data = {
            'username': 'testcase4@gmail.com',
            'password': 'pass$12345',
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


