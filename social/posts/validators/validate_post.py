from rest_framework.serializers import ValidationError
from ..models import Post
from ...helpers.serialization_errors import error_dict


def validate_post_id(user_id, post_id, method=None):
    """Validate that the post exists
    Args:
        post_id (str): the post id
        user_id(str): the user id
        method: the http request method is a must for a get request
    Raises:
        a validation error if the post does not exist
    Return:
        post (obj): the post object
    """
    try:
        post = Post.objects.get(id=post_id)
        if method == 'GET':
            return post
        if post.creator.id != user_id:
            raise ValidationError(
                error_dict['object_permission_denied'].format("post"),
            )
        return post
    except Post.DoesNotExist:
        raise ValidationError(
            error_dict['does_not_exist'].format("Post"),
        )
