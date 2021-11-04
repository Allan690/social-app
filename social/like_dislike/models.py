from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

from social.authentication.models import User


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # sums up our votes and gets the rating
        return self.get_queryset().aggregate(
            models.Sum('vote')).get('vote__sum') or 0

    def posts(self):
        return self.get_queryset().filter(
            content_type__model='post'
        ).order_by('-posts__created_at')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )
    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=300)
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()
