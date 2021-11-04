from unittest.mock import patch,Mock
from rest_framework import status
from .base_test import TestBaseCase


class MockThread:
    def start(self):
        pass


class RetrieveUserTest(TestBaseCase):
    """
    Test for account verification
    """

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_user_succeeds(self):
        """
        Test retrieve user details successfully
        """
        user = self.activated_user()
        response = self.client.get(
            self.retrieve_update_user_url,
            HTTP_AUTHORIZATION='Token ' + user.token
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['email'], user.email)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_user_without_token_fails(self):
        """
        Test for user retrieval failure
        due to missing token
        """
        response = self.client.get(self.retrieve_update_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            b'Authentication credentials were not provided.', response.content)
