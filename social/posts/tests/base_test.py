import uuid

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.reverse import reverse as api_reverse
from ...authentication.models import User
from ..models import Post


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.login_url = api_reverse('authentication:user-login')
        self.create_post_url = api_reverse('posts:create-post')
        self.retrieve_posts_url = api_reverse('posts:post-retrieve')

        self.user_one = User.objects.create_user(
            email='jane1@doe.com',
            password='janeDoe@123')

        self.user_two = User.objects.create_user(
            email='mary@mary.com',
            password='Pass@123',
            username="mary121312"
        )

        self.valid_post_details = {
            "body": "sample post"
        }

        self.valid_user_login_details = {
            'email': "jane1@doe.com",
            'password': "janeDoe@123",
        }

        self.valid_user_two_login_details = {
            'email': "mary@mary.com",
            'password': "Pass@123",
        }

        self.token = self.login_user().data['token']
        self.token_two = self.login_user_two().data['token']
        self.body = {
            "body": "new sample body1"
        }

    def login_user(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_login_details, format='json')

    def login_user_two(self):
        """
        method to login user two
        """
        return self.client.post(self.login_url,
                                self.valid_user_two_login_details,
                                format='json')

    def create_post_succeeds(self):
        """
        Register post succeeds
        """
        response = self.client.post(
            self.create_post_url, self.valid_post_details,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def create_post(self):
        self.client.post(
            self.create_post_url, self.valid_post_details,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return Post.objects.filter(creator=self.user_one.id).first()

    def retrieve_post_successfully(self):
        """
        Retrieve single post
        """
        self.create_post()
        post = self.create_post()
        response = self.client.get(
            reverse('posts:update-post', args=[post.id]),
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def retrieve_post_without_token(self):
        """
        Retrieve single post without token
        """
        post = self.create_post()
        response = self.client.get(
            reverse('posts:update-post', args=[post.id]))
        return response

    def retrieve_non_existing_post_fails(self):
        """
        Retrieve non existing post
        """
        self.create_post()
        response = self.client.get(
            reverse('posts:update-post', args=[uuid.uuid4()]),
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    def update_post_body_successfully(self):
        """
        Update post body successfully
        """
        post = self.create_post()
        response = self.client.patch(
            reverse('posts:update-post', args=[str(post.id)]),
            self.body, HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )
        return response

    def update_post_body_no_rights(self):
        """
        Update post body with no rights
        """
        post = self.create_post()
        response = self.client.patch(
            reverse('posts:update-post', args=[post.id]),
            self.body,
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))
        return response

    def update_non_existing_post_fails(self):
        """
        Update non existing post fails
        """
        response = self.client.patch(
            reverse('posts:update-post', args=[uuid.uuid4()]),
            self.body,
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def retrieve_posts(self):
        """
        Retrieve  posts
        """
        self.create_post()
        response = self.client.get(
            self.retrieve_posts_url, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response
