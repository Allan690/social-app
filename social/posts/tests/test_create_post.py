from unittest.mock import patch, Mock

from rest_framework.views import status
from social.helpers.constants import POST_CREATION_SUCCESS_MESSAGE
from .base_test import TestBaseCase
from ...authentication.tests.test_retrieve_user import MockThread


class CreatePostTest(TestBaseCase):

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_post_creation_successful(self):
        """
        Test create post
        """
        response = self.create_post_succeeds()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         POST_CREATION_SUCCESS_MESSAGE)
