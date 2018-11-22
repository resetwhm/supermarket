from django.db import models


class Basemodels(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    isdelete = models.BooleanField(default=False)

    class Meta:
        abstract = True