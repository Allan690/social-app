import json

from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..helpers.renderers import RequestJSONRenderer
from ..like_dislike.models import LikeDislike


class VotesView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    model = None
    vote_type = None

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs.get('post_id'))
        # GenericForeignKey does not support get_or_create
        try:
            like_dislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=str(obj.id), user=request.user)
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                like_dislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
        data = {
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }
        return Response(data=data, status=status.HTTP_200_OK)
