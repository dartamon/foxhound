from django.db import models
from djangotoolbox.fields import ListField

# Create your models here.
class QueryModel(models.Model):
    sessionname = models.TextField()
    savedimages = ListField()
    savedtags = ListField()
    def __str__(self):
        return self.sessionname