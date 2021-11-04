import uuid

from rest_framework import generics, status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ..helpers.renderers import RequestJSONRenderer
from ..posts.models import Post
from ..posts.serializers import (
    PostCreationSerializer, PostRetrieveSerializer, PostUpdateSerializer
)
from ..helpers.constants import POST_CREATION_SUCCESS_MESSAGE
from ..posts.validators.validate_post import validate_post_id
from ..helpers.pagination_helper import Pagination


class CreatePostAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = PostCreationSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the default post()
        """
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return_message = {
            'message': POST_CREATION_SUCCESS_MESSAGE,
            'data': serializer.data
        }
        return Response(return_message, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin, generics.GenericAPIView
):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostRetrieveSerializer

    def get(self, request, post_id):
        """
        Retrieve post details from the provided payload
        """
        self.renderer_classes = (RequestJSONRenderer,)
        post = validate_post_id(request.user.id, post_id, 'GET')
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id):
        """
        override the default patch() method to enable
        the user update a post
        """
        self.renderer_classes = (RequestJSONRenderer,)
        self.serializer_class = PostUpdateSerializer
        post = validate_post_id(request.user.id, post_id)
        data = request.data
        serializer = self.serializer_class(
            post, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        """
        override the default patch() method to enable
        the user update a post
        """
        validate_post_id(request.user.id, post_id)
        Post.objects.filter(id=uuid.UUID(post_id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsRetrieveApiView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = PostRetrieveSerializer
    pagination_class = Pagination
    queryset = Post.objects.filter(deleted=False)
    filter_backends = (SearchFilter,)
    search_fields = ('body',)

    @action(methods=['GET'], detail=False, url_name='Search post')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
