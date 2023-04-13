from django.db import models


# Create your models here.
class Audit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Table(Audit):
    name = models.CharField(max_length=20)
    fields = models.JSONField()
