import json
import time
from unittest.mock import patch, Mock

from rest_framework import status
from .base_test import TestBaseCase
from .test_retrieve_user import MockThread
from ...helpers.constants import SIGNUP_SUCCESS_MESSAGE


class RegistrationTest(TestBaseCase):
    """
    User signup test cases
    """

    @patch('requests.get', Mock(return_value={}))
    def test_user_signup_succeed(self):
        """
        Test API can successfully register a new user
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')
        time.sleep(2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], SIGNUP_SUCCESS_MESSAGE)

    @patch('requests.get', Mock(return_value={}))
    def test_user_signup_with_blank_fields_fails(self):
        """
        Test register a new user with missing details
        """
        response = self.signup_user_with_missing_fields()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
            {'password': ['This field is required.']}, 'status': 'failed'})

    @patch('requests.get', Mock(return_value={}))
    def test_user_signup_with_empty_fields_fails(self):
        """
        Test register a new user with empty fields
        """
        response = self.signup_user_with_empty_fields()
        time.sleep(2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
            {'email': ['This field may not be blank.']}, 'status': 'failed'})

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_signup_existing_user(self):
        """
        Test register existing user
        """
        response = self.signup_existing_user()
        time.sleep(2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
            {'email': ['Email already exist.']}, 'status': 'failed'})