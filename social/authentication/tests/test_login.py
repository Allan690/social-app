import json
from unittest.mock import patch, Mock

from .base_test import TestBaseCase
from rest_framework.views import status

from .test_retrieve_user import MockThread


class UserLoginTest(TestBaseCase):
    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_user_login_succeeds(self):
        """if user is registered"""
        response = self.login_user_successfull()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_login_unregistered_user_fails(self):
        """Test login for unregistered users"""
        response = self.login_user_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(json.loads(response.content), {'errors':
                                                            {'error': [
                                                                'A user with this email and password'
                                                                ' was not found.']},
                                                        'status': 'failed'})
