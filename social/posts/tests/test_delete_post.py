from unittest.mock import patch, Mock

from rest_framework.reverse import reverse
from rest_framework.views import status
from .base_test import TestBaseCase
from ...authentication.tests.test_retrieve_user import MockThread


class PostDeleteTest(TestBaseCase):

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_delete_post_succeeds(self):
        """
        Test delete post with correct privileges is successful
        """
        post = self.create_post()
        response = self.client.delete(
            reverse('posts:update-post', args=[str(post.id)]),
            self.body, HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
