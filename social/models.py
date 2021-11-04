import uuid

from django.db import models


class BaseModel(models.Model):
    """
    The common field in all the models are defined here
    """
    # Add id to every entry in the database
    id = models.UUIDField(
        db_index=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # add deleted option for every entry
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(BaseModel, self).save()

    class Meta:
        abstract = True  # Set this model as Abstract
