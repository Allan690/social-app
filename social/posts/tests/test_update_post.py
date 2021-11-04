from unittest.mock import patch, Mock

from rest_framework.views import status
from .base_test import TestBaseCase
from ...authentication.tests.test_retrieve_user import MockThread


class PostUpdateTest(TestBaseCase):

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_update_post_succeeds(self):
        """
        Test update post with correct privileges is successful
        """
        response = self.update_post_body_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data) != 0)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_update_post_no_access_fails(self):
        """
        Test updating post without access privileges fails
        """
        response = self.update_post_body_no_rights()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b'You are not the creator of this post', response.content)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_update_non_existing_post_fails(self):
        """
        Test updating non existing post fails
        """
        response = self.update_non_existing_post_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
