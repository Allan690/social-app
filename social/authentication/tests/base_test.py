import uuid

from rest_framework.test import APITestCase, APITransactionTestCase
from rest_framework.reverse import reverse as api_reverse
from social.authentication.models import User


class TestBaseCase(APITransactionTestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.signup_url = api_reverse('social.authentication:user-registration')
        self.login_url = api_reverse('social.authentication:user-login')
        self.retrieve_update_user_url = api_reverse(
            'social.authentication:user-retrieve-update')
        self.valid_user = {
            'username': 'mary',
            'email': 'mm@mm.com',
            'password': 'Pass@123'
        }

        self.valid_existing_user = {
            'username': 'ma1ry',
            'email': 'mm@mm.com',
            'password': 'Pass@123'
        }

        self.invalid_user_with_missing_fields = {
            'email': 'mm@mm.com'
        }

        self.invalid_user_with_empty_fields = {
            'email': '',
            'password': 'Pass@123',
        }

        self.user_two = User.objects.create_user(
            email='jane1@doe.com',
            password='janeDoe@123')

        self.valid_user_login_details = {
            'email': 'jane1@doe.com',
            'password': 'janeDoe@123'
        }

        self.invalid_user_login_details = {
            'email': 'janee@doe.com',
            'password': 'janeDoe@123'
        }

        self.valid_user_two = {
            'username': 'Doe123',
            'password': 'Jan5432@123',
        }

    def signup_user(self):
        """
        Signup user successfully
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')
        return response

    def signup_user_two(self):
        """
        successfully signup user
        """
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        return User.objects.get(email=self.valid_user['email'])

    def signup_user_with_missing_fields(self):
        """
        Signup user with missing fields
        """
        response = self.client.post(
            self.signup_url, self.invalid_user_with_missing_fields, format='json')

        return response

    def signup_user_with_empty_fields(self):
        """
        Signup user with empty fields
        """
        response = self.client.post(
            self.signup_url,
            self.invalid_user_with_empty_fields, format='json'
        )
        return response

    def signup_existing_user(self):
        """
        Signup existing user
        """
        self.signup_user()
        response = self.client.post(
            self.signup_url, self.valid_existing_user, format='json'
        )
        return response

    def login_user_successfull(self):
        """
        method to login user
        """
        response = self.client.post(
            self.login_url, self.valid_user_login_details, format='json'
        )
        return response

    def login_user_fails(self):
        """
        method to try login a user with invalid data
        """
        response = self.client.post(
            self.login_url, self.invalid_user_login_details, format='json'
        )
        return response

    def activated_user(self):
        """
        create an active user
        """
        user = self.signup_user_two()
        user.save()
        return user
