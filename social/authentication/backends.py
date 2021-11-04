from rest_framework import authentication
from ..helpers.token import get_token_data


class JWTAuthentication(authentication.BaseAuthentication):
    """
    This is called on every request to check if the user is authenticated
    """

    @classmethod
    def authenticate(cls, request):
        """
        This checks that the passed JWT token is valid and returns
        a user and his/her token on successful verification
        """

        # Get the passed token
        auth_header = authentication.get_authorization_header(
            request).decode('utf-8')
        if not auth_header or auth_header.split()[0].lower() != 'token':
            return None
        token = auth_header.split(" ")[1]
        # Attempt decoding the token
        user = get_token_data(token)
        # Check this user is activated

        return (user, token)
