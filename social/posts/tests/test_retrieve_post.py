from unittest.mock import patch, Mock

from rest_framework.views import status
from .base_test import TestBaseCase
from ...authentication.tests.test_retrieve_user import MockThread


class PostRetrieveTest(TestBaseCase):

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_post_succeeds(self):
        """
        Test post retrieval succeeds
        """
        response = self.retrieve_post_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data)!=0)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_non_existing_post_fails(self):
        """
        Test retrieving non-existing post will fail
        """
        response = self.retrieve_non_existing_post_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_post_without_token_fails(self):
        """
        Test post retrieve post without token
        """
        response = self.retrieve_post_without_token()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            b'Authentication credentials were not provided', response.content)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_retrieve_posts_successfully(self):
        """
        Test retrieve posts successfully
        """
        response = self.retrieve_posts()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['paginationMeta']['currentPage'], 1)
        self.assertIsInstance(response.data['paginationMeta'], dict)
        self.assertIsInstance(response.data['rows'], list)

