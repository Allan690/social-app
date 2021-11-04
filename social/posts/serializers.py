from rest_framework import serializers
from social.authentication.serializers import UserSearchSerializer
from social.posts.models import Post


class PostCreationSerializer(serializers.ModelSerializer):
    """ post creation serializer"""
    creator = serializers.CharField(read_only=True)
    body = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=3
    )

    @staticmethod
    def get_creator(obj):
        """
        get the post creator object
        Args:
            obj (object): current object reference
        Return:
            (obj): The creator object
        """
        return obj.id

    class Meta:
        model = Post
        fields = ('id', 'creator', 'body')


class PostUpdateSerializer(serializers.ModelSerializer):
    """ handles post update serialization"""
    id = serializers.CharField(read_only=True)
    creator = serializers.CharField(read_only=True)
    body = serializers.CharField(
        required=True,
        allow_null=False,
        min_length=3
    )

    class Meta:
        model = Post
        fields = "__all__"

    @staticmethod
    def get_creator(request):
        return request.creator.id


class PostRetrieveSerializer(serializers.ModelSerializer):
    creator = UserSearchSerializer()
    likes_count = serializers.SerializerMethodField('get_likes_count')
    dislikes_count = serializers.SerializerMethodField('get_dislikes_count')

    def get_likes_count(self, obj):
        return Post.objects.get(id=obj.id).votes.likes().count()

    def get_dislikes_count(self, obj):
        return Post.objects.get(id=obj.id).votes.dislikes().count()

    class Meta:
        model = Post
        fields = ('id', 'creator', 'body', 'likes_count', 'dislikes_count')
