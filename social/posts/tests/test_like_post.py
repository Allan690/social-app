from unittest.mock import patch, Mock

from rest_framework.reverse import reverse
from .base_test import TestBaseCase
from ...authentication.tests.test_retrieve_user import MockThread


class PostLikeDislike(TestBaseCase):

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
           )
    def test_post_like_successful(self):
        """
        Test create like successful
        """
        post = self.create_post()
        response = self.client.post(
            reverse('like_dislike:post-like', args=[str(post.id)]),
            self.body, HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('like_count', response.data,)
        self.assertEqual(response.data['like_count'], 1)
        self.assertEqual(response.data['dislike_count'], 0)

    @patch('social.authentication.views.UpdateUserThread', Mock(
        return_value=MockThread())
    )
    def test_post_dislike_successfully(self):
        """
        Test create like successful
        """
        post = self.create_post()
        response = self.client.post(
            reverse('like_dislike:post-dislike', args=[str(post.id)]),
            self.body, HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('like_count', response.data,)
        self.assertEqual(response.data['like_count'], 0)
        self.assertEqual(response.data['dislike_count'], 1)

