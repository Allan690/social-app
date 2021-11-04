from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from ..authentication.models import User
from ..like_dislike.models import LikeDislike
from ..models import BaseModel


class Post(BaseModel):
    """ the posts model"""
    body = models.CharField(max_length=300)
    votes = GenericRelation(LikeDislike, related_query_name='posts')
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="creator")
