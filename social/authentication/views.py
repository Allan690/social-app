from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..helpers.renderers import RequestJSONRenderer
from .serializers import (RegistrationSerializer, LoginSerializer,
                          UserRetrieveUpdateSerializer)
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE
from ..helpers.update_user import UpdateUserThread


class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user signup
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        created_user = serializer.save()
        return_message = {
            'message': SIGNUP_SUCCESS_MESSAGE,
            'data': serializer.data
        }
        UpdateUserThread(email=created_user.email).start()
        return Response(return_message, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    # Login user class
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user login
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, generics.GenericAPIView
):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = UserRetrieveUpdateSerializer

    def get(self, request, *args, **kwargs):
        """
        retrieve user details from the token provided
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        override the default patch() method to enable
        the user update their details
        """
        data = request.data
        serializer = self.serializer_class(
            request.user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
